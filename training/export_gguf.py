import sys
import os
import urllib.request
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

MERGED_MODEL_PATH = ROOT_DIR / "models" / "gemma_medkit_merged_16bit"
TOKENIZER_MODEL_PATH = MERGED_MODEL_PATH / "tokenizer.model"
TOKENIZER_URLS = [
    "https://huggingface.co/unsloth/gemma-4-E2B-it-unsloth-bnb-4bit/resolve/main/tokenizer.model",
    "https://huggingface.co/unsloth/gemma-2-2b-it/resolve/main/tokenizer.model",
    "https://huggingface.co/google/gemma-2-2b-it/resolve/main/tokenizer.model"
]

OUTPUT_GGUF_DIR = ROOT_DIR / "models"
OUTPUT_FP16_GGUF = OUTPUT_GGUF_DIR / "Panda-Med-4-FP16.gguf"
MODEL_NAME = "Panda-Med-4"

def ensure_tokenizer_model():
    """Tải file tokenizer.model cần thiết cho llama.cpp nếu chưa có."""
    if not TOKENIZER_MODEL_PATH.exists():
        print(f"📥 Đang tải tokenizer.model cho mô hình Gemma từ HuggingFace...")
        for url in TOKENIZER_URLS:
            try:
                urllib.request.urlretrieve(url, TOKENIZER_MODEL_PATH)
                print(f"✅ Đã tải thành công tokenizer.model từ {url}")
                return True
            except Exception:
                continue
        print("❌ Không thể tải tokenizer.model từ các nguồn HuggingFace.")
        return False
    return True

def convert_to_gguf():
    print("=" * 60)
    print(f"🚀 XUẤT MODEL GGUF CHO MÔ HÌNH: {MODEL_NAME}")
    print("=" * 60)

    if not MERGED_MODEL_PATH.exists():
        print(f"❌ Không tìm thấy thư mục mô hình đã merged tại: {MERGED_MODEL_PATH}")
        print("💡 Hãy chạy 'python training/merge_lora.py' trước.")
        return

    if not ensure_tokenizer_model():
        return

    convert_script = ROOT_DIR / "llama.cpp" / "convert_hf_to_gguf.py"
    if not convert_script.exists():
        print(f"❌ Không tìm thấy script convert tại {convert_script}")
        return

    cmd = [
        sys.executable,
        str(convert_script),
        str(MERGED_MODEL_PATH),
        "--outfile", str(OUTPUT_FP16_GGUF)
    ]

    print(f"\n⚙️ Đang tiến hành chuyển đổi sang file GGUF ({OUTPUT_FP16_GGUF.name})...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print(f"🎉 TẠO FILE GGUF THÀNH CÔNG!")
        print(f"📁 Đường dẫn file GGUF: {OUTPUT_FP16_GGUF}")
        print("=" * 60)

        # Tạo file Modelfile cho Ollama với tên Panda Med 4
        modelfile_path = ROOT_DIR / "Modelfile"
        modelfile_content = f"""# Modelfile chuẩn dành cho mô hình: {MODEL_NAME}
FROM ./models/{OUTPUT_FP16_GGUF.name}

SYSTEM \"\"\"Bạn là {MODEL_NAME}, một trợ lý tư vấn y tế AI thông minh, chuyên nghiệp và tận tâm dành cho người dùng tại Việt Nam. Bạn giải thích nguyên nhân dễ hiểu, trấn an bệnh nhân, đưa ra lời khuyên an toàn y tế và hướng dẫn đi khám ngay nếu có dấu hiệu nguy hiểm (Red Flags).\"\"\"

TEMPLATE \"\"\"{{{{ if .System }}}}<start_of_turn>system
{{{{ .System }}}}<end_of_turn>
{{{{ end }}}}{{{{ if .Prompt }}}}<start_of_turn>user
{{{{ .Prompt }}}}<end_of_turn>
{{{{ end }}}}<start_of_turn>model
{{{{ .Response }}}}<end_of_turn>\"\"\"

PARAMETER stop "<start_of_turn>"
PARAMETER stop "<end_of_turn>"
PARAMETER temperature 0.3
PARAMETER top_p 0.9
"""
        with open(modelfile_path, "w", encoding="utf-8") as f:
            f.write(modelfile_content)
        
        print(f"\n📝 Đã tự động tạo file Ollama Modelfile tại: {modelfile_path}")
        print(f"👉 Để nạp mô hình vào Ollama với tên '{MODEL_NAME}', hãy chạy lệnh:")
        print(f"   ollama create {MODEL_NAME} -f Modelfile")
        print(f"👉 Sau đó gõ lệnh để chat:")
        print(f"   ollama run {MODEL_NAME}")
    else:
        print("❌ Lỗi trong quá trình xuất file GGUF.")

if __name__ == "__main__":
    convert_to_gguf()
