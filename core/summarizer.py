import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import string

nltk.download('punkt')

class Summarizer:
    def __init__(self):
        pass

    def summarize(self, text, max_sentences=3):
        sentences = sent_tokenize(text)
        if len(sentences) <= max_sentences:
            return text

        words = word_tokenize(text.lower())
        words = [w for w in words if w not in string.punctuation]

        freq = Counter(words)
        ranked_sentences = sorted(
            sentences,
            key=lambda s: sum(freq.get(w.lower(), 0) for w in word_tokenize(s)),
            reverse=True
        )

        summary = " ".join(ranked_sentences[:max_sentences])
        return summary
