import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from verification.layer1_syntax import Layer1SyntaxVerifier
from verification.layer2_safety_rules import Layer2SafetyVerifier
from verification.layer3_dedup_diversity import Layer3DeduplicationVerifier
from verification.layer4_llm_critic import Layer4LLMCriticVerifier
from verification.verifier_pipeline import MedicalDataVerifierPipeline
from dataset_ops.splitter import DatasetSplitter

def test_layer1_syntax():
    valid_entry = {
        "messages": [
            {"role": "system", "content": "System prompt test"},
            {"role": "user", "content": "Con em bị sốt 38.5 độ thì làm sao ạ?"},
            {"role": "assistant", "content": "Với bé sốt 38.5 độ bạn nên cho bé uống nhiều nước và theo dõi thêm."}
        ]
    }
    ok, msg = Layer1SyntaxVerifier.verify(valid_entry)
    assert ok is True

    invalid_entry = {"messages": [{"role": "user", "content": "short"}]}
    ok_inv, _ = Layer1SyntaxVerifier.verify(invalid_entry)
    assert ok_inv is False

def test_layer2_safety_red_flag_detection():
    red_flag_entry = {
        "messages": [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "Bố em bị đau ngực dữ dội lan ra tay trái, vã mồ hôi hột"},
            {"role": "assistant", "content": "Hãy cho bác nằm nghỉ ngơi và theo dõi thêm tại nhà."}  # Thiếu Cấp cứu 115
        ]
    }
    ok, msg = Layer2SafetyVerifier.verify(red_flag_entry)
    assert ok is False
    assert "Red Flag Violation" in msg

def test_layer3_deduplication():
    verifier = Layer3DeduplicationVerifier(similarity_threshold=0.8)
    entry1 = {
        "messages": [
            {"role": "system", "content": "Sys"},
            {"role": "user", "content": "Con em 3 tuổi bị sốt 38.5 độ có sao không ạ?"},
            {"role": "assistant", "content": "Sốt 38.5 độ là sốt nhẹ vừa bạn nên lau mát cho bé."}
        ]
    }
    entry2 = {
        "messages": [
            {"role": "system", "content": "Sys"},
            {"role": "user", "content": "Con em 3 tuổi sốt 38.5 độ có sao không ạ?"}, # Rất trùng lặp với entry 1
            {"role": "assistant", "content": "Sốt 38.5 độ là sốt nhẹ vừa bạn nên lau mát cho bé."}
        ]
    }
    ok1, _ = verifier.verify_entry(entry1)
    assert ok1 is True
    ok2, msg2 = verifier.verify_entry(entry2)
    assert ok2 is False
    assert "Fuzzy Duplicate" in msg2

def test_dataset_splitter():
    sample_dataset = []
    for i in range(100):
        sample_dataset.append({
            "messages": [
                {"role": "system", "content": "sys"},
                {"role": "user", "content": f"Câu hỏi bệnh nhân số {i} với độ dài thích hợp?"},
                {"role": "assistant", "content": f"Câu trả lời y tế mẫu số {i} giải thích chi tiết dễ hiểu."}
            ],
            "metadata": {
                "safety_flags": {"is_red_flag": (i % 5 == 0)}
            }
        })

    split_paths = DatasetSplitter.split_dataset(sample_dataset)
    assert split_paths["train"].exists()
    assert split_paths["eval"].exists()
    assert split_paths["test"].exists()
