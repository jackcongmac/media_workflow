#!/usr/bin/env python3
"""可灵 Kling 批量出片客户端（幂等、可续跑、不重复扣费）。

用法：
  python3 tools/kling_gen.py images [--only FF01]   # 文生图 -> 03_images/FFxx.png
  python3 tools/kling_gen.py videos [--only V01]     # 图生视频 -> 05_video_projects/Vxx.mp4
  python3 tools/kling_gen.py probe                   # 只发一个建图请求探接口/余额，不轮询

幂等：成片文件已存在=跳过；任务已建(state 记了 task_id)=续查，不重复创建/扣费。
驱动数据：storyboard.csv(镜头/FF/V/时长) + image_prompts.md(FFxx) + video_prompts.md(Vxx)。
"""
import argparse, base64, hashlib, hmac, json, os, re, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(ROOT, "shorts/yejiban_anomaly_archive")
DEFAULT_EP = "NX-071_undelivered_letter"
# 默认值（NX-071 历史产物在扁平目录）；__main__ 里按 --ep 用 set_episode() 覆盖。
EP = os.path.join(ARCHIVE, DEFAULT_EP)
IMG_DIR = os.path.join(ARCHIVE, "03_images")
VID_DIR = os.path.join(ARCHIVE, "05_video_projects")

def set_episode(ep):
    """按集设置目录。输出目录按集命名空间隔离 05_video_projects/<ep>/，
    避免不同集的 V01.mp4 互相覆盖/误跳过。NX-071 历史产物在扁平目录，
    其命名空间目录不存在时回退扁平目录以保持向后兼容。"""
    global EP, IMG_DIR, VID_DIR
    EP = os.path.join(ARCHIVE, ep)
    ns_img = os.path.join(ARCHIVE, "03_images", ep)
    ns_vid = os.path.join(ARCHIVE, "05_video_projects", ep)
    use_flat = (ep == DEFAULT_EP and not os.path.isdir(ns_vid))
    IMG_DIR = os.path.join(ARCHIVE, "03_images") if use_flat else ns_img
    VID_DIR = os.path.join(ARCHIVE, "05_video_projects") if use_flat else ns_vid

STYLE = "竖屏9:16，夜间监控画风，低照度，写实，电影感冷调，画面内无任何文字水印logo，监控/夜视/噪点质感"
NEG_IMG = "多余手指、畸形手、畸形脸、五官扭曲、现代品牌logo、画面文字、字幕、水印、卡通、3D渲染感、过曝、血腥、可辨认真实地标"
NEG_VID = "人物快速大幅运动、多人乱动、五官扭曲变形、手指增生、镜头穿模、画面文字浮现、抖动失控、画质忽然变清晰失去监控感、护目镜、墨镜、太阳镜、大号眼镜、摩托头盔、滑雪头盔、面部高清特写、脱离监控宫格的普通人像特写"

def load_env():
    env = {}
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1); env[k.strip()] = v.strip()
    return env

ENV = load_env()
AK = ENV.get("KLING_ACCESS_KEY"); SK = ENV.get("KLING_SECRET_KEY")
BASE = ENV.get("KLING_BASE", "https://api-beijing.klingai.com")
IMG_MODEL = ENV.get("KLING_IMG_MODEL", "kling-v2")
VID_MODEL = ENV.get("KLING_VID_MODEL", "kling-v1-6")
VID_MODE = ENV.get("KLING_VID_MODE", "std")

def b64url(b): return base64.urlsafe_b64encode(b).rstrip(b"=")

def jwt():
    h = {"alg": "HS256", "typ": "JWT"}; now = int(time.time())
    p = {"iss": AK, "exp": now + 1800, "nbf": now - 5}
    seg = b64url(json.dumps(h, separators=(",", ":")).encode()) + b"." + b64url(json.dumps(p, separators=(",", ":")).encode())
    return (seg + b"." + b64url(hmac.new(SK.encode(), seg, hashlib.sha256).digest())).decode()

