# Short Video Workflow Experiment

Date: 2026-06-09

## Goal

Build one repeatable short-video production workflow that can take a topic from research to publication without losing momentum. The first experiment should produce a small season of 10 videos, not a single over-polished video.

Success means:

- 10 finished vertical videos.
- Each video has script, sources, prompts, assets, edit file, captions, cover, publish copy, and analytics row.
- The workflow is reusable for the next topic.
- Publishing is automated where APIs allow it, and semi-automated where platforms block full automation.
- The final video is cinematic motion video, not a still-image slideshow.

## Recommended Theme

Series name:

**If Ancient Emperors Had a Crisis Room**

Chinese title options:

- **帝王危机室**
- **如果皇帝有现代参谋部**
- **皇帝的最后一场会议**

Core format:

Each episode turns one historical decision into a 60-90 second vertical micro-drama. It should feel like a tense boardroom, crisis meeting, or intelligence briefing, but the characters are emperors, generals, ministers, strategists, and rivals.

Why this theme:

- It keeps your original "帝王将相" interest, so previous research is not wasted.
- Micro-drama and vertical serialized storytelling are hot.
- AI history vlogging is emerging, but Chinese imperial "crisis-room drama" is still less crowded than generic "history explained" videos.
- It can be made from short AI-generated moving shots, voiceover, captions, music, and tight editing, so the first version does not require one expensive continuous AI video.

The creative promise:

> We do not lecture history. We recreate the moment when power had to make a decision.

## Season 1

Make 10 episodes around one emotional pattern: "A ruler has 3 bad choices and 20 seconds to decide."

Episode candidates:

1. Qin Shi Huang: burn the books or lose ideological control.
2. Liu Bang: spare Han Xin or fear him forever.
3. Xiang Yu: cross the river or die with pride.
4. Han Wudi: expand the empire or bankrupt it.
5. Cao Cao: execute Kong Rong or tolerate dissent.
6. Sima Yi: wait, pretend, survive.
7. Li Shimin: Xuanwu Gate before dawn.
8. Wu Zetian: rule openly or rule through others.
9. Zhao Kuangyin: take the throne without starting a bloodbath.
10. Chongzhen: one last court meeting before collapse.

## Production Stack

Research and planning:

- Claude Code: outline, research questions, source summaries, logic checks.
- Codex: script templates, prompt generation, folder management, batch exports, publish-package creation.
- Notion, Airtable, Google Sheets, or a local CSV: content database.

Script ownership:

- The user is not responsible for writing hooks or scripts.
- Claude/Codex acts as the first-season writing room.
- The user only chooses the topic direction, approves or rejects drafts, and gives simple feedback such as "too boring", "too long", "more dramatic", or "more factual".
- After 10 videos, hire a human short-drama/history scriptwriter only if the data proves the format works.

Image assets:

- GPT Image 2: covers, first-frame references, character portraits, room shots, symbolic objects.
- Public-domain museum images where useful.
- Optional stock footage: Pexels, Pixabay, Storyblocks, Envato.

Video assembly:

- MVP: AI image-to-video / text-to-video clips + CapCut/Jianying assembly + auto captions.
- Automation layer: FFmpeg for resizing, naming, watermarking, compression.
- Later: Remotion for fully template-based video rendering.

Audio:

- OpenAI TTS or ElevenLabs for voice.
- CapCut/Jianying for captions and timing.
- Licensed BGM only.

Publishing:

- YouTube: API upload is possible, but new unverified API projects upload as private until audited.
- TikTok: Direct Post requires app approval, `video.publish` permission, and user authorization; unaudited clients are private-only.
- Douyin, Xiaohongshu, Instagram: treat as semi-automated first unless official API access is already available.

## Folder Structure

Create one folder per season:

```text
shorts/
  season_001_emperor_crisis_room/
    00_research/
    01_scripts/
    02_prompts/
    03_images/
    04_audio/
    05_video_projects/
    06_exports/
    07_publish_packages/
    08_analytics/
```

