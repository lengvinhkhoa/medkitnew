import re
from typing import Dict, Any, Tuple
from config.red_flags_keywords import (
    RED_FLAGS_KEYWORDS,
    MEDICATION_KEYWORDS,
    EMERGENCY_DISCLAIMER,
    MEDICATION_DISCLAIMER,
    AMBIGUOUS_QUESTION_GUIDANCE
)
from utils.logger import logger

class SafetyEngine:
    """Hệ thống kiểm soát và gán nhãn an toàn dữ liệu Y Tế."""

    @staticmethod
    def process_qa_safety(question: str, answer: str, seed_meta: Dict[str, Any] = None) -> Tuple[str, str, Dict[str, bool]]:
        """
        Phân tích và điều chỉnh nội dung theo các quy tắc bắt buộc:
        1. Red Flags -> Chỉ gán cho triệu chứng thực sự NGUY CẤP từ phía bệnh nhân.
        2. Thuốc / Liều dùng -> Thận trọng, khuyến cáo hỏi dược sĩ/bác sĩ.
        3. Mơ hồ / Thiếu thông tin -> Hỏi lại người dùng thay vì đoán bừa.
        """
        seed_meta = seed_meta or {}
        
        flags = {
            "is_red_flag": seed_meta.get("is_red_flag", False),
            "is_medication": seed_meta.get("is_medication", False),
            "is_ambiguous": seed_meta.get("is_ambiguous", False)
        }

        q_lower = question.lower()
        a_lower = answer.lower()

        # 1. Kiểm tra Red Flags CHỈ từ CÂU HỎI BỆNH NHÂN (không soi câu trả lời tránh dán nhầm vào sốt nhẹ 38.5)
        if not flags["is_red_flag"]:
            # Chỉ các triệu chứng cực kỳ nguy cấp xuất hiện trong câu hỏi bệnh nhân
            critical_q_keywords = [
                "thở ngáp", "tím tái", "co giật mắt trợn", "méo miệng", "nói ngọng",
                "yếu nửa người", "đau thắt ngực", "vã mồ hôi hột", "nôn ra máu", 
                "phân đen như bã cà phê", "bụng cứng như gỗ", "đau đầu dữ dội chưa từng có",
                "huyết áp 170", "huyết áp 180"
            ]
            for kw in critical_q_keywords:
                if kw in q_lower:
                    flags["is_red_flag"] = True
                    break

        # 2. Kiểm tra câu hỏi Thuốc
        if not flags["is_medication"]:
            for kw in MEDICATION_KEYWORDS:
                if kw in q_lower:
                    flags["is_medication"] = True
                    break

        # 3. Kiểm tra câu hỏi Mơ hồ (Ambiguous)
        if not flags["is_ambiguous"]:
            # Nếu câu hỏi quá ngắn hoặc thiếu thông tin lâm sàng
            if len(question.strip()) < 35 or re.search(r"\b(uống thuốc gì|làm sao bác sĩ|bôi thuốc gì|có sao không)\b", q_lower):
                # ngoại trừ câu đã có thông tin chi tiết
                if not any(k in q_lower for k in ["sốt 3", "tháng", "tuổi", "đau thắt ngực", "méo miệng"]):
                    flags["is_ambiguous"] = True

        # Tùy chỉnh câu trả lời (Assistant Output) để đảm bảo tuân thủ tuyệt đối
        processed_answer = answer

        if flags["is_red_flag"]:
            if "cấp cứu" not in a_lower and "115" not in a_lower:
                processed_answer += EMERGENCY_DISCLAIMER

        if flags["is_medication"]:
            if "dược sĩ" not in a_lower and "chỉ định" not in a_lower:
                processed_answer += MEDICATION_DISCLAIMER

        if flags["is_ambiguous"]:
            if "hỏi thêm" not in a_lower and "chia sẻ thêm" not in a_lower and "chi tiết" not in a_lower:
                processed_answer += AMBIGUOUS_QUESTION_GUIDANCE

        return question, processed_answer, flags
