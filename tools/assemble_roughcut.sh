#!/bin/zsh
# NX-071 无声粗剪：把 05_video_projects/V01..V12.mp4 按 storyboard 顺序与时长
# 拼成 1080x1920、加轻度监控暗绿质感的一条无声底片。
# 配音/字幕/精修留给剪映（见 texture_notes.md）。
# 用法: zsh tools/assemble_roughcut.sh
set -u
ROOT="${0:A:h:h}"
EP="$ROOT/shorts/yejiban_anomaly_archive/NX-071_undelivered_letter"
VID="$ROOT/shorts/yejiban_anomaly_archive/05_video_projects"
OUT="$EP/final_roughcut_silent.mp4"
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
