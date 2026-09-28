# Kokoro-ONNX Local Speech Server 🎙️

A lightweight, zero-cost, high-speed neural Text-to-Speech (TTS) micro-server built specifically for **CineForge Text2Video & Storyboard Studio**.

It serves native Kokoro TTS on CPU over HTTP (`http://127.0.0.1:5050`), enabling unlimited voiceover synthesis without requiring paid cloud API credits.

```
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

---

## 📌 Why This Server Exists

1. **Pollinations Cloud Credit Constraint**:
   - Pollinations splits pollen balances into **Tier** (free earned pollen from quests/usage) and **Paid** (purchased pollen).
   - Cloud TTS endpoints (`hexgrad/kokoro-82m`, ElevenLabs, etc.) are strictly marked `paid_only: true`.
   - Accounts with earned tier pollen will receive HTTP `402 Payment Required` when requesting cloud voice generation.
2. **Local CPU Autonomy**:
   - Running `kokoro-onnx` directly on the local machine provides instant, 100% free neural speech synthesis with all 50 Kokoro voice personas.
3. **Graceful Hybrid Fallback**:
   - The CineForge web application ([`index.html`](file:///home/jack/Desktop/POLINATIONS/text2video_generator/index.html)) automatically pings this server on launch. If running, it uses local neural voiceover; if offline, it seamlessly falls back to the built-in Web Audio synthesizer.

---

## ⚙️ Architecture & Hardware Guardrails

[`local_kokoro_server.py`](file:///home/jack/Desktop/POLINATIONS/text2video_generator/local_kokoro_server.py) is intentionally designed without heavy server frameworks like Flask or FastAPI to remain ultra-lean, fast, and free of dependency conflicts:

- **Standard Library HTTP Server**: Built on Python's native `http.server.HTTPServer` and `BaseHTTPRequestHandler`.
- **CORS Enabled**: Configured with `Access-Control-Allow-Origin: *` so client-side JavaScript running in the browser can query the server directly.
- **Hardware Throttling Guard**:
  - `os.nice(15)`: Automatically lowers OS process priority so background synthesis never stutters the browser UI or desktop environment.
  - `torch.set_num_threads(2)`: Restricts PyTorch thread concurrency to 2 CPU cores, keeping CPU temps cool and avoiding system hangs.
- **Instant Clean Exit**:
  - Captures `SIGINT` (Ctrl+C) and `SIGTERM` with `os._exit(0)`, closing socket bindings immediately without leaving orphaned processes.

---

## 🧠 Model Discovery & Weights

The server automatically scans known project directories for Kokoro ONNX model and voice embedding binaries:

| Asset | Scanned File Paths |
| :--- | :--- |
| **ONNX Model** (`kokoro-v1.0.onnx`) | `/home/jack/Desktop/Media_Studio/models/kokoro/kokoro-v1.0.onnx`<br>`/home/jack/Desktop/Kokoro-TTS-Pause/kokoro-v1.0.onnx`<br>`/home/jack/Desktop/StaacorUtilities/kokoro-v1.0.onnx` |
| **Voices Bin** (`voices-v1.0.bin`) | `/home/jack/Desktop/Media_Studio/models/kokoro/voices-v1.0.bin`<br>`/home/jack/Desktop/Media_Studio/models/kokoro/voices.bin` |

---

## 🧹 Markdown & Asterisk Speech Sanitizer

When LLMs output formatted story dossiers, they often include bold formatting or bullet markers (e.g. `**Field report:**` or `*Sector 4*`). Standard TTS models will literally pronounce these as *"asterisk, asterisk"*.

[`local_kokoro_server.py`](file:///home/jack/Desktop/POLINATIONS/text2video_generator/local_kokoro_server.py) includes a built-in pre-processing sanitizer:
- Strips bold/italic markers (`**`, `*`, `_`).
- Strips markdown headers (`#`), code ticks (`` ` ``), and bracket tags.
- Removes list bullet points (`-`, `•`, `+`).
- Normalizes excess whitespace into clean conversational English before synthesis.

---

## 📡 REST API Reference

The server listens on **`http://127.0.0.1:5050`**.

### 1. Health Check
Checks if the local server and ONNX runtime are ready.

- **Endpoint**: `GET /health`
- **Response**:
  ```json
  {
    "status": "ok",
    "engine": "kokoro-onnx-cpu"
  }
  ```

### 2. Available Voices List
Lists all 50 embedded voice personas available in the weights file.

- **Endpoint**: `GET /api/voices`
- **Response**:
  ```json
  ["af_sarah", "af_nicole", "af_bella", "am_adam", "am_michael", "am_fenrir", ...]
  ```

### 3. Speech Synthesis (TTS)
Synthesizes speech from text and returns standard 16-bit PCM WAV audio.

- **Endpoint**: `GET /api/tts` (or `GET /audio`)
- **Query Parameters**:
  - `text` (required): The narrative text or dossier to speak.
  - `voice` (optional, default: `af_sarah`): Kokoro voice identifier.
  - `speed` (optional, default: `1.0`): Speech pace multiplier (e.g. `0.95` for cinematic slow, `1.1` for fast).
- **Response Headers**:
  - `Content-Type: audio/wav`
  - `Content-Length: <byte_count>`
- **Response Body**: Binary 16-bit PCM WAV audio.

---

## 🚀 Running the Server

### Starting the Server
From the terminal:
```bash
cd /home/jack/Desktop/POLINATIONS/text2video_generator
python3 local_kokoro_server.py
```

Console output:
```text
✓ Found model: /home/jack/Desktop/Media_Studio/models/kokoro/kokoro-v1.0.onnx
✓ Found voices: /home/jack/Desktop/Media_Studio/models/kokoro/voices-v1.0.bin
⏳ Loading Kokoro-ONNX model into memory...
✓ Kokoro ONNX ready! (50 voices available)

🚀 Kokoro TTS Server live at: http://127.0.0.1:5050
👉 Health check: http://127.0.0.1:5050/health
👉 Synthesis API: http://127.0.0.1:5050/api/tts?text=Hello&voice=af_sarah
```

### Testing with cURL
Verify health:
```bash
curl -s http://127.0.0.1:5050/health
```

Generate a test audio sample:
```bash
curl -G "http://127.0.0.1:5050/api/tts" \
  --data-urlencode "text=Exploration vessel telemetry confirmed. Orbiting anomaly." \
  --data-urlencode "voice=af_sarah" \
  --data-urlencode "speed=0.95" \
  -o test_narration.wav
```

---

## 🔗 Integration with CineForge Frontend

In [`index.html`](file:///home/jack/Desktop/POLINATIONS/text2video_generator/index.html):
1. **Auto-Detection (`checkLocalKokoro`)**:
   On page load, the frontend sends a `fetch("http://127.0.0.1:5050/health")`. If HTTP 200 is received, the header status badge updates to:
   `● LOCAL KOKORO: ONLINE (PORT 5050)`
2. **Director Controls**:
   The audio engine automatically defaults to `🖥️ Local Kokoro (CPU)` with voice selection (`af_sarah`, `am_adam`, `af_nicole`, `am_michael`, `af_bella`, `am_fenrir`).
3. **Video Audio Embedding**:
   The generated WAV audio is passed to Web Audio's `createMediaStreamDestination()` and mixed directly into the canvas `MediaRecorder` stream, producing `.webm` videos with embedded voice narration.
