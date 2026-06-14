#!/bin/zsh
set -u
here="${0:A:h}"; root="${here:h:h}"
fx="$(mktemp -d "$PWD/.tmp_fixtures.XXXXXX")"
trap 'rm -rf "$fx"' EXIT
mk() {
  local size="$1" t="$2" aud="$3" out="$4"
  if [[ "$aud" == yes ]]; then
    ffmpeg -y -hide_banner -f lavfi -i testsrc2=size=${size}:rate=10 \
      -f lavfi -i sine=frequency=1000:sample_rate=48000 -t "$t" -filter:a "volume=2.2" \
      -c:v libx264 -preset ultrafast -crf 35 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest "$out" >/dev/null 2>&1
  else
    ffmpeg -y -hide_banner -f lavfi -i testsrc2=size=${size}:rate=10 -t "$t" \
      -c:v libx264 -preset ultrafast -crf 35 -pix_fmt yuv420p -an "$out" >/dev/null 2>&1
  fi
}
mk 1080x1920 62 yes "$fx/pass.mp4"
mk 720x1280  62 yes "$fx/fail_res.mp4"
mk 1080x1920 50 yes "$fx/fail_dur.mp4"
mk 1080x1920 62 no  "$fx/fail_noaudio.mp4"
"$root/tools/validate_export.sh" "$fx/pass.mp4";        [[ $? -eq 0 ]]  || { echo "FAIL pass"; exit 1; }
"$root/tools/validate_export.sh" "$fx/fail_res.mp4";    [[ $? -eq 10 ]] || { echo "FAIL res"; exit 1; }
"$root/tools/validate_export.sh" "$fx/fail_dur.mp4";    [[ $? -eq 10 ]] || { echo "FAIL dur"; exit 1; }
"$root/tools/validate_export.sh" "$fx/fail_noaudio.mp4";[[ $? -eq 10 ]] || { echo "FAIL noaudio"; exit 1; }
"$root/tools/validate_export.sh" "$fx/nonexist.mp4";    [[ $? -eq 2 ]]  || { echo "FAIL missing"; exit 1; }
echo "ALL PASS"
