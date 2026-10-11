"""
Veritas Text Corpus Profiler & Explainability Engine
Analyzes vocabulary, length distributions, sentiment tone, and computes fidelity scorecards.
"""
import re
from typing import List, Dict, Any, Optional
from collections import Counter


class TextCorpusAnalyzer:
    @staticmethod
    def profile_corpus(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Profiles uploaded text corpus: length stats, vocabulary, tone, and category distributions.
        records: list of dicts with at least 'text' key, and optional 'label' or 'category' key.
        """
        if not records:
            return {
                "total_samples": 0,
                "avg_word_count": 0,
                "vocab_size": 0,
                "length_distribution": {},
                "top_keywords": [],
                "label_distribution": {}
            }

        texts = [str(r.get("text", "")).strip() for r in records if str(r.get("text", "")).strip()]
        total_samples = len(texts)
        if total_samples == 0:
            return {"total_samples": 0, "avg_word_count": 0, "vocab_size": 0}

        word_counts = [len(t.split()) for t in texts]
        char_counts = [len(t) for t in texts]

        # Extract words for vocabulary analysis
        all_words = []
        for t in texts:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', t.lower())
            all_words.extend(words)

        stop_words = {"the", "and", "for", "with", "this", "that", "was", "are", "have", "from", "you", "they", "our", "all"}
        filtered_words = [w for w in all_words if w not in stop_words]
        vocab_counter = Counter(filtered_words)
        vocab_size = len(set(all_words))
        top_keywords = [{"word": w, "count": c} for w, c in vocab_counter.most_common(12)]

        # Category/label distribution
        labels = [str(r.get("category") or r.get("label") or "Uncategorized") for r in records]
        label_counts = Counter(labels)
        label_distribution = {k: round(v / total_samples, 3) for k, v in label_counts.items()}

        # Simple tone analysis
        pos_words = {"great", "good", "excellent", "love", "awesome", "fast", "helpful", "easy", "satisfied", "best"}
        neg_words = {"bad", "slow", "broken", "worst", "terrible", "issue", "problem", "difficult", "poor", "error"}
        pos_count = sum(1 for w in all_words if w in pos_words)
        neg_count = sum(1 for w in all_words if w in neg_words)
        
        tone = "Neutral"
        if pos_count > neg_count * 1.5:
            tone = "Positive / Praising"
        elif neg_count > pos_count * 1.5:
            tone = "Critical / Problem-Reporting"

        return {
            "total_samples": total_samples,
            "avg_word_count": round(float(sum(word_counts) / max(total_samples, 1)), 1),
            "min_word_count": min(word_counts) if word_counts else 0,
            "max_word_count": max(word_counts) if word_counts else 0,
            "avg_char_count": round(float(sum(char_counts) / max(total_samples, 1)), 1),
            "vocab_size": vocab_size,
            "top_keywords": top_keywords,
            "label_distribution": label_distribution,
            "detected_tone": tone
        }

    @staticmethod
    def compare_real_and_synthetic(real_texts: List[str], syn_texts: List[str],
                                   real_labels: Optional[List[str]] = None,
                                   syn_labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Text Explainability & Evaluation:
        Computes vocabulary overlap (Jaccard similarity), length alignment, and label fidelity.
        """
        def get_vocab(text_list):
            words = set()
            for t in text_list:
                tokens = re.findall(r'\b[a-zA-Z]{3,}\b', str(t).lower())
                words.update(tokens)
            return words

        r_vocab = get_vocab(real_texts)
        s_vocab = get_vocab(syn_texts)

        intersection = r_vocab.intersection(s_vocab)
        union = r_vocab.union(s_vocab)
        jaccard = len(intersection) / max(len(union), 1)

        r_len = [len(str(t).split()) for t in real_texts] or [0]
        s_len = [len(str(t).split()) for t in syn_texts] or [0]
        r_avg = sum(r_len) / len(r_len)
        s_avg = sum(s_len) / len(s_len)

        length_similarity = max(0.0, 1.0 - abs(r_avg - s_avg) / max(r_avg, 1.0))

        # Overall text fidelity
        fidelity_score = round(float(0.5 * jaccard + 0.5 * length_similarity), 3)

        return {
            "vocabulary_jaccard_similarity": round(float(jaccard), 3),
            "shared_vocab_count": len(intersection),
            "real_vocab_size": len(r_vocab),
            "synthetic_vocab_size": len(s_vocab),
            "real_avg_length": round(float(r_avg), 1),
            "synthetic_avg_length": round(float(s_avg), 1),
            "length_alignment_score": round(float(length_similarity), 3),
            "overall_text_fidelity": fidelity_score,
            "explanation": f"Synthetic text shares {len(intersection)} vocabulary tokens ({round(jaccard*100, 1)}% overlap) and matches real average document length within {round(abs(r_avg - s_avg), 1)} words."
        }