Each episode uses this naming:

```text
E01_qin_shihuang_books/
  research.md
  script.md
  storyboard.csv
  image_prompts.md
  voiceover.txt
  captions.srt
  cover_prompt.md
  publish_copy.md
  final.mp4
```

## End-to-End Workflow

### 1. Trend Research

Output:

- 5 candidate topics.
- 1 chosen topic.
- 10 episode titles.
- 3 reference accounts or formats.
- Risk notes: copyright, factual sensitivity, platform restrictions.

Rule:

Do not start production until the topic can support at least 10 videos.

### 2. Source Research

For each episode, collect:

- Main historical event.
- 3-5 verifiable facts.
- 1 central conflict.
- 1 emotional hook.
- 1 open question.
- 2-4 source links or book references.

Research should answer:

- What decision was being made?
- Who had something to lose?
- What did later people misunderstand?
- What is the one line viewers will repeat in comments?

### 3. Script

Target:

- 60-90 seconds.
- 130-220 Chinese characters for fast dramatic narration, or 180-280 characters for slower documentary narration.
- First 3 seconds must create conflict.
- End with a question or twist.

Script template:

```text
Hook:
Historical setup:
Conflict:
Decision:
Consequence:
Comment bait:
```

Writing-room rule:

For every episode, the AI writing room must deliver:

- 5 hook options.
- 3 title options.
- 1 dramatic script.
- 1 more factual script.
- 1 shorter 45-second version.
- 1 storyboard-ready caption version.

The user should never start from a blank page.

### 4. Storyboard

Each video uses 6-8 shots:

1. Cover shot.
2. Crisis-room wide shot.
3. Ruler close-up.
4. Opponent or minister close-up.
5. Map, edict, battlefield, or symbolic object.
6. Decision moment.
7. Consequence image.
8. Final question screen.

### 5. Image Generation

Use GPT Image 2 for:

- 1 cover.
- 6-8 first-frame references for video generation.
- 1 optional character reference.

Style rule:

Use "cinematic historical micro-drama, vertical 9:16, realistic lighting, Chinese imperial court, dramatic but historically grounded, no fantasy armor, no modern objects, no text in image."

Quality rule:

Generate low/medium drafts first. Only upscale or regenerate the cover and first-frame references that will become moving video clips.

Hard rule:

Do not publish a video made from still images with simple push-in/pan effects. Still images are allowed only as:

- cover image
- first frame for image-to-video
- historical document/map/object insert of 1-2 seconds
- background for an explicit title card

At least 80% of the final runtime should be made from moving video clips.

### 6. Voice and Captions

Voice style:

- Calm but tense.
- Documentary narrator, not exaggerated movie trailer.

Captions:

- Burned-in Chinese captions.
- 7-12 Chinese characters per line.
- Highlight only one key phrase per scene.

### 7. Assembly

MVP assembly in CapCut/Jianying:

- 9:16 project.
- 60-90 seconds.
- 8-12 moving video shots, usually 3-6 seconds each.
- 1 voiceover track.
- 1 low-volume BGM.
- Captions.
- Cover frame.

Shot rule:

Do not try to generate one continuous 60-90 second AI video. Generate short cinematic shots and cut them together like a film:

```text
shot 01: 3-4s establishing shot
shot 02: 4-5s ruler close-up
shot 03: 3-5s minister reaction
shot 04: 3-5s object/map/edict
shot 05: 4-6s argument escalation
shot 06: 4-6s decision moment
shot 07: 3-5s consequence
shot 08: 3-4s final question
```

Automation assembly:

- Codex prepares assets and names.
- FFmpeg checks video duration, resolution, bitrate, loudness, and creates platform copies.
- Remotion comes later when the CapCut template is stable.

### 8. Quality Gate

Do not publish unless all are true:

