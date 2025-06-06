import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect
from utils.logger import get_logger

log_handler = get_logger(__name__)
load_dotenv()

model_name_fr = os.getenv("MODEL_FR")
model_name_en = os.getenv("MODEL_EN")

if not model_name_fr or not model_name_en:
    log_handler.error("Model names are not set in the .env file.")
    raise ValueError("MODEL_FR and MODEL_EN must be defined in the environment")

# Models init
models = {
    "fr": {
        "name": model_name_fr,
        "tokenizer": None,
        "model": None,
    },
    "en": {
        "name": model_name_en,
        "tokenizer": None,
        "model": None,
    }
}


def load_model(lang_code):
    
    log_handler.info("Loading model for %s", lang_code)
    if models[lang_code]["model"] is None:
        models[lang_code]["tokenizer"] = AutoTokenizer.from_pretrained(models[lang_code]["name"])
        models[lang_code]["model"] = AutoModelForSeq2SeqLM.from_pretrained(models[lang_code]["name"])

def summarize_article(text: str) -> str:
    
    log_handler.info("Starting summarization process")
    lang = detect(text)
    lang_code = "fr" if lang == "fr" else "en"
    log_handler.info("Detected language: %s", lang_code)
    load_model(lang_code)

    tokenizer = models[lang_code]["tokenizer"]
    model = models[lang_code]["model"]

    # Text preparation
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=400, early_stopping=False)
    log_handler.info("Summarization completed")
    
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
