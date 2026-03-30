import re

def clean_text(text):
    if not text:
        return ""

    # 1. Normalize newlines first
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n+', '\n', text)

    # 2. Remove extra spaces (but preserve structure)
    text = re.sub(r'[ \t]+', ' ', text)

    # 3. Remove weird invisible characters
    text = re.sub(r'[\x00-\x1f\x7f]', '', text)

    # 4. Trim
    text = text.strip()

    return text