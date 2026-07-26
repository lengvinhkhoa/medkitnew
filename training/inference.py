import sys
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TextStreamer
from peft import PeftModel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from config.settings import DEFAULT_SYSTEM_PROMPT

MODEL_ADAPTER_PATH = ROOT_DIR / "models" / "gemma_medkit_qlora"

def load_medkit_gemma(
    base_model_name: str = "google/gemma-2-2b-it",
    adapter_path: Path = MODEL_ADAPTER_PATH
):
    """Tải Base Model Gemma + LoRA Adapter đã huấn luyện trên RTX 3060."""
    print("=" * 60)
    print("🤖 NẠP MODEL NGUYÊN BẢN GEMMA FINE-TUNED MEDKIT")
    print(f"📌 Base Model: {base_model_name}")
    print(f"📌 LoRA Adapter: {adapter_path}")
    print("=" * 60)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
        bnb_4bit_use_double_quant=True
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )

    if adapter_path.exists():
        print(f"✅ Nạp LoRA Adapter thành công từ: {adapter_path}")
        model = PeftModel.from_pretrained(base_model, str(adapter_path))
    else:
        print(f"⚠️ Chưa tìm thấy LoRA Adapter tại {adapter_path}. Sử dụng Base Model gốc để test.")
        model = base_model

    return model, tokenizer

def chat_interactive(base_model_name: str = "google/gemma-2-2b-it"):
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

            messages = [
                {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]

            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
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
    parser = argparse.ArgumentParser(description="Chạy thử nghiệm Model Gemma 2 đã Fine-tuned")
    parser.add_argument("--base_model", type=str, default="google/gemma-2-2b-it", help="Hugging Face Base Model ID")

    args = parser.parse_args()
    chat_interactive(args.base_model)
