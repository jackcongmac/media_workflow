#!/bin/zsh
set -u
here="${0:A:h}"; root="${here:h:h}"
tmp="$(mktemp -d "$PWD/.tmp_new_episode.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/tools" "$tmp/shorts/yejiban_anomaly_archive/_TEMPLATE"
for f in research.md script.md storyboard.csv image_prompts.md video_prompts.md voiceover.txt captions.srt texture_notes.md publish_copy.md; do
  : > "$tmp/shorts/yejiban_anomaly_archive/_TEMPLATE/$f"
done
cp "$root/tools/new_episode.sh" "$tmp/tools/new_episode.sh"
MEDIA_WORKFLOW_ROOT="$tmp" "$tmp/tools/new_episode.sh" NX-071 undelivered_letter
[[ $? -eq 0 ]] || { echo "FAIL create exit"; exit 1; }
[[ -d "$tmp/shorts/yejiban_anomaly_archive/NX-071_undelivered_letter" ]] || { echo "FAIL dir"; exit 1; }
MEDIA_WORKFLOW_ROOT="$tmp" "$tmp/tools/new_episode.sh" NX-071 undelivered_letter
[[ $? -eq 4 ]] || { echo "FAIL no-overwrite exit"; exit 1; }
MEDIA_WORKFLOW_ROOT="$tmp" "$tmp/tools/new_episode.sh" BAD-1 x
[[ $? -eq 2 ]] || { echo "FAIL arg-validate exit"; exit 1; }
echo "ALL PASS"
