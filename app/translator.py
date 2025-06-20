# app/translator.py

import os
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
from loguru import logger
import torch

# Set model name (multilingual to English)
MODEL_NAME = "Helsinki-NLP/opus-mt-mul-en"

# -------------------------
# Load MarianMT Translation Model
# -------------------------
def load_translation_model():
    try:
        tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
        model = MarianMTModel.from_pretrained(MODEL_NAME)
        model.eval()
        logger.info(f"✅ Loaded MarianMT model: {MODEL_NAME}")
        return tokenizer, model
    except Exception as e:
        logger.error(f"❌ Failed to load translation model: {e}")
        return None, None

# Load model once at module level
tokenizer, model = load_translation_model()

# -------------------------
# Language Detection
# -------------------------
def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        logger.debug(f"Detected language: {lang}")
        return lang
    except Exception as e:
        logger.error(f"⚠️ Language detection failed: {e}")
        return "unknown"

# -------------------------
# Translate any non-English text to English
# -------------------------
def translate_to_english(text: str) -> str:
    if not model or not tokenizer:
        logger.warning("⚠️ Translation model not available. Returning original text.")
        return text

    detected_lang = detect_language(text)
    if detected_lang == "en":
        logger.debug("Skipping translation: already in English.")
        return text

    try:
        # Tokenize and translate in inference mode
        with torch.no_grad():
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            output_tokens = model.generate(**inputs, max_length=512, num_beams=4)
            translated = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

        logger.info(f"🌍 Translated [{detected_lang}] → [en]")
        return translated

    except Exception as e:
        logger.error(f"❌ Translation failed: {e}")
        return text  # Fallback to original
