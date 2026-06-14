#!/bin/zsh
set -u
fail() { code="$1"; shift; print -u2 -- "FAIL: $*"; exit "$code"; }
[[ $# -eq 2 ]] || fail 2 "usage: tools/new_episode.sh <NX-NNN> <slug>"
nx="$1"; slug="$2"
case "$nx" in (NX-[0-9][0-9][0-9]) ;; (*) fail 2 "episode id must match NX-NNN, got: $nx" ;; esac
case "$slug" in (""|*[!A-Za-z0-9_-]*) fail 2 "slug must use only A-Z a-z 0-9 _ -" ;; esac
script_dir="${0:A:h}"
project_root="${MEDIA_WORKFLOW_ROOT:-${script_dir:h}}"
base="$project_root/shorts/yejiban_anomaly_archive"
template="$base/_TEMPLATE"
dest="$base/${nx}_${slug}"
required=(research.md script.md storyboard.csv image_prompts.md video_prompts.md voiceover.txt captions.srt texture_notes.md publish_copy.md)
[[ -d "$template" ]] || fail 3 "template dir missing: $template"
[[ ! -e "$dest" ]] || fail 4 "episode dir already exists: $dest"
for f in "${required[@]}"; do [[ -f "$template/$f" ]] || fail 3 "template missing required file: $template/$f"; done
tmp="$(mktemp -d "$base/.new_episode.${nx}_${slug}.XXXXXX")" || fail 5 "could not create temp dir under: $base"
rsync -a --exclude='._*' --exclude='.DS_Store' "$template"/ "$tmp"/ || fail 5 "template copy failed"
mv "$tmp" "$dest" || fail 5 "could not move temp episode dir into place: $dest"
print -- "$dest"
exit 0
