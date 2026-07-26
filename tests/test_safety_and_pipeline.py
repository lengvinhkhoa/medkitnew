import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from processors.cleaner import TextCleaner
from processors.safety_filter import SafetyEngine
from processors.formatter import DataFormatter

def test_cleaner_removes_junk():
    raw_text = "Hỏi: Con em sốt 38.5 độ. Xem thêm tại Vinmec. Hotline: 0912345678"
    clean_q = TextCleaner.format_question(raw_text)
    assert "Hotline" not in clean_q
    assert "Xem thêm tại" not in clean_q
    assert clean_q.startswith("Con em sốt")

def test_safety_filter_red_flag():
    q = "Bố em bị đau ngực dữ dội lan ra tay trái, vã mồ hôi hột"
    a = "Nên cho bác nghỉ ngơi."
    _, processed_a, flags = SafetyEngine.process_qa_safety(q, a)
    assert flags["is_red_flag"] is True
    assert "115" in processed_a or "cấp cứu" in processed_a.lower()

def test_safety_filter_medication():
    q = "Cho em hỏi liều lượng uống kháng sinh Amoxicillin cho người lớn thế nào ạ?"
    a = "Uống ngày 2 lần."
    _, processed_a, flags = SafetyEngine.process_qa_safety(q, a)
    assert flags["is_medication"] is True
    assert "Dược sĩ" in processed_a or "bác sĩ" in processed_a.lower()

def test_formatter_gemma_messages():
    formatter = DataFormatter()
    raw_data = [
        {
            "source": "unit_test",
            "url": "http://test.com",
            "question": "Con em 3 tuổi sốt 38.5 độ, có cần đi viện không ạ?",
            "answer": "Với bé 3 tuổi sốt 38.5°C, đây là sốt nhẹ-vừa. Cho bé uống nhiều nước và theo dõi thêm."
        }
    ]
    formatted = formatter.format_to_gemma_messages(raw_data)
    assert len(formatted) == 1
    messages = formatted[0]["messages"]
    assert len(messages) == 3
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[2]["role"] == "assistant"
