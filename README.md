# CineForge • Sci-Fi Text2Video & Storyboard Studio 🎬🪐

An AI-powered multi-modal cinematic studio that transforms ideas into in-universe sci-fi screenplays, matching concept art, synchronized neural voiceovers, scrolling HUD subtitles, and downloadable animated video clips (`.webm` / `.mp4`).

Built for the **[Pollinations.ai](https://pollinations.ai)** ecosystem and unified API.

---

## ✨ Features

- **Rich Worldbuilding Lore Engine (StellarForge Lore Format)**:
  - Generates categorized in-universe sector coordinates, threat/tech class, and **2-3 vivid paragraphs of expedition worldbuilding logs** using `openai/gpt-5.4-nano`.
  - Full formatted archive dossier with copyable expedition reports.
- **Visual Storyboard Panels (1 or 2 Images)**:
  - **1 Image**: Single continuous cinematic shot with Ken Burns camera dynamics (zoom/pan).
  - **2 Images (Dual Scene Storyboard)**: Generates both Panel 1 (Establishing Exterior / Inception) and Panel 2 (Interior / Anomaly Core Reveal), seamlessly stitched together in-browser with a smooth cinematic 50% midpoint cross-fade dissolve transition and synchronized dual-panel HUD telemetry.
- **Concept Art Visual Synthesis**:
  - Renders photorealistic visuals matching the story using the **FLUX** model on Pollinations across custom aspect ratios (16:9, 9:16, 1:1, compact).
- **Quad-Audio Engine (Local & Cloud)**:
  - 🖥️ **Local Native Kokoro-ONNX (Offline CPU)**: Zero cloud cost, running on your CPU via `local_kokoro_server.py`. Accesses all 50 voices (`af_sarah`, `am_adam`, `af_nicole`, `am_michael`, `af_bella`, `am_fenrir`) with zero API balance needed!
  - ⚡ **Pollinations Cloud Kokoro (`hexgrad/kokoro-82m`)**: Official Pollinations cloud TTS endpoint when Paid Pollen is available.
  - 🎵 **Cinematic Soundscape Synthesizer (16-bit PCM WAV)**: Built-in client-side Web Audio engine generating deep cosmic sub-bass drones and telemetry pulses embedded directly into the video!
  - 📁 **Custom Audio File Loader**: Upload any `.mp3` or `.wav` voice file from your computer to automatically sync and embed into the video!
  - 🔊 **Direct Web Speech Narration**: One-click audible readout of the full screenplay story using the browser's speech synthesis.
- **Sci-Fi HUD Subtitles**: Real-time dialogue ticker with mission telemetry, timestamps, scanlines, and targeting reticles.
- **In-Browser Video Stitching**: Generates cinematic Ken Burns camera motion (Slow Zoom-In, Dramatic Zoom-Out, Pan Right, Pan Left) composited with subtitles and stereo voiceover into a high-definition video.
- **Aspect Ratios**:
  - Landscape 16:9 (`1024×576` & `512×384`)
  - Portrait 9:16 (`576×1024` & `384×512`)
  - Square 1:1 (`512×512`)
- **Zero-Install Client Deployment**: The frontend is 100% pure HTML5/CSS3/Vanilla JS and can deploy directly to GitHub Pages for the Pollinations App Directory!

---

## 🚀 Quick Start (Local with Native Kokoro)

1. Start the local Kokoro-ONNX speech server:
   ```bash
   cd /home/jack/Desktop/POLINATIONS/text2video_generator
   python3 local_kokoro_server.py
   ```
2. Open [`index.html`](index.html) in your web browser.
3. The app will auto-detect the local server and show:
   `● LOCAL KOKORO: ONLINE (PORT 5050)`
4. Enter any sci-fi concept, pick your voice actor, and click **FORGE TEXT2VIDEO**!

---

## 🌐 GitHub Pages Deployment (Pollinations Submission)

1. Push this directory to your GitHub account:
   ```bash
   git remote add origin git@github.com:JupyterJones/text2video_generator.git
   git push -u origin main
   ```
2. Enable **GitHub Pages** under repository *Settings -> Pages -> Deploy from branch `main`*.
3. Live URL: **`https://jupyterjones.github.io/text2video_generator/`**

---

## 🛠️ Technology & Attribution

- **Backend AI Provider**: [Pollinations.ai](https://gen.pollinations.ai)
  - **Screenplay & Worldbuilding**: `openai/gpt-5.4-nano` on `/v1/chat/completions`
  - **Concept Art**: `flux` on `/image/{prompt}`
  - **Audio Synthesis**: Native Kokoro-ONNX + `hexgrad/kokoro-82m` on `/audio/{prompt}` + Web Audio PCM Synthesizer
  - **Video Engine**: HTML5 Canvas + Web Audio Destination + MediaStream Recording API
- **Author**: Jack Northrup ([@JupyterJones](https://github.com/JupyterJones))
- **License**: MIT
