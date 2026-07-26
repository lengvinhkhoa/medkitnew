import sys
import os
import torch
from pathlib import Path
from typing import Optional
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

ADAPTER_PATH = ROOT_DIR / "models" / "gemma_medkit_qlora"
MERGED_OUTPUT_PATH = ROOT_DIR / "models" / "gemma_medkit_merged_16bit"

def merge_and_save(
    base_model_name: str = "unsloth/gemma-4-E2B-it-unsloth-bnb-4bit",
    adapter_path: Path = ADAPTER_PATH,
    output_path: Path = MERGED_OUTPUT_PATH,
    token: Optional[str] = None
):
    """Merge LoRA adapter vào Base Model và xuất ra weights 16-bit nguyên bản."""
    print("=" * 60)
    print("🔀 HÀM MERGE LORA ADAPTER VÀO BASE MODEL (Dành cho xuất GGUF / Ollama)")
    print(f"📌 Base Model: {base_model_name}")
    print(f"📌 Adapter: {adapter_path}")
    print(f"📌 Target Output: {output_path}")
    print("=" * 60)

    hf_token = token or os.environ.get("HF_TOKEN")

    if not adapter_path.exists():
        print(f"❌ Không tìm thấy adapter tại: {adapter_path}")
        return

    try:
        print("\n1. Tải Base Model 16-bit...")
        tokenizer = AutoTokenizer.from_pretrained(
            base_model_name,
            token=hf_token,
            trust_remote_code=True
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map="cpu",  # Merge trên CPU/RAM để tránh OOM GPU
            token=hf_token,
            trust_remote_code=True
        )

        print("\n2. Nạp LoRA Adapter...")
        peft_model = PeftModel.from_pretrained(base_model, str(adapter_path))

        print("\n3. Hợp nhất (Merge and Unload) trọng số...")
        merged_model = peft_model.merge_and_unload()

        print(f"\n4. Lưu Model hoàn chỉnh tại: {output_path}...")
        output_path.mkdir(parents=True, exist_ok=True)
        merged_model.save_pretrained(str(output_path), safe_serialization=True)
        tokenizer.save_pretrained(str(output_path))

        print(f"✅ MERGE THÀNH CÔNG! ĐÃ XUẤT MODEL 16-BIT TẠI: {output_path}")

    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình merge: {e}")
        if "gated repo" in str(e).lower() or "401" in str(e):
            print("\n💡 CÁCH KHẮC PHỤC LỖI GATED REPO / 401:")
            print("1. Truy cập https://huggingface.co/google/gemma-2-2b-it và nhấn 'Accept License' (chấp nhận điều khoản Gemma).")
            print("2. Truyền token HF của bạn khi chạy lệnh:")
            print("   python training/merge_lora.py --token hf_xxxxxxxxxxxxxxxxx")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge LoRA Adapter vào Gemma 2 Base Model")
    parser.add_argument("--base_model", type=str, default="unsloth/gemma-2-2b-it", help="Hugging Face Base Model ID (16-bit float)")
    parser.add_argument("--adapter", type=str, default=str(ADAPTER_PATH), help="Đường dẫn LoRA adapter")
    parser.add_argument("--output", type=str, default=str(MERGED_OUTPUT_PATH), help="Đường dẫn lưu model merged")
    parser.add_argument("--token", type=str, default=None, help="Hugging Face Token (Access Token)")

    args = parser.parse_args()
    merge_and_save(args.base_model, Path(args.adapter), Path(args.output), token=args.token)