def api(method, path, body=None):
    url = BASE.rstrip("/") + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Authorization": "Bearer " + jwt(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode("utf-8", "replace"))
        except Exception: return e.code, {"raw": "http error"}
    except Exception as e:
        return None, {"err": repr(e)}

# ---------- 解析驱动数据 ----------
def parse_storyboard():
    shots = []
    p = os.path.join(EP, "storyboard.csv")
    rows = [r for r in open(p, encoding="utf-8").read().splitlines() if r.strip()]
    for r in rows[1:]:
        c = r.split(",")
        start, end = float(c[1]), float(c[2])
        shots.append({"shot": c[0], "ff": c[7], "v": c[8],
                      "dur": "10" if (end - start) > 5 else "5"})
    return shots

def parse_prompts(path, tag):
    out = {}
    for line in open(path, encoding="utf-8"):
        m = re.search(r"\*\*" + tag + r"(\d+)\*\*[^：:]*[：:]\s*(.+)", line)
        if m: out[tag + m.group(1)] = m.group(2).strip()
    return out

# ---------- 状态(续跑/防重复扣费) ----------
def load_state(d):
    p = os.path.join(d, ".kling_state.json")
    return json.load(open(p)) if os.path.exists(p) else {}

def save_state(d, st):
    json.dump(st, open(os.path.join(d, ".kling_state.json"), "w"), ensure_ascii=False, indent=2)

def download(url, dest):
    with urllib.request.urlopen(url, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())

