import sys
import os
import argparse
from pathlib import Path
from huggingface_hub import HfApi, create_repo

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

DEFAULT_REPO_ID = "gemma-4-medkit-vietnamese"
MERGED_FOLDER = ROOT_DIR / "models" / "gemma_medkit_merged_16bit"
GGUF_FILE = ROOT_DIR / "models" / "Panda-Med-4-FP16.gguf"
MODELFILE_PATH = ROOT_DIR / "Modelfile"

MODEL_CARD_CONTENT = """---
language:
- vi
license: gemma
library_name: transformers
tags:
- medical
- vietnamese
- gemma2
- gguf
- ollama
- conversational
- sft
base_model: google/gemma-2-2b-it
pipeline_tag: text-generation
---

# 🏥 Panda Med 4 - Trợ lý Tư vấn Y tế AI Việt Nam

**Panda Med 4** là mô hình ngôn ngữ lớn chuyên sâu về y tế dành riêng cho người Việt Nam, được tinh chỉnh (Fine-tuned) từ kiến trúc **Gemma 2 (2B)** trên tập dữ liệu Hỏi-Đáp sức khỏe chất lượng cao.

---

## 🌟 Đặc điểm nổi bật & An toàn Y tế

1. **Văn phong thân thiện & Trấn an:** Giải thích nguyên nhân triệu chứng bằng ngôn từ đời thường dễ hiểu, đánh giá mức độ nghiêm trọng.
2. **Hệ thống Red Flags Safety:** Tự động nhận diện các triệu chứng nguy cấp (*đau ngực thắt, đột quỵ, sốt cao co giật, thở dốc...*) và khuyến cáo đưa bệnh nhân đi **Cấp cứu 115 / Bệnh viện ngay lập tức**.
3. **Thận trọng với Thuốc:** Tự động chèn cảnh báo không tự ý dùng kháng sinh / thuốc kê đơn khi chưa có chỉ định của bác sĩ/dược sĩ.
4. **Định dạng sẵn GGUF & Ollama:** Hỗ trợ chạy trực tiếp siêu mượt trên Ollama / LM Studio.

---

## 💻 1. Sử dụng trực tiếp qua Ollama (Khuyên dùng)

Bạn có thể kéo và chạy trực tiếp **Panda Med 4** thông qua Ollama:

```bash
ollama run hf.co/vnhkhwa/gemma-4-medkit-vietnamese
```

Hoặc nạp bằng `Modelfile` với tên mô hình `Panda-Med-4`:

```bash
ollama create Panda-Med-4 -f Modelfile
ollama run Panda-Med-4
```

---

## 🐍 2. Sử dụng bằng Python (Transformers)

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "vnhkhwa/gemma-4-medkit-vietnamese"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto"
)

prompt = "<start_of_turn>user\\nCon em 3 tuổi sốt 38.5 độ, có cần đi viện không ạ?<end_of_turn>\\n<start_of_turn>model\\n"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.3)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## ⚠️ Miễn trừ trách nhiệm (Medical Disclaimer)

*Thông tin do **Panda Med 4** cung cấp chỉ mang tính chất tham khảo và hỗ trợ giáo dục sức khỏe. Mô hình KHÔNG thay thế cho chẩn đoán, điều trị hay tư vấn y khoa trực tiếp từ Bác sĩ chuyên khoa. Trong trường hợp cấp cứu, vui lòng gọi **115** hoặc đến cơ sở y tế gần nhất.*
"""

def deploy_full_to_hf(token: str, repo_id: str = DEFAULT_REPO_ID):
    print("=" * 60)
    print("🚀 TIẾN HÀNH DEPLOY TOÀN BỘ PANDA MED 4 LÊN HUGGING FACE")
    print("=" * 60)

    api = HfApi(token=token)
    user_info = api.whoami(token=token)
    username = user_info.get("name")
    
    if "/" not in repo_id:
        target_repo = f"{username}/{repo_id}"
    else:
        target_repo = repo_id

    print(f"👤 Tài khoản: {username}")
    print(f"📌 Repository Target: https://huggingface.co/{target_repo}")

    create_repo(repo_id=target_repo, token=token, exist_ok=True, repo_type="model")

    # 1. Upload thư mục Merged (safetensors 16-bit)
    if MERGED_FOLDER.exists():
        print(f"\n1. Đang upload thư mục Merged Model ({MERGED_FOLDER})...")
        api.upload_folder(
            folder_path=str(MERGED_FOLDER),
            repo_id=target_repo,
            repo_type="model"
        )
        print("✅ Upload Merged Model thành công!")

    # 2. Upload file GGUF nếu có
    if GGUF_FILE.exists():
        print(f"\n2. Đang upload file GGUF ({GGUF_FILE.name})...")
        api.upload_file(
            path_or_fileobj=str(GGUF_FILE),
            path_in_repo=GGUF_FILE.name,
            repo_id=target_repo,
            repo_type="model"
        )
        print(f"✅ Upload file {GGUF_FILE.name} thành công!")
    else:
        print(f"⚠️ Chưa thấy file {GGUF_FILE.name}, bỏ qua upload GGUF.")

    # 3. Upload Modelfile nếu có
    if MODELFILE_PATH.exists():
        print(f"\n3. Đang upload file Modelfile...")
        api.upload_file(
            path_or_fileobj=str(MODELFILE_PATH),
            path_in_repo="Modelfile",
            repo_id=target_repo,
            repo_type="model"
        )
        print("✅ Upload Modelfile thành công!")

    # 4. Upload Model Card README.md
    print(f"\n4. Đang upload Model Card README.md (Giới thiệu Panda Med 4)...")
    temp_readme = ROOT_DIR / "TEMP_HF_README.md"
    with open(temp_readme, "w", encoding="utf-8") as f:
        f.write(MODEL_CARD_CONTENT)

    api.upload_file(
        path_or_fileobj=str(temp_readme),
        path_in_repo="README.md",
        repo_id=target_repo,
        repo_type="model"
    )
    if temp_readme.exists():
        temp_readme.unlink()

    print("\n" + "=" * 60)
    print("🎉 DEPLOY TOÀN BỘ PANDA MED 4 LÊN HUGGING FACE THÀNH CÔNG!")
    print(f"🔗 Trang mô hình: https://huggingface.co/{target_repo}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Panda Med 4 toàn bộ lên Hugging Face Hub")
    parser.add_argument("--token", type=str, required=True, help="Hugging Face Write Token")
    parser.add_argument("--repo_id", type=str, default=DEFAULT_REPO_ID, help="Tên Repo ID")

    args = parser.parse_args()
    deploy_full_to_hf(token=args.token, repo_id=args.repo_id)
