import os
import sys
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TextStreamer
from peft import PeftModel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Cấu hình Cache HuggingFace lưu trực tiếp vào thư mục dự án trên ổ F: (tránh ổ C: bị hết đĩa)
CACHE_DIR = ROOT_DIR / "models" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(CACHE_DIR)
os.environ["TRANSFORMERS_CACHE"] = str(CACHE_DIR)
os.environ["HF_HUB_CACHE"] = str(CACHE_DIR)

from config.settings import DEFAULT_SYSTEM_PROMPT

MODEL_ADAPTER_PATH = ROOT_DIR / "models" / "gemma_medkit_qlora"
DEFAULT_MODEL_NAME = "unsloth/gemma-4-E2B-it-unsloth-bnb-4bit"

def load_medkit_gemma(
    base_model_name: str = DEFAULT_MODEL_NAME,
    adapter_path: Path = MODEL_ADAPTER_PATH
):
    """Tải Base Model Gemma + LoRA Adapter đã huấn luyện trên RTX 3060."""
    print("=" * 60)
    print("🤖 NẠP MODEL TRỢ LÝ Y TẾ AI NGUYÊN BẢN GEMMA FINE-TUNED MEDKIT")
    print(f"📌 Base Model: {base_model_name}")
    print(f"📌 Cache Directory (Ổ F): {CACHE_DIR}")
    print(f"📌 LoRA Adapter: {adapter_path}")
    print("=" * 60)

    is_cuda_ok = torch.cuda.is_available()

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16 if is_cuda_ok and torch.cuda.is_bf16_supported() else torch.float16,
        bnb_4bit_use_double_quant=True
    )

    tokenizer = AutoTokenizer.from_pretrained(
        base_model_name,
        cache_dir=str(CACHE_DIR),
        trust_remote_code=True
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config,
        device_map="auto" if is_cuda_ok else "cpu",
        cache_dir=str(CACHE_DIR),
        trust_remote_code=True
    )

    if adapter_path.exists():
        print(f"✅ Nạp LoRA Adapter thành công từ: {adapter_path}")
        model = PeftModel.from_pretrained(base_model, str(adapter_path))
    else:
        print(f"⚠️ Chưa tìm thấy LoRA Adapter tại {adapter_path}. Sử dụng Base Model gốc để test.")
        model = base_model

    return model, tokenizer

def chat_interactive(base_model_name: str = DEFAULT_MODEL_NAME):
    """Giao diện Chat thử nghiệm trực tiếp trên terminal với Streamer."""
    model, tokenizer = load_medkit_gemma(base_model_name)
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

    print("\n💡 ĐÃ SẴN SÀNG! Bạn có thể gõ câu hỏi y tế bên dưới (Gõ 'exit' hoặc 'quit' để thoát).\n")

    while True:
        try:
            user_input = input("\n👤 Bệnh nhân: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Bác sĩ AI chào tạm biệt bạn!")
                break

            # Ghép System Prompt vào User message chuẩn Gemma Chat Template
            user_content = f"{DEFAULT_SYSTEM_PROMPT}\n\nCâu hỏi: {user_input}"
            messages = [
                {"role": "user", "content": user_content}
            ]

            try:
                prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            except Exception:
                prompt = f"<start_of_turn>user\n{user_content}<end_of_turn>\n<start_of_turn>model\n"

            inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

            print("\n👨‍⚕️ Trợ lý Y tế AI: ", end="", flush=True)
            _ = model.generate(
                **inputs,
                streamer=streamer,
                max_new_tokens=512,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.1,
                do_sample=True
            )
            print()

        except KeyboardInterrupt:
            print("\n👋 Đã dừng chat.")
            break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chạy thử nghiệm Model Gemma đã Fine-tuned")
    parser.add_argument("--base_model", type=str, default=DEFAULT_MODEL_NAME, help="Hugging Face Base Model ID")

    args = parser.parse_args()
    chat_interactive(args.base_model)
