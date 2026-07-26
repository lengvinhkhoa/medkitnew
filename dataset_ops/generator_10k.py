import json
import random
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

from config.settings import PROCESSED_DATA_DIR, DEFAULT_SYSTEM_PROMPT
from dataset_ops.seed_medical_kb import SEED_MEDICAL_DATABASE
from processors.cleaner import TextCleaner
from processors.safety_filter import SafetyEngine
from verification.verifier_pipeline import MedicalDataVerifierPipeline
from dataset_ops.splitter import DatasetSplitter
from dataset_ops.auditor import PhysicianAuditor
from utils.logger import logger

# Nhóm Phân Tầng Đối Tượng Y Tế Đồng Bộ Tuổi (Tuples: demo_title, age_str, demo_ref)
PEDIATRIC_DEMOGRAPHICS = [
    ("Bé 1 tuổi", "1 tuổi", "bé 1 tuổi"),
    ("Con em 8 tháng tuổi", "8 tháng tuổi", "bé 8 tháng tuổi"),
    ("Trẻ 3 tuổi", "3 tuổi", "trẻ 3 tuổi"),
    ("Cháu 14 tháng", "14 tháng", "cháu 14 tháng"),
    ("Bé nhà em 5 tháng", "5 tháng", "bé 5 tháng"),
    ("Con em 4 tuổi", "4 tuổi", "bé 4 tuổi"),
    ("Bé 18 tháng", "18 tháng", "bé 18 tháng"),
    ("Cháu 6 tháng", "6 tháng", "bé 6 tháng"),
    ("Bé 2 tuổi", "2 tuổi", "bé 2 tuổi"),
    ("Con gái 3 tuổi", "3 tuổi", "bé 3 tuổi"),
    ("Con trai 5 tuổi", "5 tuổi", "bé 5 tuổi"),
    ("Bé sơ sinh 2 tháng", "2 tháng", "bé 2 tháng")
]

SENIOR_DEMOGRAPHICS = [
    ("Bố em 60 tuổi", "60 tuổi", "người 60 tuổi"),
    ("Bà nội em 75 tuổi", "75 tuổi", "người 75 tuổi"),
    ("Mẹ em 62 tuổi", "62 tuổi", "người 62 tuổi"),
    ("Bác gái 50 tuổi", "50 tuổi", "người 50 tuổi"),
    ("Cụ 80 tuổi", "80 tuổi", "người cao tuổi 80 tuổi"),
    ("Ông ngoại 72 tuổi", "72 tuổi", "người 72 tuổi"),
    ("Bà ngoại 68 tuổi", "68 tuổi", "người 68 tuổi"),
    ("Cụ ông 82 tuổi", "82 tuổi", "người cao tuổi 82 tuổi")
]

ADULT_DEMOGRAPHICS = [
    ("Em 24 tuổi", "24 tuổi", "bệnh nhân 24 tuổi"),
    ("Chồng em 35 tuổi", "35 tuổi", "người 35 tuổi"),
    ("Vợ em 30 tuổi", "30 tuổi", "người 30 tuổi"),
    ("Anh trai 28 tuổi", "28 tuổi", "người 28 tuổi"),
    ("Chị gái 32 tuổi", "32 tuổi", "người 32 tuổi"),
    ("Mình 27 tuổi", "27 tuổi", "bệnh nhân 27 tuổi"),
    ("Tôi 40 tuổi", "40 tuổi", "bệnh nhân 40 tuổi"),
    ("Em sinh viên 20 tuổi", "20 tuổi", "bệnh nhân 20 tuổi")
]

FEMALE_DEMOGRAPHICS = [
    ("Vợ em 28 tuổi", "28 tuổi", "chị 28 tuổi"),
    ("Chị gái em 30 tuổi", "30 tuổi", "chị 30 tuổi"),
    ("Em 25 tuổi", "25 tuổi", "chị 25 tuổi"),
    ("Chị em 32 tuổi", "32 tuổi", "chị 32 tuổi"),
    ("Cháu gái 22 tuổi", "22 tuổi", "chị 22 tuổi")
]

VARIATION_PREFIXES = [
    "Dạ bác sĩ cho em hỏi", "Chào bác sĩ", "Ad cho mình thắc mắc xíu ạ",
    "Bác sĩ tư vấn giúp em với", "Mọi người cho em hỏi xíu", "Dạ em xin hỏi bác sĩ",
    "Dạ cho cháu hỏi xíu ạ", "Chào bác sĩ tư vấn", "Dạ ad ơi cho em hỏi",
    "Xin chào bác sĩ", "Thưa bác sĩ chuyên khoa", "Chào ad cho em xin thông tin",
    "Bác sĩ cho tôi hỏi", "Dạ thưa bác sĩ", "Dạ em chào bác sĩ"
]

