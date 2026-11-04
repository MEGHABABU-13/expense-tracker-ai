import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.5-flash-lite"
CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education",
    "Other",
]
FALLBACK = "Uncategorized"

client = genai.Client()
_cache = {}


def _ask_gemini(description):
    prompt = (
        "Classify this expense into exactly one of these categories: "
        + ", ".join(CATEGORIES)
        + ". Reply with the category name only, nothing else.\n"
        + f"Expense: {description}"
    )
    for attempt in range(3):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text or ""
        except Exception as error:
            print(f"Gemini attempt {attempt + 1} failed: {str(error)[:120]}")
            if "429" in str(error):
                break
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
    return ""


def _validate(text):
    words = text.replace("*", " ").split()
    if not words:
        return FALLBACK
    first_word = words[0].strip(".,:;").lower()
    for category in CATEGORIES:
        if first_word == category.lower():
            return category
    return FALLBACK


def categorize(description):
    key = description.strip().lower()
    if key in _cache:
        return _cache[key]
    category = _validate(_ask_gemini(description))
    if category != FALLBACK:
        _cache[key] = category
    return category