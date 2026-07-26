import json
from pathlib import Path
from typing import List, Dict, Any
from datasets import Dataset

def load_jsonl_dataset(file_path: Path) -> Dataset:
    """Tải file .jsonl (chứa format messages role: system, user, assistant) thành HuggingFace Dataset."""
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                records.append({"messages": item["messages"]})
    
    return Dataset.from_list(records)

def format_messages_for_gemma(examples: Dict[str, Any], tokenizer) -> Dict[str, List[str]]:
    """Format hội thoại theo Gemma Chat Template chuẩn."""
    texts = []
    for messages in examples["messages"]:
        # Chuyển đổi định dạng hội thoại thành chuỗi prompt Gemma 2
        try:
            formatted_text = tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=False
            )
        except Exception:
            # Fallback nếu tokenizer chưa hỗ trợ role system trong chat template
            system_msg = ""
            user_msg = ""
            assistant_msg = ""
            for msg in messages:
                if msg["role"] == "system":
                    system_msg = msg["content"]
                elif msg["role"] == "user":
                    user_msg = msg["content"]
                elif msg["role"] == "assistant":
                    assistant_msg = msg["content"]
            
            formatted_text = f"<start_of_turn>user\n{system_msg}\n\n{user_msg}<end_of_turn>\n<start_of_turn>model\n{assistant_msg}<end_of_turn>"
        
        texts.append(formatted_text)
    
    return {"text": texts}
