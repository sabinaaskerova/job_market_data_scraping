import json
import spacy
from collections import defaultdict
from langdetect import detect
import re
from company import Company

# Load spaCy models for English and French
nlp_models = {
    "en": spacy.load("en_core_web_sm"),
    "fr": spacy.load("fr_core_news_sm")
}

def detect_language(text):
    """Detect the language of the text."""
    try:
        return detect(text)
    except:
        return None

def extract_entities(text, language):
    """Extract entities using spaCy's NER model."""
    nlp = nlp_models.get(language)
    if not nlp:
        return defaultdict(list)  # Return empty if language not supported

    doc = nlp(text)
    extracted = defaultdict(list)

    for ent in doc.ents:
        # Categorize entities of interest
        if ent.label_ in {"ORG"} and ent.text not in extracted["organizations"]:
            extracted["organizations"].append(ent.text)
        elif ent.label_ in {"GPE"} and ent.text not in extracted["locations"]:
            extracted["locations"].append(ent.text)
        elif ent.label_ in {"PERSON"} and ent.text not in extracted["people"]:
            extracted["people"].append(ent.text)
        # # I tried to train a skills extraction NER model, but couldn't do it. Maybe let this as an indication for further improvement.
        # elif ent.label_ in {"SKILL"} and ent.text not in extracted["skills"]:  # Custom skill identification
        #     extracted["skills"].append(ent.text)
    return extracted

def process_company_entry(company, get_text_blocks: bool = True):
    """Process a single company entry with advanced NER extraction."""
    sector = str(company.get("sector"))

    sector = [s.strip() for s in re.split(r'[;,/]', sector) if s.strip()]

    company["sector"] = sector

    if get_text_blocks:
        text_blocks = company.get("text_blocks", {})

        for block_key, block_content in text_blocks.items():
            if not block_content or \
                not block_key in ["Presentation", "What they are looking for", "Good to know"]:
                continue

            language = detect_language(block_content)

            company[f"Language"] = language

            if language not in {"en", "fr"}:
                continue  # Skip unsupported languages

            # entities = extract_entities(block_content, language)

            # # Add extracted entities to the company data
            # company[f"{block_key}_entities"] = entities

    return company

# Process JSON file incrementally
input_file = "data/company_data.json"
output_file = "data/cleaned_company_data.json"

# Load JSON file
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

processed_data = []

for id, company in enumerate(data):
    company = Company(company)
    company['id'] = id

    if company['name'] is not None:
        processed_entry = process_company_entry(company)
        processed_data.append(processed_entry)

processed_data = list(set(processed_data))

# Save the cleaned JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)

print(f"Processing completed. Data written to {output_file}.")
