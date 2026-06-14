#!/usr/bin/env python3
"""可灵 Kling API 鉴权 smoke test —— 不花生成额度。

读取 .env 的 KLING_ACCESS_KEY / KLING_SECRET_KEY，生成 JWT，
对多个候选 base URL 各发一个"查询不存在任务"的请求：
  - 401/鉴权错误  => 密钥或签名不对
  - 404/任务不存在/参数错误(非鉴权) => 鉴权通过、base 正确
据此判断密钥可用且找到正确的 API 域名。
"""
import base64, hashlib, hmac, json, os, time, urllib.request, urllib.error

def load_env(path):
    env = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def b64url(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=")

def make_jwt(ak, sk):
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {"iss": ak, "exp": now + 1800, "nbf": now - 5}
    seg = b64url(json.dumps(header, separators=(",", ":")).encode()) + b"." + \
          b64url(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(sk.encode(), seg, hashlib.sha256).digest()
    return (seg + b"." + b64url(sig)).decode()

def probe(base, token):
    # 查询一个几乎不可能存在的 image 任务 id；只看鉴权是否通过
    url = base.rstrip("/") + "/v1/images/generations/smoke-test-nonexistent-id"
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read(400).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(400).decode("utf-8", "replace")
    except Exception as e:
        return None, "ERR: " + repr(e)

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = load_env(os.path.join(root, ".env"))
    ak, sk = env.get("KLING_ACCESS_KEY"), env.get("KLING_SECRET_KEY")
    if not ak or not sk:
        print("FAIL: .env 缺少 KLING_ACCESS_KEY / KLING_SECRET_KEY"); return 2
    token = make_jwt(ak, sk)
    print("JWT 生成 OK，前 24 字符:", token[:24], "...")
    bases = [
        "https://api-beijing.klingai.com",
        "https://api.klingai.com",
        "https://api-singapore.klingai.com",
    ]
    good = None
    for b in bases:
        st, body = probe(b, token)
        print(f"\n[{b}] status={st}\n  {body[:300]}")
        if st is not None and st != 401 and st != 403 and not (body or '').startswith('ERR'):
            good = good or b
    print("\n==== 判定 ====")
    if good:
        print(f"鉴权通过，建议 base URL = {good}")
        return 0
    print("未确认通过：若全部 401/403 => 密钥/签名问题；若全部 ERR(DNS/超时) => 网络无法访问该域名。")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
