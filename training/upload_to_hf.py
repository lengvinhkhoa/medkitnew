import sys
import argparse
from pathlib import Path
from transformers import AutoTokenizer
from peft import PeftModel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

MODEL_ADAPTER_PATH = ROOT_DIR / "models" / "gemma_medkit_qlora"

def push_to_huggingface(
    repo_id: str,
    token: str,
    adapter_path: Path = MODEL_ADAPTER_PATH
):
    """
    Đẩy LoRA Adapter đã Fine-tune lên Hugging Face Hub.
    """
    print("=" * 60)
    print("🚀 ĐẨY MODEL FINE-TUNED MEDKIT LÊN HUGGING FACE HUB")
    print(f"📌 Target Repository: https://huggingface.co/{repo_id}")
    print(f"📌 Local Adapter Path: {adapter_path}")
    print("=" * 60)

    if not adapter_path.exists():
        print(f"❌ Không tìm thấy LoRA Adapter tại: {adapter_path}")
        return

    try:
        from huggingface_hub import HfApi, create_repo
        
        print("\n1. Khởi tạo / Kiểm tra Repository trên Hugging Face...")
        api = HfApi(token=token)
        create_repo(repo_id=repo_id, token=token, exist_ok=True, repo_type="model")

        print("\n2. Đang tải Adapter và Tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(adapter_path)
        
        print("\n3. Đang Upload toàn bộ trọng số LoRA lên Hugging Face Hub...")
        api.upload_folder(
            folder_path=str(adapter_path),
            repo_id=repo_id,
            repo_type="model"
        )

        print("\n" + "=" * 60)
        print("🎉 XUẤT VÀ UPLOAD THÀNH CÔNG 100%!")
        print(f"🔗 Link Model của bạn: https://huggingface.co/{repo_id}")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Lỗi trong quá trình upload: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload LoRA Adapter lên Hugging Face Hub")
    parser.add_argument("--repo_id", type=str, required=True, help="Tên Repo trên HF (Ví dụ: lengvinhkhoa/gemma-4-medkit-vietnamese)")
    parser.add_argument("--token", type=str, required=True, help="Hugging Face Write Token (hf_xxx...)")

    args = parser.parse_args()
    push_to_huggingface(args.repo_id, args.token)
