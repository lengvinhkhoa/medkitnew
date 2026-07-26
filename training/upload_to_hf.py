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
    print("=" * 60)

    if not adapter_path.exists():
        print(f"❌ Không tìm thấy LoRA Adapter tại: {adapter_path}")
        return

    try:
        from huggingface_hub import HfApi, create_repo
        
        api = HfApi(token=token)
        user_info = api.whoami(token=token)
        hf_username = user_info.get("name")
        print(f"👤 Đã xác thực thành công tài khoản Hugging Face: {hf_username}")

        # Tự động sửa namespace repo theo đúng Username tài khoản Token
        if "/" not in repo_id:
            repo_id = f"{hf_username}/{repo_id}"
        else:
            repo_name_only = repo_id.split("/", 1)[1]
            repo_id = f"{hf_username}/{repo_name_only}"

        print(f"📌 Target Repository: https://huggingface.co/{repo_id}")
        print(f"📌 Local Adapter Path: {adapter_path}")

        print("\n1. Khởi tạo / Kiểm tra Repository trên Hugging Face...")
        create_repo(repo_id=repo_id, token=token, exist_ok=True, repo_type="model")

        print("\n2. Đang Upload toàn bộ trọng số LoRA Adapter lên Hugging Face Hub...")
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
        print("💡 Lưu ý: Hãy đảm bảo Token được tạo ở dạng 'Write' (Quyền ghi) tại https://huggingface.co/settings/tokens")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload LoRA Adapter lên Hugging Face Hub")
    parser.add_argument("--repo_id", type=str, default="gemma-4-medkit-vietnamese", help="Tên Repo trên HF")
    parser.add_argument("--token", type=str, required=True, help="Hugging Face Write Token (hf_xxx...)")

    args = parser.parse_args()
    push_to_huggingface(args.repo_id, args.token)
