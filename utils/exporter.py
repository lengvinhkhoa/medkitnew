import json
from pathlib import Path
from typing import Dict, Any, List
from utils.logger import logger

class DatasetValidator:
    """Kiểm tra tính hợp lệ và thống kê chất lượng của Dataset Fine-tuning."""

    @staticmethod
    def validate_and_summarize(jsonl_path: Path) -> Dict[str, Any]:
        if not jsonl_path.exists():
            logger.error(f"Tệp không tồn tại: {jsonl_path}")
            return {}

        total_samples = 0
        red_flag_count = 0
        medication_count = 0
        ambiguous_count = 0
        valid_structure_count = 0

        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                total_samples += 1
                try:
                    data = json.loads(line)
                    messages = data.get("messages", [])
                    if len(messages) == 3 and messages[0]["role"] == "system" and messages[1]["role"] == "user" and messages[2]["role"] == "assistant":
                        valid_structure_count += 1

                    metadata = data.get("metadata", {})
                    flags = metadata.get("safety_flags", {})
                    if flags.get("is_red_flag"):
                        red_flag_count += 1
                    if flags.get("is_medication"):
                        medication_count += 1
                    if flags.get("is_ambiguous"):
                        ambiguous_count += 1
                except Exception as e:
                    logger.warning(f"Dòng {total_samples} bị lỗi định dạng: {e}")

        summary = {
            "file_path": str(jsonl_path),
            "total_samples": total_samples,
            "valid_gemma_schema_samples": valid_structure_count,
            "red_flag_cases": red_flag_count,
            "medication_cases": medication_count,
            "ambiguous_cases": ambiguous_count
        }

        logger.info("=== BÁO CÁO CHẤT LƯỢNG DATASET HUẤN LUYỆN ===")
        logger.info(f"Tổng số mẫu: {total_samples}")
        logger.info(f"Chuẩn định dạng Gemma 4 e2b: {valid_structure_count}/{total_samples}")
        logger.info(f"Số mẫu Red Flags (Cấp cứu): {red_flag_count}")
        logger.info(f"Số mẫu Hỏi Thuốc: {medication_count}")
        logger.info(f"Số mẫu Mơ hồ (Cần hỏi lại): {ambiguous_count}")
        logger.info("==========================================")

        return summary
