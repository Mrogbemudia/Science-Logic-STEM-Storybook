# 📚 Illustrated Cultural & STEM Storybook Generator

An automated, modular Python pipeline that transforms complex STEM concepts (such as Algorithmic If/Else Logic or Solar Photovoltaics) into culturally relatable, multi-sensory African stories designed for primary school students (ages 7–10).

Built as a capstone project, this application combines **Chain-of-Thought (CoT) LLM reasoning**, **Pydantic schema enforcement**, **dynamic image generation with style anchoring**, **multilingual neural voice narration**, and **print-ready PDF compilation** into both an interactive Streamlit web application and a CLI orchestrator.

---

## 🚀 Key Technical Features

1. **Chain-of-Thought (CoT) Story Decomposition:**
   - Leverages Gemini to bridge abstract STEM principles with everyday cultural analogies (e.g., mapping conditional branching logic to grandmother grading and sorting harvested yams).
2. **Strict Schema & Reading-Level Validation:**
   - Uses Pydantic to guarantee strict JSON schema compliance.
   - Includes `utils/validators.py` to programmatically inspect sentences and enforce a strict **12-word per sentence primary school reading limit**.
3. **Character-Consistent & Dynamically Seeded Illustrations:**
   - Employs global art style anchoring (*vector art children book illustration, vibrant warm African color palette*) and immutable character sheets.
   - Utilizes unique per-page seeds (`base_seed + page_number`) with exponential backoff retries and fallback asset handling to ensure distinct visual storytelling without network failures.
4. **Natural African Neural Audio Narration:**
   - Integrated via `edge-tts` to generate natural MP3 voice narrations across multiple African English accents (Nigerian, Kenyan, South African) with independent audio stream handling.
5. **Print-Ready PDF Storybook Compilation:**
   - Assembles structured text and generated illustrations into a landscape A4, print-ready PDF using `FPDF2` and `Pillow`.
6. **Interactive Streamlit Web Interface:**
   - Provides sidebar topic presets, custom overrides, voice selection, real-time generation status, page-by-page audio players, and one-click PDF downloads.

---

## 📂 Project Architecture & File Tree

```text
cultural-stem-storybook/
│
├── app.py                      # Interactive Streamlit web application dashboard
├── main.py                     # Command-line orchestrator script
├── requirements.txt            # Python package dependencies
├── .env                        # Environment variables (Gemini API key)
│
├── schemas/
│   └── storybook.py            # Pydantic data schemas for validation & structuring
│
├── services/
│   ├── llm_service.py          # Gemini LLM service for CoT reasoning & story generation
│   ├── image_service.py        # Pollinations.ai image generator with retries & fallback
│   ├── audio_service.py        # edge-tts multilingual neural voice narration service
│   └── pdf_compiler.py         # FPDF2 & Pillow print-ready storybook PDF compiler
│
├── utils/
│   └── validators.py           # Reading-level checker (enforces 12-word sentence limit)
│
├── assets/
│   └── placeholder.png         # Fallback image asset for network safety
│
└── output/
    ├── images/                 # Generated page illustrations (.png)
    ├── audio/                  # Generated voice narrations (.mp3)
    └── books/                  # Compiled printable PDF storybooks (.pdf)
