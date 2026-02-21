# Audio Demos Feature Design

**Date:** 2026-02-21
**Status:** Approved

## Overview

Add audio demo samples to MayariWEB to showcase the Kokoro TTS voices, similar to paper2audio.com.

## Components

### 1. Hero Audio Player
- Location: Hero section, below tagline, above download buttons
- Content: Single audio player with Emma (best) voice sample
- Implementation: Native HTML5 `<audio>` element

### 2. Voice Showcase Section
- Location: New section after TTS features (#tts)
- Content: Grid of 8 voice cards with audio samples
- Layout: 4-col desktop, 2-col tablet, 1-col mobile

## Voices

| Voice | Gender | Description |
|-------|--------|-------------|
| Emma | F | Best quality, warm and clear |
| Isabella | F | Expressive, gentle |
| Alice | F | Bright, youthful |
| Lily | F | Soft, calming |
| George | M | Authoritative, deep |
| Fable | M | Storyteller, engaging |
| Lewis | M | Professional, neutral |
| Daniel | M | Friendly, conversational |

## File Structure

```
MayariWEB/
├── audio/
│   ├── sample-emma.mp3
│   ├── sample-isabella.mp3
│   ├── sample-alice.mp3
│   ├── sample-lily.mp3
│   ├── sample-george.mp3
│   ├── sample-fable.mp3
│   ├── sample-lewis.mp3
│   └── sample-daniel.mp3
└── index.html (updated)
```

## Sample Text

"Welcome to Mayari. Transform your PDFs into audiobooks with natural-sounding British voices."
