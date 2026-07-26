import random
from typing import List, Dict, Any
from utils.logger import logger

PRONOUN_VARIATIONS = [
    ("em", "ạ"),
    ("cháu", "dạ"),
    ("tôi", "cho tôi hỏi"),
    ("mình", "ad cho mình hỏi"),
    ("bác sĩ cho em hỏi", "với ạ"),
]

AGE_DEMOGRAPHICS = [
    "Con em 2 tuổi",
    "Bố em 65 tuổi",
    "Mẹ em 55 tuổi",
    "Bé nhà em 8 tháng tuổi",
    "Bà nội em 72 tuổi",
]

class SeedAugmentor:
    """Tạo biến thể tự nhiên (Augmentation) từ Seed Cases để mở rộng dataset mà không làm đổi nghĩa y khoa."""

    @staticmethod
    def augment_seed_case(seed_item: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
        messages = seed_item.get("messages", [])
        if len(messages) < 3:
            return [seed_item]

        user_q = messages[1]["content"]
        assistant_a = messages[2]["content"]
        system_p = messages[0]["content"]

        augmented_list = [seed_item]

        for i in range(count):
            p1, p2 = PRONOUN_VARIATIONS[i % len(PRONOUN_VARIATIONS)]
            # Đổi biến thể xưng hô
            new_q = user_q
            if "em" in new_q:
                new_q = new_q.replace("em", p1)
            elif "tôi" in new_q:
                new_q = new_q.replace("tôi", p1)

            if not new_q.endswith("ạ?") and not new_q.endswith("ạ"):
                new_q += f" {p2}?"

            aug_entry = {
                "messages": [
                    {"role": "system", "content": system_p},
                    {"role": "user", "content": new_q},
                    {"role": "assistant", "content": assistant_a}
                ],
                "metadata": {
                    "source": "augmented_seed",
                    "original_url": seed_item.get("metadata", {}).get("url", ""),
                    "safety_flags": seed_item.get("metadata", {}).get("safety_flags", {})
                }
            }
            augmented_list.append(aug_entry)

        return augmented_list
