import re
from typing import Dict, Any, Tuple
from config.red_flags_keywords import RED_FLAGS_KEYWORDS, MEDICATION_KEYWORDS

class Layer2SafetyVerifier:
    """Lớp 2: Kiểm tra Quy tắc An toàn Y tế & Logic Văn phong Tự nhiên."""

    @staticmethod
    def verify(entry: Dict[str, Any]) -> Tuple[bool, str]:
        messages = entry.get("messages", [])
        if len(messages) < 3:
            return False, "Lỗi Lớp 2: Thiếu dữ liệu tin nhắn."

        user_q = messages[1].get("content", "").lower()
        assistant_a = messages[2].get("content", "").lower()

        # 0. Kiểm tra Logic phi lý y khoa (Nonsensical Medical Mismatch)
        # Ví dụ: "Bé 5 tháng" + "thức khuya làm việc căng thẳng"
        if re.search(r"(bé|trẻ|cháu\s*\d|con em\s*\d)\s*.*(thức khuya|làm việc|uống rượu|bia|đột quỵ|méo miệng)", user_q):
            return False, "Lỗi Lớp 2 [Medical Mismatch]: Đối tượng trẻ em nhưng lại ghép với triệu chứng/ngữ cảnh người lớn (thức khuya/làm việc/đột quỵ)."

        # Ví dụ: "Bố 60 tuổi / Bà 75 tuổi" + "bỏ bú / thóp phồng"
        if re.search(r"(bố|mẹ|bà|ông|cụ)\s*.*(bỏ bú|thóp phồng|mọc răng|sốt co giật ở trẻ)", user_q):
            return False, "Lỗi Lớp 2 [Medical Mismatch]: Đối tượng người lớn nhưng lại ghép triệu chứng trẻ em (bỏ bú/thóp phồng)."

        # Kiểm tra trùng lặp mâu thuẫn đối tượng (VD: "Vợ em 30 tuổi bà nội em 75 tuổi")
        pronouns_found = re.findall(r"(vợ em|chồng em|bà nội|bố em|mẹ em|bé\s*\d|cháu\s*\d|em sinh viên)", user_q)
        if len(set(pronouns_found)) > 1:
            return False, f"Lỗi Lớp 2 [Contradictory Subjects]: Câu hỏi ghép mâu thuẫn nhiều đối tượng khác nhau ({pronouns_found})."

        # 1. Bắt buộc cảnh báo Cấp cứu 115 khi chứa Red Flags
        is_red_flag_in_q = any(kw in user_q for kw in RED_FLAGS_KEYWORDS)
        if is_red_flag_in_q:
            has_emergency_notice = any(term in assistant_a for term in ["115", "cấp cứu", "khám ngay", "bệnh viện ngay", "cơ sở y tế"])
            if not has_emergency_notice:
                return False, "Lỗi Lớp 2 [Red Flag Violation]: Câu hỏi chứa triệu chứng cấp cứu nhưng câu trả lời không có cảnh báo Cấp cứu 115 hoặc Đi khám ngay."

        # 2. Thận trọng với Thuốc & Liều dùng
        is_med_in_q = any(kw in user_q for kw in MEDICATION_KEYWORDS)
        if is_med_in_q:
            has_med_caution = any(term in assistant_a for term in ["dược sĩ", "bác sĩ", "chỉ định", "kê đơn", "tham khảo", "tự ý"])
            if not has_med_caution:
                return False, "Lỗi Lớp 2 [Medication Caution Missing]: Câu hỏi về thuốc nhưng câu trả lời không có khuyến cáo tham khảo ý kiến Bác sĩ/Dược sĩ."

        # 3. Không đưa ra chẩn đoán khẳng định tuyệt đối thay bác sĩ
        dangerous_claims = ["chắc chắn bạn bị", "khẳng định 100%", "bạn đã bị ung thư", "không cần đi khám"]
        for claim in dangerous_claims:
            if claim in assistant_a:
                return False, f"Lỗi Lớp 2 [Dangerous Medical Claim]: Câu trả lời chứa phát ngôn chẩn đoán bừa bãi: '{claim}'."

        return True, "PASSED"
