#!/usr/bin/env python3
"""
🎙️ Local Kokoro-ONNX Speech Server for CineForge Text2Video Studio
Serves zero-cost, high-speed neural TTS on CPU for the CineForge web app.

Complies with TEMPLATE.md constraints:
- Hardware throttling guard: os.nice(15) + torch.set_num_threads(2)
- Fast SIGINT/SIGTERM exit: os._exit(0)
- CORS enabled for seamless in-browser fetch from index.html
"""

import os
import sys
import io
import signal
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Throttling Guard & Signal Handling ---
try:
    os.nice(15)
except Exception:
    pass

def sig_handler(sig, frame):
    print("\n[Kokoro Server] Shutting down cleanly.")
    os._exit(0)

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)

try:
    import torch
    torch.set_num_threads(2)
except Exception:
    pass

# --- Model Paths ---
MODEL_PATHS = [
    "/home/jack/Desktop/Media_Studio/models/kokoro/kokoro-v1.0.onnx",
    "/home/jack/Desktop/Kokoro-TTS-Pause/kokoro-v1.0.onnx",
    "/home/jack/Desktop/StaacorUtilities/kokoro-v1.0.onnx"
]

VOICE_PATHS = [
    "/home/jack/Desktop/Media_Studio/models/kokoro/voices-v1.0.bin",
    "/home/jack/Desktop/Media_Studio/models/kokoro/voices.bin"
]

model_path = next((p for p in MODEL_PATHS if os.path.exists(p)), None)
voice_path = next((p for p in VOICE_PATHS if os.path.exists(p)), None)

if not model_path or not voice_path:
    print(f"❌ Error: Kokoro model or voices file not found in known locations.")
    sys.exit(1)

print(f"✓ Found model: {model_path}")
print(f"✓ Found voices: {voice_path}")

try:
    import kokoro_onnx
    import soundfile as sf
    print("⏳ Loading Kokoro-ONNX model into memory...")
    kokoro = kokoro_onnx.Kokoro(model_path, voice_path)
    voices = kokoro.get_voices()
    print(f"✓ Kokoro ONNX ready! ({len(voices)} voices available)")
except Exception as e:
    print(f"❌ Failed to initialize Kokoro ONNX: {e}")
    sys.exit(1)

# --- HTTP Request Handler ---
PORT = 5050

class KokoroHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Range')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/health":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","engine":"kokoro-onnx-cpu"}')
            return

        if parsed.path == "/api/voices":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(str(voices).replace("'", '"').encode('utf-8'))
            return

        if parsed.path in ["/api/tts", "/audio"]:
            params = urllib.parse.parse_qs(parsed.query)
            text = params.get('text', [''])[0].strip()
            voice = params.get('voice', ['af_sarah'])[0].strip()
            speed = float(params.get('speed', ['1.0'])[0])

            if not text:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error":"Missing text parameter"}')
                return

            import re
            # Clean markdown formatting so Kokoro never speaks 'asterisk' or symbols
            text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
            text = text.replace('*', '').replace('#', '').replace('`', '').replace('[', '').replace(']', '')
            text = re.sub(r'^\s*[-•+]\s+', '', text, flags=re.MULTILINE)
            text = re.sub(r'\s+', ' ', text).strip()

            print(f"🎙️ [Kokoro TTS] Voice: {voice} | Speed: {speed} | Text: {text[:60]}...")

            try:
                samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
                
                # Write to in-memory WAV
                buf = io.BytesIO()
                sf.write(buf, samples, sample_rate, format='WAV', subtype='PCM_16')
                wav_bytes = buf.getvalue()

                self.send_response(200)
                self.send_header('Content-Type', 'audio/wav')
                self.send_header('Content-Length', str(len(wav_bytes)))
                self.end_headers()
                self.wfile.write(wav_bytes)
                print(f"✓ Delivered {len(wav_bytes)} bytes WAV ({len(samples)/sample_rate:.2f}s)")
            except Exception as err:
                print(f"❌ Synthesis error: {err}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'{{"error":"{str(err)}"}}'.encode('utf-8'))
            return

        # Default fallback
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]} - {args[1]}\n")

def run():
    server = HTTPServer(('127.0.0.1', PORT), KokoroHandler)
    print(f"\n🚀 Kokoro TTS Server live at: http://127.0.0.1:{PORT}")
    print(f"👉 Health check: http://127.0.0.1:{PORT}/health")
    print(f"👉 Synthesis API: http://127.0.0.1:{PORT}/api/tts?text=Hello&voice=af_sarah\n")
    server.serve_forever()

if __name__ == '__main__':
    run()
