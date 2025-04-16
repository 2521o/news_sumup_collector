from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect

# Initialisation des modèles
models = {
    "fr": {
        "name": "moussaKam/barthez-orangesum-abstract",
        "tokenizer": None,
        "model": None,
    },
    "en": {
        "name": "sshleifer/distilbart-cnn-12-6",
        "tokenizer": None,
        "model": None,
    }
}

def load_model(lang_code):
    if models[lang_code]["model"] is None:
        print(f"🔄 Loading model for {lang_code}...")
        models[lang_code]["tokenizer"] = AutoTokenizer.from_pretrained(models[lang_code]["name"])
        models[lang_code]["model"] = AutoModelForSeq2SeqLM.from_pretrained(models[lang_code]["name"])

def summarize_article(text: str) -> str:
    lang = detect(text)
    lang_code = "fr" if lang == "fr" else "en"
    
    load_model(lang_code)

    tokenizer = models[lang_code]["tokenizer"]
    model = models[lang_code]["model"]

    # Préparation du texte
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, early_stopping=True)
    
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
