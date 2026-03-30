import re

def split_into_sentences(text):
    """
    Basic sentence splitter using regex.
    Handles ., ?, ! as sentence boundaries.
    """
    if not text:
        return []

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Split sentences
    sentences = re.split(r'(?<=[.?!])\s+', text)

    # Clean sentences
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences


def create_chunks(sentences, max_words=300, overlap_sentences=2):
    """
    Create chunks from sentences with overlap.
    """
    chunks = []
    current_chunk = []
    current_word_count = 0
    chunk_id = 1

    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        word_count = len(sentence.split())

        # If adding this sentence exceeds limit → finalize chunk
        if current_word_count + word_count > max_words and current_chunk:
            chunk_text = " ".join(current_chunk)

            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text
            })

            chunk_id += 1

            # 🔥 Overlap logic
            overlap_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
            current_chunk = overlap_chunk.copy()
            current_word_count = sum(len(s.split()) for s in current_chunk)

        else:
            current_chunk.append(sentence)
            current_word_count += word_count
            i += 1

    # Add last chunk
    if current_chunk:
        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(current_chunk)
        })

    return chunks


def chunk_text(text, max_words=300, overlap_sentences=2):
    """
    Main function to generate chunks.
    """
    if not text:
        return []

    sentences = split_into_sentences(text)

    # Edge case: very small text
    if len(sentences) <= 1:
        return [{
            "chunk_id": 1,
            "text": text.strip()
        }]

    chunks = create_chunks(sentences, max_words, overlap_sentences)

    return chunks


