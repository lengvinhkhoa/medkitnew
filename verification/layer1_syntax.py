from typing import Dict, Any, Tuple

class Layer1SyntaxVerifier:
    """Lớp 1: Kiểm tra cấu trúc Cú pháp, Schema JSON, Mã hóa UTF-8 và Độ dài câu."""

    @staticmethod
    def verify(entry: Dict[str, Any]) -> Tuple[bool, str]:
        if not isinstance(entry, dict):
            return False, "Lỗi Lớp 1: Mẫu dữ liệu không phải là JSON Object hợp lệ."

        messages = entry.get("messages")
        if not messages or not isinstance(messages, list):
            return False, "Lỗi Lớp 1: Thiếu trường 'messages' hoặc không phải danh sách."

        if len(messages) != 3:
            return False, f"Lỗi Lớp 1: Trường 'messages' phải có đúng 3 phần tử (Role: system, user, assistant), hiện tại có {len(messages)} phần tử."

        roles = [m.get("role") for m in messages if isinstance(m, dict)]
        if roles != ["system", "user", "assistant"]:
            return False, f"Lỗi Lớp 1: Thứ tự role không chuẩn ['system', 'user', 'assistant']. Hiện tại: {roles}"

        system_content = messages[0].get("content", "").strip()
        user_content = messages[1].get("content", "").strip()
        assistant_content = messages[2].get("content", "").strip()

        if not system_content or not user_content or not assistant_content:
            return False, "Lỗi Lớp 1: Tồn tại nội dung tin nhắn rỗng."

        if len(user_content) < 10:
            return False, f"Lỗi Lớp 1: Câu hỏi user quá ngắn ({len(user_content)} ký tự < 10 ký tự)."

        if len(assistant_content) < 30:
            return False, f"Lỗi Lớp 1: Câu trả lời assistant quá ngắn ({len(assistant_content)} ký tự < 30 ký tự)."

        return True, "PASSED"
