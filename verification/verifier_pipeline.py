from typing import List, Dict, Any
from verification.layer1_syntax import Layer1SyntaxVerifier
from verification.layer2_safety_rules import Layer2SafetyVerifier
from verification.layer3_dedup_diversity import Layer3DeduplicationVerifier
from verification.layer4_llm_critic import Layer4LLMCriticVerifier
from utils.logger import logger

class MedicalDataVerifierPipeline:
    """Bộ Kiểm Duyệt 4 Lớp Hoàn Chỉnh Cho Dataset Y Tế."""

    def __init__(self, enable_llm_critic: bool = False):
        self.layer1 = Layer1SyntaxVerifier()
        self.layer2 = Layer2SafetyVerifier()
        self.layer3 = Layer3DeduplicationVerifier()
        self.layer4 = Layer4LLMCriticVerifier() if enable_llm_critic else None

    def run_pipeline(self, raw_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        passed_dataset = []
        rejected_items = []
        self.layer3.reset()

        stats = {
            "total_input": len(raw_dataset),
            "passed_count": 0,
            "layer1_rejected": 0,
            "layer2_rejected": 0,
            "layer3_rejected": 0,
            "layer4_rejected": 0,
        }

        logger.info(f"=== BẮT ĐẦU CHẠY BỘ VERIFY 4 LỚP (Tổng số: {len(raw_dataset)} mẫu) ===")

        for idx, entry in enumerate(raw_dataset):
            # Lớp 1: Cấu trúc & Syntax
            ok1, msg1 = self.layer1.verify(entry)
            if not ok1:
                stats["layer1_rejected"] += 1
                rejected_items.append({"index": idx, "reason": msg1, "data": entry})
                continue

            # Lớp 2: Quy tắc Y tế & Red Flags
            ok2, msg2 = self.layer2.verify(entry)
            if not ok2:
                stats["layer2_rejected"] += 1
                rejected_items.append({"index": idx, "reason": msg2, "data": entry})
                continue

            # Lớp 3: Trùng lặp & Đa dạng Mẫu câu
            ok3, msg3 = self.layer3.verify_entry(entry)
            if not ok3:
                stats["layer3_rejected"] += 1
                rejected_items.append({"index": idx, "reason": msg3, "data": entry})
                continue

            # Lớp 4: LLM Critic
            if self.layer4:
                ok4, msg4 = self.layer4.verify(entry)
                if not ok4:
                    stats["layer4_rejected"] += 1
                    rejected_items.append({"index": idx, "reason": msg4, "data": entry})
                    continue

            # Nếu vượt qua cả 4 Lớp
            passed_dataset.append(entry)

        stats["passed_count"] = len(passed_dataset)

        logger.info(f"=== BÁO CÁO KẾT QUẢ BỘ VERIFY 4 LỚP ===")
        logger.info(f"Đã duyệt ĐẠT: {stats['passed_count']}/{stats['total_input']} mẫu")
        logger.info(f"Loại ở Lớp 1 (Cấu trúc): {stats['layer1_rejected']}")
        logger.info(f"Loại ở Lớp 2 (An toàn y tế/Red Flag): {stats['layer2_rejected']}")
        logger.info(f"Loại ở Lớp 3 (Trùng lặp/Diversity): {stats['layer3_rejected']}")
        logger.info(f"Loại ở Lớp 4 (LLM Critic): {stats['layer4_rejected']}")
        logger.info("=========================================")

        return {
            "passed_dataset": passed_dataset,
            "rejected_items": rejected_items,
            "stats": stats
        }