def poll(path_prefix, task_id, kind, dest, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        st, resp = api("GET", path_prefix + "/" + task_id)
        data = (resp or {}).get("data") or {}
        status = data.get("task_status")
        if status == "succeed":
            res = data.get("task_result") or {}
            items = res.get("images") if kind == "img" else res.get("videos")
            url = items[0]["url"]
            download(url, dest)
            return True, "succeed"
        if status == "failed":
            return False, "failed: " + json.dumps(data.get("task_status_msg", ""), ensure_ascii=False)
        time.sleep(6)
    return False, "timeout"

# ---------- 主流程 ----------
def gen_images(only=None):
    os.makedirs(IMG_DIR, exist_ok=True)
    prompts = parse_prompts(os.path.join(EP, "image_prompts.md"), "FF")
    state = load_state(IMG_DIR)
    for shot in parse_storyboard():
        ff = shot["ff"]
        if only and ff != only: continue
        dest = os.path.join(IMG_DIR, ff + ".png")
        if os.path.exists(dest): print(f"[skip] {ff} 已存在"); continue
        tid = (state.get(ff) or {}).get("task_id")
        if not tid:
            body = {"model_name": IMG_MODEL, "prompt": (prompts.get(ff, "") + " " + STYLE)[:2400],
                    "negative_prompt": NEG_IMG, "n": 1, "aspect_ratio": "9:16"}
            st, resp = api("POST", "/v1/images/generations", body)
            print(f"[{ff}] create -> http {st} {json.dumps(resp, ensure_ascii=False)[:200]}")
            if (resp or {}).get("code") != 0:
                print(f"[{ff}] 创建失败，停。"); return
            tid = resp["data"]["task_id"]; state[ff] = {"task_id": tid}; save_state(IMG_DIR, state)
        ok, msg = poll("/v1/images/generations", tid, "img", dest)
        print(f"[{ff}] {'OK -> ' + dest if ok else 'FAIL ' + msg}")
        if not ok: return

def gen_videos(only=None):
    os.makedirs(VID_DIR, exist_ok=True)
    prompts = parse_prompts(os.path.join(EP, "video_prompts.md"), "V")
    state = load_state(VID_DIR)
    for shot in parse_storyboard():
        v, ff, dur = shot["v"], shot["ff"], shot["dur"]
        if only and v != only: continue
        dest = os.path.join(VID_DIR, v + ".mp4")
        if os.path.exists(dest): print(f"[skip] {v} 已存在"); continue
        img_path = os.path.join(IMG_DIR, ff + ".png")
        if not os.path.exists(img_path): print(f"[{v}] 缺首帧 {ff}.png，跳过"); continue
        tid = (state.get(v) or {}).get("task_id")
        if not tid:
            img_b64 = base64.b64encode(open(img_path, "rb").read()).decode()
            body = {"model_name": VID_MODEL, "image": img_b64,
                    "prompt": prompts.get(v, ""), "negative_prompt": NEG_VID,
                    "mode": VID_MODE, "duration": dur, "cfg_scale": 0.5}
            st, resp = api("POST", "/v1/videos/image2video", body)
            print(f"[{v}] create -> http {st} {json.dumps(resp, ensure_ascii=False)[:200]}")
            if (resp or {}).get("code") != 0:
                print(f"[{v}] 创建失败，停。"); return
            tid = resp["data"]["task_id"]; state[v] = {"task_id": tid}; save_state(VID_DIR, state)
        ok, msg = poll("/v1/videos/image2video", tid, "vid", dest, timeout=900)
        print(f"[{v}] {'OK -> ' + dest if ok else 'FAIL ' + msg}")
        if not ok: return

def gen_t2v(only=None):
    """文生视频：不需首帧图，只吃视频额度。prompt = FF场景 + V运动 + 风格。"""
    os.makedirs(VID_DIR, exist_ok=True)
    ff_prompts = parse_prompts(os.path.join(EP, "image_prompts.md"), "FF")
    v_prompts = parse_prompts(os.path.join(EP, "video_prompts.md"), "V")
    state_path = os.path.join(VID_DIR, ".kling_state_t2v.json")
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    for shot in parse_storyboard():
        v, ff, dur = shot["v"], shot["ff"], shot["dur"]
        if only and v != only: continue
        dest = os.path.join(VID_DIR, v + ".mp4")
        if os.path.exists(dest): print(f"[skip] {v} 已存在"); continue
        tid = (state.get(v) or {}).get("task_id")
        if not tid:
            scene = ff_prompts.get(ff, ""); motion = v_prompts.get(v, "")
            prompt = (scene + "。镜头运动：" + motion + " " + STYLE)[:2400]
            body = {"model_name": VID_MODEL, "prompt": prompt, "negative_prompt": NEG_VID,
                    "mode": VID_MODE, "duration": dur, "aspect_ratio": "9:16", "cfg_scale": 0.5}
            st, resp = api("POST", "/v1/videos/text2video", body)
            print(f"[{v}] create -> http {st} {json.dumps(resp, ensure_ascii=False)[:200]}")
            if (resp or {}).get("code") != 0:
                print(f"[{v}] 创建失败，停。"); return
            tid = resp["data"]["task_id"]; state[v] = {"task_id": tid}
            json.dump(state, open(state_path, "w"), ensure_ascii=False, indent=2)
        ok, msg = poll("/v1/videos/text2video", tid, "vid", dest, timeout=900)
        print(f"[{v}] {'OK -> ' + dest if ok else 'FAIL ' + msg}")
        if not ok: return

def probe():
    prompts = parse_prompts(os.path.join(EP, "image_prompts.md"), "FF")
    body = {"model_name": IMG_MODEL, "prompt": (prompts.get("FF01", "") + " " + STYLE)[:2400],
            "negative_prompt": NEG_IMG, "n": 1, "aspect_ratio": "9:16"}
    st, resp = api("POST", "/v1/images/generations", body)
    print(f"probe create image -> http {st}\n{json.dumps(resp, ensure_ascii=False, indent=2)[:600]}")

if __name__ == "__main__":
    if not AK or not SK: sys.exit(".env 缺 KLING_ACCESS_KEY/KLING_SECRET_KEY")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["images", "videos", "t2v", "probe"])
    ap.add_argument("--only")
    ap.add_argument("--ep", default=DEFAULT_EP,
                    help="集目录名（shorts/yejiban_anomaly_archive/ 下），默认 NX-071")
    a = ap.parse_args()
    set_episode(a.ep)
    if a.cmd == "images": gen_images(a.only)
    elif a.cmd == "videos": gen_videos(a.only)
    elif a.cmd == "t2v": gen_t2v(a.only)
    else: probe()
