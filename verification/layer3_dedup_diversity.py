import re
from typing import List, Dict, Any, Tuple, Set

class Layer3DeduplicationVerifier:
    """Lớp 3: Kiểm tra Trùng lặp (Fuzzy Deduplication) và Đa dạng Mẫu câu (Pattern Diversity)."""

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.seen_question_word_sets: List[Set[str]] = []

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        words = re.findall(r"\w+", text.lower())
        return set(words)

    @staticmethod
    def _jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def verify_entry(self, entry: Dict[str, Any]) -> Tuple[bool, str]:
        messages = entry.get("messages", [])
        if len(messages) < 2:
            return False, "Lỗi Lớp 3: Thiếu câu hỏi user."

        user_q = messages[1].get("content", "")
        q_words = self._tokenize(user_q)

        # Check trùng lặp fuzzy với các câu hỏi đã duyệt qua trước đó
        for existing_words in self.seen_question_word_sets:
            sim = self._jaccard_similarity(q_words, existing_words)
            if sim >= self.similarity_threshold:
                return False, f"Lỗi Lớp 3 [Fuzzy Duplicate]: Câu hỏi có độ tương đồng quá cao ({sim:.2%}) với mẫu khác trong dataset."

        self.seen_question_word_sets.append(q_words)
        return True, "PASSED"

    def reset(self):
        self.seen_question_word_sets.clear()
