import json
from pathlib import Path
from typing import List, Dict, Any
from config.settings import DEFAULT_SYSTEM_PROMPT, PROCESSED_DATA_DIR
from processors.cleaner import TextCleaner
from processors.safety_filter import SafetyEngine
from utils.logger import logger

class DataFormatter:
    """Chuyển đổi dữ liệu Y tế đã làm sạch sang định dạng JSONL tiêu chuẩn của Gemma 4 e2b."""

    def __init__(self, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        self.system_prompt = system_prompt

    def format_to_gemma_messages(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Biến đổi danh sách cặp Hỏi-Đáp thô thành chuẩn `messages` Chat Format."""
        formatted_dataset = []

        for item in raw_items:
            q_raw = item.get("question", "")
            a_raw = item.get("answer", "")

            # 1. Làm sạch văn bản
            q_clean = TextCleaner.format_question(q_raw)
            a_clean = TextCleaner.format_answer(a_raw)

            if not q_clean or not a_clean or len(q_clean) < 5 or len(a_clean) < 15:
                continue

            # 2. Xử lý An toàn Y tế & Red Flags
            question, answer, safety_flags = SafetyEngine.process_qa_safety(q_clean, a_clean)

            # 3. Đóng gói cấu trúc Messages
            message_entry = {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": answer}
                ],
                "metadata": {
                    "source": item.get("source", "unknown"),
                    "url": item.get("url", ""),
                    "safety_flags": safety_flags
                }
            }
            formatted_dataset.append(message_entry)

        logger.info(f"Đã định dạng thành công {len(formatted_dataset)} mẫu dữ liệu chuẩn Gemma 4 e2b.")
        return formatted_dataset

    def export_to_jsonl(self, dataset: List[Dict[str, Any]], filename: str = "patient_medical_dataset.jsonl") -> Path:
        """Xuất file .jsonl hoàn chỉnh để đưa vào huấn luyện Fine-tune."""
        output_path = PROCESSED_DATA_DIR / filename
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in dataset:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        logger.info(f"[SUCCESS] ĐÃ XUẤT DATASET BỆNH NHÂN THÀNH CÔNG: {output_path}")
        return output_path