- Video is 1080x1920 or platform-ready vertical.
- No captions are cut off.
- No AI image has broken hands, wrong clothing, modern objects, or fake Chinese characters.
- No AI video has obvious broken motion, warped faces, drifting costumes, extra limbs, or modern objects.
- Historical claim is not presented as certainty unless sourced.
- Title is clear in 8 Chinese characters or fewer when possible.
- First 3 seconds contain conflict.
- Final 5 seconds invites comment.

### 9. Publish Package

Each video gets one package:

```text
title:
description:
hashtags:
cover:
platform_versions:
  youtube_shorts:
  tiktok:
  douyin:
  xiaohongshu:
  instagram_reels:
disclosure:
  contains_ai_images: true
  contains_synthetic_voice: true/false
```

### 10. Analytics Loop

Track after 24h, 72h, 7d:

- Views.
- Hook retention if available.
- Average watch time.
- Completion rate.
- Likes.
- Comments.
- Shares.
- Saves.
- New followers.
- Best comment.
- Next episode idea.

Decision rules:

- If completion is weak, shorten intro and cut one shot.
- If comments are strong, make a sequel.
- If saves are strong, make more factual/educational episodes.
- If shares are strong, lean into emotional conflict.

## Automation Roadmap

Phase 1: Manual MVP

- Codex creates folders, scripts, prompts, publish packages.
- GPT Image 2 creates covers and first-frame references.
- AI video tools create moving clips from those references.
- CapCut/Jianying assembles final edit.
- Manual upload or semi-auto upload.

Phase 2: Assisted Production

- One command generates episode folder, storyboard, image prompts, voice script, caption draft, and publish copy.
- FFmpeg validates exports and creates platform-specific files.
- YouTube upload can be automated after OAuth/API setup.

Phase 3: Publishing Hub

- Local dashboard or Notion/Airtable status board.
- Buttons: generate assets, render draft, export package, upload to supported platforms.
- Unsupported platforms open the right upload page and prefill copy where possible.

Phase 4: Feedback Engine

- Pull analytics where APIs allow.
- Rank episodes by retention and engagement.
- Suggest next 10 scripts based on winners.

## Budget

MVP budget for 10 videos:

- GPT Image 2: set a cap of $20-$60 for image generation drafts and finals.
- Text/script/research model use: $5-$30 depending on depth.
- Voice: $0-$30 if using built-in/low-cost TTS, more for premium voice.
- CapCut/Jianying: use existing plan first; budget $0-$20 if extra features are needed.
- Stock music/assets: $0-$50; avoid paid assets in the first experiment if possible.
- Video generation: optional. If using Sora 2, official pricing lists 720p at $0.10/second standard or $0.05/second batch. Use only for 3-5 second inserts at first.

Recommended first experiment cap:

**$100 total for 10 videos**, excluding subscriptions you already pay for.

Do not spend on ads until the workflow is stable.

## The First One-Click Target

Do not try to make "one click to every platform" first. It will break your flow because each platform has different API approval, metadata rules, and AI disclosure requirements.

Build this instead:

**One click to create a publish package.**

That package contains final video, cover, title, description, hashtags, disclosure text, and platform variants. Then automate YouTube first, TikTok second, and keep Douyin/Xiaohongshu semi-manual until the account and API path are clear.

## Episode 1 Draft

Title:

**焚书前夜**

Hook:

如果你是秦始皇，天下刚统一，所有读书人却还在引用旧制度反驳你。你会让他们继续说，还是让所有声音闭嘴？

Conflict:

这不是一个关于书的决定，而是一个关于帝国能不能只有一个大脑的决定。

Beat outline:

1. Dark palace, maps on the table.
2. Ministers argue about old books and old states.
3. Qin Shi Huang looks at the empire map.
4. Li Si presents the control argument.
5. Flames begin, but the camera stays on the ruler's face.
6. Narrator asks: a unified empire needs统一思想, or can it survive disagreement?

Comment bait:

如果你坐在那个位置，你会烧书，禁言，还是放任争论？

## Operating Rule

One video can be imperfect. A broken workflow cannot.

The first season exists to learn the machine.
