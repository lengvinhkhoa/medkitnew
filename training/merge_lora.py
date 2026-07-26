import sys
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

ADAPTER_PATH = ROOT_DIR / "models" / "gemma_medkit_qlora"
MERGED_OUTPUT_PATH = ROOT_DIR / "models" / "gemma_medkit_merged_16bit"

def merge_and_save(
    base_model_name: str = "google/gemma-2-2b-it",
    adapter_path: Path = ADAPTER_PATH,
    output_path: Path = MERGED_OUTPUT_PATH
):
    """Merge LoRA adapter vào Base Model và xuất ra weights 16-bit nguyên bản."""
    print("=" * 60)
    print("🔀 HÀM MERGE LORA ADAPTER VÀO BASE MODEL (Dành cho xuất GGUF / Ollama)")
    print(f"📌 Base Model: {base_model_name}")
    print(f"📌 Adapter: {adapter_path}")
    print(f"📌 Target Output: {output_path}")
    print("=" * 60)

    if not adapter_path.exists():
        print(f"❌ Không tìm thấy adapter tại: {adapter_path}")
        return

    print("\n1. Tải Base Model 16-bit...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="cpu",  # Merge trên CPU/RAM để tránh OOM GPU
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Merge LoRA Adapter vào Gemma 2 Base Model")
    parser.add_argument("--base_model", type=str, default="google/gemma-2-2b-it", help="Hugging Face Base Model ID")
    parser.add_argument("--adapter", type=str, default=str(ADAPTER_PATH), help="Đường dẫn LoRA adapter")
    parser.add_argument("--output", type=str, default=str(MERGED_OUTPUT_PATH), help="Đường dẫn lưu model merged")

    args = parser.parse_args()
    merge_and_save(args.base_model, Path(args.adapter), Path(args.output))
