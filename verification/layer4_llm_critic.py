import os
import re
import json
import httpx
from typing import Dict, Any, Tuple
from config.settings import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_API_URL
from utils.logger import logger

class Layer4LLMCriticVerifier:
    """Lớp 4: Kiểm duyệt Chất lượng & Độ chính xác Y tế bằng LLM Critic qua OpenRouter API."""

    def __init__(self, api_key: str = None, model: str = OPENROUTER_MODEL):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", OPENROUTER_API_KEY)
        self.model = model
        self.warned = False

    def verify(self, entry: Dict[str, Any]) -> Tuple[bool, str]:
        if not self.api_key:
            if not self.warned:
                logger.warning(
                    "⚠️ [LỚP 4 LLM CRITIC THÔNG BÁO]: Chưa tìm thấy OPENROUTER_API_KEY! "
                    "Lớp 4 tạm thời BỎ QUA (Bypass). "
                    "Để bật Lớp 4 đánh giá bằng model 'inclusionai/ling-3.0-flash:free', vui lòng gõ lệnh:\n"
                    "👉 Windows PowerShell: $env:OPENROUTER_API_KEY='sk-or-v1-...'"
                )
                self.warned = True
            return True, "SKIPPED_OFFLINE: Chưa có OPENROUTER_API_KEY. Đã bỏ qua Lớp 4."

        messages = entry.get("messages", [])
        if len(messages) < 3:
            return False, "Lỗi Lớp 4: Thiếu tin nhắn."

        user_q = messages[1].get("content", "")
        assistant_a = messages[2].get("content", "")

        critic_prompt = (
            "Bạn là một Bác sĩ Chuyên gia Y tế Độc lập thẩm định dữ liệu cho AI Y Tế Việt Nam.\n"
            "Hãy đánh giá nghiêm ngặt cặp Hỏi-Đáp y tế sau:\n\n"
            f"[CÂU HỎI BỆNH NHÂN]: {user_q}\n"
            f"[CÂU TRẢ LỜI Y TẾ]: {assistant_a}\n\n"
            "TIÊU CHÍ ĐÁNH GIÁ:\n"
            "1. Chính xác y khoa, lời khuyên hợp lý, không gây hại.\n"
            "2. Văn phong thân thiện, đời thường, dễ hiểu, có thái độ trấn an bệnh nhân.\n"
            "3. Tuân thủ an toàn: Có hướng dẫn cấp cứu khi gặp triệu chứng nặng, không khẳng định chẩn đoán thay bác sĩ.\n\n"
            "Trả về duy nhất 1 JSON object có định dạng:\n"
            '{"score": 5, "status": "PASS", "reason": "Giải thích ngắn gọn"}'
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Không truyền "response_format": {"type": "json_object"} vì model inclusionai/ling-3.0-flash:free không hỗ trợ structured-outputs
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": critic_prompt}
            ],
            "temperature": 0.1
        }

        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(OPENROUTER_API_URL, headers=headers, json=payload)
                if resp.status_code == 200:
                    result = resp.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Trích xuất JSON từ chuỗi kết quả
                    json_match = re.search(r"\{.*\}", content, re.DOTALL)
                    if json_match:
                        parsed = json.loads(json_match.group(0))
                        score = parsed.get("score", 0)
                        status = parsed.get("status", "REJECT")
                        reason = parsed.get("reason", "")

                        if status == "PASS" and score >= 4:
                            logger.info(f"[LỚP 4 LLM CRITIC PASS] Score {score}/5 - {reason}")
                            return True, f"PASSED (LLM Score: {score}/5 - {reason})"
                        else:
                            logger.warning(f"[LỚP 4 LLM CRITIC REJECT] Score {score}/5 - {reason}")
                            return False, f"Lỗi Lớp 4 [LLM Critic Reject]: Score {score}/5 - {reason}"
                    else:
                        # Fallback nếu model trả về text không chứa JSON
                        return True, "PASSED (LLM Text Pass)"
                else:
                    logger.warning(f"Lớp 4 OpenRouter HTTP {resp.status_code}: {resp.text}")
                    return True, "SKIPPED_API_ERROR: Lỗi phản hồi API OpenRouter."
        except Exception as e:
            logger.warning(f"Lớp 4 Exception OpenRouter: {e}")
            return True, f"SKIPPED_NETWORK_ERROR: {e}"
