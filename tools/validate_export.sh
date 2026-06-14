#!/bin/zsh
set -u
fail() { code="$1"; shift; print -u2 -- "FAIL: $*"; exit "$code"; }
[[ $# -eq 1 ]] || fail 2 "usage: tools/validate_export.sh <path-to-mp4>"
mp4="$1"
[[ -f "$mp4" ]] || fail 2 "file not found: $mp4"
command -v ffprobe >/dev/null 2>&1 || fail 2 "ffprobe not installed"
resolution="$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$mp4")" || fail 2 "ffprobe video failed"
duration="$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$mp4")" || fail 2 "ffprobe duration failed"
audio_count="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$mp4" | awk 'NF{n++} END{print n+0}')"
hard_fail=0
res_msg="resolution: $resolution"; [[ "$resolution" == "1080x1920" ]] || { hard_fail=1; res_msg="resolution: $resolution (expected 1080x1920)"; }
awk -v d="$duration" 'BEGIN{exit !(d>=60 && d<=75)}'; dur_ok=$?
dur_msg="duration: ${duration}s OK"; [[ $dur_ok -eq 0 ]] || { hard_fail=1; dur_msg="duration: ${duration}s (expected 60-75)"; }
aud_msg="audio streams: $audio_count OK"; [[ "$audio_count" -ge 1 ]] || { hard_fail=1; aud_msg="audio streams: 0 (expected >=1)"; }
lufs=""
if [[ "$audio_count" -ge 1 ]]; then
  log="$(ffmpeg -hide_banner -nostdin -i "$mp4" -vn -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1)"
  lufs="$(print -- "$log" | awk -F: '/"input_i"/ {v=$2; gsub(/[, "]/,"",v); print v; exit}')"
fi
loud_msg="integrated loudness: ${lufs:-unknown}${lufs:+ LUFS}"
if [[ -n "$lufs" && "$lufs" != "-inf" ]]; then
  awk -v l="$lufs" 'BEGIN{exit !(l < -16 || l > -13)}' && loud_msg="$loud_msg  [WARN outside -16..-13]"
fi
if [[ $hard_fail -eq 0 ]]; then
  print -- "PASS: export validation passed"
  print -- "- $res_msg"; print -- "- $dur_msg"; print -- "- $aud_msg"; print -- "- $loud_msg"
  exit 0
else
  print -u2 -- "FAIL: export validation failed"
  print -u2 -- "- $res_msg"; print -u2 -- "- $dur_msg"; print -u2 -- "- $aud_msg"
  exit 10
fi
