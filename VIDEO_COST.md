# CineForge • Video Generation Cost & Pollen Economics 💰🎬

A complete economic and unit-cost guide for generating multi-modal sci-fi text-to-video dispatches using the **[Pollinations.ai](https://pollinations.ai)** ecosystem.

---

## 🪙 Currency & Economy Fundamentals

- **The Currency**: Pollinations uses **Pollen** as its internal unit of exchange.
- **Conversion Rate**:
  $$\mathbf{1\text{ Pollen} = \$1.00\text{ USD}}$$
- **Fractional Credits**: Fractions of Pollen map directly to cents and sub-cents:
  - `0.0100 Pollen = $0.01` (1 cent)
  - `0.0010 Pollen = $0.001` (1/10th of a cent)
  - `0.0001 Pollen = $0.0001` (1/100th of a cent)
- **Credit Expiration**: Purchased Pollen **never expires**.
- **Tier Pollen vs. Paid Pollen**:
  - **Tier Pollen (Earned)**: Free pollen awarded via community quests or daily usage.
  - **Paid Pollen (Purchased)**: Credits bought via credit card/Stripe.
  - *Important*: Certain premium endpoints (such as cloud audio TTS) require at least a non-zero **Paid Pollen** balance (`paid_only: true`).

---

## 📋 Live Model Pricing Table

Live unit pricing queried directly from the Pollinations unified API:

| Pipeline Step | Provider / Model | Modality | Rate / Unit | Pricing Type |
| :--- | :--- | :--- | :--- | :--- |
| **1. Screenplay & Lore** | `openai/gpt-5.4-nano` | Text LLM | `0.00000015 Pollen` / input token<br>`0.0000009375 Pollen` / output token | Token-based |
| **2. Concept Art** | `black-forest-labs/flux.1-schnell` | Image (FLUX) | `0.0020 Pollen` / image | Flat rate |
| **3. Cloud Voice** | `hexgrad/kokoro-82m` | Neural Audio | `0.00000062 Pollen` / audio token | Token-based (`paid_only`) |
| **3. Local Voice** | `local_kokoro_server.py` | CPU Audio | **$0.0000** | Free offline |
| **3. Audio Synth** | Built-in Web Audio PCM | Soundscape | **$0.0000** | Free browser |
| **4. Subtitles HUD** | Dynamic Canvas Ticker | Typography | **$0.0000** | Free browser |
| **5. Video Stitching** | HTML5 Canvas + MediaRecorder | Video Engine | **$0.0000** | Free browser |

---

## 🎬 Total Cost Per Video Scenarios

### Scenario A: Full Cloud (1 Image • Single Continuous Shot)
*Uses Pollinations GPT-5.4-nano, 1 FLUX concept art image, and Cloud Kokoro audio (~20s narration).*

| Item | Calculation | Cost (Pollen / USD) |
| :--- | :--- | :--- |
| Story & Screenplay | ~350 prompt & completion tokens | `~$0.0003` |
| Concept Art (1 Image) | 1 × `0.0020 Pollen` | `$0.0020` |
| Cloud Kokoro Audio | ~1,200 audio tokens (~20s speech) | `~$0.0008` |
| Video Stitching & Subtitles | Client-side Canvas rendering | `$0.0000` |
| **Total Cost Per Video** | | **`~0.0031 Pollen` (~$0.0031 USD)** |

> [!NOTE]
> That is less than **one-third of a single penny (0.31¢)** per video!

---

### Scenario B: Full Cloud (2 Images • Dual Storyboard with Dissolve)
*Uses Pollinations GPT-5.4-nano, 2 FLUX concept art images (Exterior & Interior Reveal), and Cloud Kokoro audio (~25s narration).*

| Item | Calculation | Cost (Pollen / USD) |
| :--- | :--- | :--- |
| Story & Screenplay | ~450 prompt & completion tokens | `~$0.0004` |
| Concept Art (2 Images) | 2 × `0.0020 Pollen` | `$0.0040` |
| Cloud Kokoro Audio | ~1,500 audio tokens (~25s speech) | `~$0.0010` |
| Video Stitching & Subtitles | Client-side Canvas rendering | `$0.0000` |
| **Total Cost Per Video** | | **`~0.0054 Pollen` (~$0.0054 USD)** |

> [!NOTE]
> Roughly **half a penny (0.54¢)** for a complete 2-scene storyboard video with dissolve transitions.

---

### Scenario C: Hybrid Mode (Pollinations FLUX + Local CPU Kokoro)
*Uses Pollinations FLUX for concept art, but runs [`local_kokoro_server.py`](file:///home/jack/Desktop/POLINATIONS/text2video_generator/local_kokoro_server.py) on your AMD Ryzen CPU.*

| Item | Calculation | Cost (Pollen / USD) |
| :--- | :--- | :--- |
| Story & Screenplay | Free tier / `gpt-5.4-nano` | `~$0.0003` |
| Concept Art (1 Image) | 1 × `0.0020 Pollen` | `$0.0020` |
| Local Kokoro-ONNX | Native CPU execution | **$0.0000** |
| Video Stitching & Subtitles | Client-side Canvas rendering | **$0.0000** |
| **Total Cost Per Video** | | **`~0.0023 Pollen` (~$0.0023 USD)** |

> [!TIP]
> **No Paid Pollen required!** Hybrid mode allows you to generate videos even if your account has $0.00 in purchased credits.

---

### Scenario D: Zero Cloud Audio (Built-in Synth or Custom Audio File)
*Uses Pollinations for images and story, with built-in Web Audio PCM soundscape or your own uploaded voice recording.*

| Item | Calculation | Cost (Pollen / USD) |
| :--- | :--- | :--- |
| Concept Art (1 Image) | 1 × `0.0020 Pollen` | `$0.0020` |
| Audio Engine | In-browser synthesizer / uploaded MP3 | **$0.0000** |
| **Total Cost Per Video** | | **`~$0.0023 USD`** |

---

## 📈 Purchasing Power: What Does Your Budget Buy?

Because the costs are a fraction of a cent per video, modest balances produce massive generation volumes:

| Deposit / Balance | Full Cloud (1 Image) | Full Cloud (2 Images) | Hybrid (Local Kokoro) |
| :--- | :--- | :--- | :--- |
| **$1.00 (1.0 Pollen)** | **~320 Videos** | **~185 Videos** | **~435 Videos** |
| **$5.00 (5.0 Pollen)** | **~1,600 Videos** | **~925 Videos** | **~2,170 Videos** |
| **$10.00 (10.0 Pollen)** | **~3,200 Videos** | **~1,850 Videos** | **~4,340 Videos** |

---

## 💡 Cost-Optimization Guidelines

1. **Use Local Kokoro For Development**:
   - Keep `local_kokoro_server.py` running locally while experimenting with story pacing, prompts, and aspect ratios. You will burn zero audio credits.
2. **Batch Image Selection**:
   - Start with **1 Image** when exploring concepts. Switch to **2 Images** once you find a lore scenario you want to develop into a dual-scene cinematic storyboard.
3. **Aspect Ratio Agnostic**:
   - On Pollinations, `16:9`, `9:16`, and `1:1` images cost the exact same flat rate (`0.002 Pollen`).