CONVERSATIONAL_FILLERS = [
    "khoảng 2 hôm nay", "tự nhiên dạo này", "mấy ngày nay", "đột ngột từ sáng tới giờ",
    "gần đây", "khoảng tuần nay", "mới bị hôm qua", ""
]

class Medical10kGenerator:
    """Bộ Sinh & Kiểm Duyệt Dữ Liệu Quy Mô Đúng 10.000 Mẫu Chuẩn Gemma 4 e2b."""

    def __init__(self, target_count: int = 10000):
        self.target_count = target_count
        self.verifier = MedicalDataVerifierPipeline(enable_llm_critic=False)

    def _select_demographic_tuple(self, category: str, question: str) -> Tuple[str, str, str]:
        q_lower = question.lower()
        if "nhi" in category.lower() or "trẻ" in q_lower or "bé" in q_lower or "con em" in q_lower:
            return random.choice(PEDIATRIC_DEMOGRAPHICS)
        elif "đột quỵ" in q_lower or "thắt ngực" in q_lower or "tim" in q_lower or "bố em" in q_lower or "bà nội" in q_lower:
            return random.choice(SENIOR_DEMOGRAPHICS)
        elif "mang thai" in q_lower or "sản" in category.lower() or "kinh" in q_lower:
            return random.choice(FEMALE_DEMOGRAPHICS)
        else:
            return random.choice(ADULT_DEMOGRAPHICS)

    @staticmethod
    def _strip_existing_demographics(question: str) -> str:
        """Xóa sạch các số tuổi / xưng hô cũ trong câu hỏi gốc để tránh lặp."""
        text = question
        text = re.sub(r"^(con em|bố em|mẹ em|bé|em|bệnh nhân|người nhà|mẹ|bố|tôi|chị em|anh trai|chị gái)\s*", "", text, flags=re.I).strip()
        text = re.sub(r"\b\d+\s*(tuổi|tháng\s*tuổi|tháng)\b", "", text, flags=re.I).strip()
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _fix_pronoun_consistency(demo_title: str, text: str) -> str:
        """Đồng bộ đại từ xưng hô tránh trường hợp 'Mẹ em 62 tuổi ... em bị thắt tim'."""
        demo_lower = demo_title.lower()
        res = text

        # Nếu đối tượng hỏi là người thân/người khác (Không phải chính bản thân người hỏi)
        if any(k in demo_lower for k in ["mẹ", "bố", "bà", "ông", "bác", "cụ", "chú", "vợ", "chồng", "anh", "chị", "bạn"]):
            res = re.sub(r"\b(em|tôi|mình)\s+bị\b", "bị", res, flags=re.I)
            res = re.sub(r"\bđột ngột em bị\b", "đột ngột bị", res, flags=re.I)
            res = re.sub(r"\bđột nhiên em bị\b", "đột nhiên bị", res, flags=re.I)
            res = re.sub(r"\btự nhiên em bị\b", "tự nhiên bị", res, flags=re.I)
            res = re.sub(r"\bthỉnh thoảng em bị\b", "thỉnh thoảng bị", res, flags=re.I)

        elif any(k in demo_lower for k in ["bé", "con", "cháu", "trẻ"]):
            res = re.sub(r"\b(em|tôi|mình)\s+bị\b", "bé bị", res, flags=re.I)
            res = re.sub(r"\bđột ngột em bị\b", "đột ngột bé bị", res, flags=re.I)
            res = re.sub(r"\bđột nhiên em bị\b", "đột nhiên bé bị", res, flags=re.I)
            res = re.sub(r"\btự nhiên em bị\b", "tự nhiên bé bị", res, flags=re.I)
            res = re.sub(r"\bthỉnh thoảng em bị\b", "thỉnh thoảng bé bị", res, flags=re.I)

        return res

    @staticmethod
    def _sync_answer_age(answer: str, age_str: str, demo_ref: str) -> str:
        """Đồng bộ chính xác số tuổi trong câu trả lời từ seed."""
        res = answer
        res = res.replace("{AGE}", age_str).replace("{DEMO_REF}", demo_ref)
        
        res = re.sub(r"với bé \d+\s*(tuổi|tháng\s*tuổi|tháng)", f"với {demo_ref}", res, flags=re.I)
        res = re.sub(r"bé \d+\s*(tuổi|tháng\s*tuổi|tháng)", demo_ref, res, flags=re.I)
        res = re.sub(r"ở người lớn tuổi", f"ở {demo_ref}", res, flags=re.I)
        res = re.sub(r"ở người trung niên", f"ở {demo_ref}", res, flags=re.I)
        return res

    def generate_10k_dataset(self, raw_crawled_items: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        logger.info(f"=== KHỞI CHẠY BỘ GENERATOR DỮ LIỆU CHUẨN ĐỒNG BỘ TUỔI & XƯNG HỒ MỤC TIÊU: {self.target_count} MẪU ===")

        base_seeds = []
        for seed in SEED_MEDICAL_DATABASE:
            base_seeds.append({
                "source": "seed_kb",
                "category": seed.get("category", "General"),
                "question": seed["question"],
                "answer": seed["answer"],
                "is_red_flag": seed.get("is_red_flag", False),
                "is_medication": seed.get("is_medication", False),
                "is_ambiguous": seed.get("is_ambiguous", False)
            })

        if raw_crawled_items:
            for item in raw_crawled_items:
                base_seeds.append(item)

        clean_verified_dataset = []
        seen_user_questions = set()
        tested_candidates_count = 0
        batch_size = 500

        while len(clean_verified_dataset) < self.target_count:
            batch_formatted = []

            for _ in range(batch_size):
                seed_item = random.choice(base_seeds)
                cat = seed_item.get("category", "General")
                q_orig = seed_item.get("question", "")
                a_orig = seed_item.get("answer", "")
                is_ambig = seed_item.get("is_ambiguous", False)

                prefix = random.choice(VARIATION_PREFIXES)
                demo_title, age_str, demo_ref = self._select_demographic_tuple(cat, q_orig)
                filler = random.choice(CONVERSATIONAL_FILLERS)

                # Xử lý riêng cho nhóm Mơ Hồ (Ambiguous): Giữ nguyên vẻ tự nhiên ngắn gọn
                if is_ambig:
                    clean_q = self._strip_existing_demographics(q_orig)
                    if clean_q:
                        clean_q = clean_q[0].lower() + clean_q[1:]
                    new_q = f"{prefix}, {clean_q}"
                    new_a = a_orig
                else:
                    # Thay thế placeholders trong câu gốc nếu có
                    if "{AGE}" in q_orig:
                        clean_q = q_orig.replace("{AGE}", age_str)
                        clean_q = self._strip_existing_demographics(clean_q)
                    else:
                        clean_q = self._strip_existing_demographics(q_orig)

                    if clean_q:
                        clean_q = clean_q[0].lower() + clean_q[1:]

                    # Sửa lỗi xưng hô bất nhất (ví dụ: Mẹ em 62 tuổi ... em bị thắt tim)
                    clean_q = self._fix_pronoun_consistency(demo_title, clean_q)

                    # Ghép câu tự nhiên
                    filler_str = f" {filler}" if filler else ""
                    new_q = f"{prefix}, {demo_title}{filler_str} {clean_q}"
                    new_a = self._sync_answer_age(a_orig, age_str, demo_ref)

                new_q = TextCleaner.format_question(new_q)
                new_a = TextCleaner.format_answer(new_a)

                # Kiểm tra trùng lặp tuyệt đối
                norm_q = new_q.strip().lower()
                if norm_q in seen_user_questions:
                    continue

                question, answer, safety_flags = SafetyEngine.process_qa_safety(new_q, new_a, seed_meta=seed_item)

                batch_formatted.append({
                    "messages": [
                        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": answer}
                    ],
                    "metadata": {
                        "source": "scaled_variation",
                        "safety_flags": safety_flags
                    }
                })
                seen_user_questions.add(norm_q)

            tested_candidates_count += len(batch_formatted)
            v_res = self.verifier.run_pipeline(batch_formatted)
            passed_batch = v_res["passed_dataset"]

            clean_verified_dataset.extend(passed_batch)
            logger.info(f"[TIẾN TRÌNH 10K] Đã tích lũy: {len(clean_verified_dataset)} / {self.target_count} mẫu ĐẠT CHUẨN (Đã quét: {tested_candidates_count} ứng viên)...")

        if len(clean_verified_dataset) > self.target_count:
            random.seed(42)
            clean_verified_dataset = random.sample(clean_verified_dataset, self.target_count)

        logger.info(f"🎉 HOÀN THÀNH TẠO & VERIFY THÀNH CÔNG ĐÚNG {len(clean_verified_dataset)} MẪU Y TẾ ĐẠT CHUẨN NGUYÊN BẢN!")

        out_main = PROCESSED_DATA_DIR / "patient_medical_dataset.jsonl"
        with open(out_main, "w", encoding="utf-8") as f:
            for entry in clean_verified_dataset:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        DatasetSplitter.split_dataset(clean_verified_dataset)
        PhysicianAuditor.extract_audit_sample(clean_verified_dataset)

        return clean_verified_dataset
