#!/bin/zsh
# 无声粗剪：把某集的 V01..V12.mp4 按 storyboard 顺序与时长拼成 1080x1920、
# 加轻度监控暗绿质感的一条无声底片。配音/字幕/精修留给剪映（见 texture_notes.md）。
# 用法: zsh tools/assemble_roughcut.sh [集目录名]
#   不带参数 = NX-071（向后兼容，读扁平 05_video_projects/）。
#   带参数   = 该集，读按集隔离的 05_video_projects/<集目录名>/。
set -u
ROOT="${0:A:h:h}"
ARCHIVE="$ROOT/shorts/yejiban_anomaly_archive"
DEFAULT_EP="NX-071_undelivered_letter"
EP_NAME="${1:-$DEFAULT_EP}"
EP="$ARCHIVE/$EP_NAME"
NS_VID="$ARCHIVE/05_video_projects/$EP_NAME"
# 命名空间隔离的片源目录；仅默认集(NX-071)在其命名空间目录不存在时回退扁平目录。
if [[ "$EP_NAME" == "$DEFAULT_EP" && ! -d "$NS_VID" ]]; then
  VID="$ARCHIVE/05_video_projects"
else
  VID="$NS_VID"
fi
OUT="$EP/final_roughcut_silent.mp4"
if [[ ! -d "$EP" ]]; then echo "FAIL: 集目录不存在: $EP"; exit 1; fi
mkdir -p "$VID"
WORK="$(mktemp -d "$VID/.roughcut.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

# 监控质感：压暗、偏冷绿、轻噪点、暗角
FILT="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=brightness=-0.05:contrast=1.06:saturation=0.82,colorbalance=gm=0.12:bm=-0.06,noise=alls=7:allf=t,vignette=PI/5"

list="$WORK/list.txt"; : > "$list"; n=0; missing=0
# 读 storyboard（跳表头），按 shot 顺序处理
tail -n +2 "$EP/storyboard.csv" | while IFS=, read -r shot start end desc camera subject texture ff v; do
  dur=$(awk -v s="$start" -v e="$end" 'BEGIN{printf "%.3f", e-s}')
  src="$VID/$v.mp4"
  if [[ ! -f "$src" ]]; then echo "[缺] $v.mp4"; missing=$((missing+1)); continue; fi
  seg="$WORK/${v}_seg.mp4"
  ffmpeg -nostdin -y -hide_banner -loglevel error -i "$src" -t "$dur" -vf "$FILT" \
    -an -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p "$seg" \
    && echo "file '$seg'" >> "$list" && echo "[OK] $v -> ${dur}s" && n=$((n+1))
done

if [[ ! -s "$list" ]]; then echo "FAIL: 没有可用片段"; exit 1; fi
ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "$list" -c copy "$OUT" \
  || { echo "FAIL: 拼接失败"; exit 1; }

echo "----"
echo "粗剪完成: $OUT"
ffprobe -v error -show_entries stream=width,height -show_entries format=duration -of default=noprint_wrappers=1 "$OUT"
[[ $missing -gt 0 ]] && echo "注意: 有 $missing 条片段缺失，粗剪不完整（等 12 条出齐再跑一次）"
exit 0
