import json
import random
from pathlib import Path
from typing import List, Dict, Any
from config.settings import PROCESSED_DATA_DIR, AUDIT_SAMPLE_RATIO
from utils.logger import logger

class PhysicianAuditor:
    """Trích xuất 10-15% mẫu ngẫu nhiên xuất ra file cho Bác sĩ / Chuyên gia Y tế kiểm định thủ công."""

    @staticmethod
    def extract_audit_sample(
        dataset: List[Dict[str, Any]],
        ratio: float = AUDIT_SAMPLE_RATIO,
        output_filename: str = "audit_sample_15pct.json",
        seed: int = 42
    ) -> Path:
        random.seed(seed)
        shuffled = list(dataset)
        random.shuffle(shuffled)

        sample_size = max(1, int(len(shuffled) * ratio))
        audit_samples = shuffled[:sample_size]

        # Format thân thiện cho bác sĩ đọc review
        doctor_friendly_list = []
        for idx, entry in enumerate(audit_samples, 1):
            messages = entry.get("messages", [])
            doctor_friendly_list.append({
                "stt": idx,
                "cau_hoi_benh_nhan": messages[1]["content"] if len(messages) > 1 else "",
                "cau_tra_loi_ai": messages[2]["content"] if len(messages) > 2 else "",
                "flags": entry.get("metadata", {}).get("safety_flags", {}),
                "bac_si_review": {
                    "y_khoa_chinh_xac": "ĐẠT / KHÔNG ĐẠT",
                    "co_red_flag_chua": "CÓ / KHÔNG / N/A",
                    "nhat_xet": ""
                }
            })

        output_path = PROCESSED_DATA_DIR / output_filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(doctor_friendly_list, f, ensure_ascii=False, indent=2)

        logger.info(f"[AUDIT EXPORT] Đã xuất {len(audit_samples)} mẫu audit ({ratio * 100:.0f}%) cho Bác sĩ tại: {output_path}")
        return output_path
