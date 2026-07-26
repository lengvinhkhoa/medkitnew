# 🚀 BỘ TOOLKIT HUẤN LUYỆN MODEL GEMMA 2 NGUYÊN BẢN (QLoRA 4-BIT)
> **Tối ưu riêng cho GPU NVIDIA RTX 3060 (12GB VRAM) & Windows System**

Thư mục `training/` chứa toàn bộ mã nguồn để tiến hành Fine-tune mô hình **Gemma 2 (2B / 9B)** trên bộ dữ liệu y tế 10.000 mẫu đã qua bộ kiểm duyệt 4 lớp.

---

## 📂 1. Cấu trúc thư mục `training/`

```
medkitnew/
├── training/
│   ├── dataset_loader.py     # Loader & Format dữ liệu JSONL sang HuggingFace Gemma Prompt
│   ├── train_qlora.py        # Kịch bản huấn luyện QLoRA 4-bit chính (Tối ưu 12GB VRAM)
│   ├── inference.py          # Script Chat thử nghiệm trực tiếp model sau khi fine-tune
│   ├── merge_lora.py         # Script hợp nhất LoRA Adapter thành model 16-bit nguyên bản
│   ├── requirements_train.txt # Thư viện cần thiết cho quá trình train
│   └── README_TRAIN.md       # Hướng dẫn chi tiết sử dụng
├── data/processed/
│   ├── train.jsonl           # 8,504 mẫu huấn luyện
│   ├── eval.jsonl            # 748 mẫu đánh giá
│   └── test.jsonl            # 748 mẫu kiểm thử
└── models/
    └── gemma_medkit_qlora/   # Nơi lưu LoRA Adapter sau khi train xong
```

---

## 🛠️ 2. Cài đặt môi trường huấn luyện

Mở Terminal / PowerShell tại thư mục gốc của dự án (`medkitnew`) và cài đặt dependencies:

```bash
# 1. Cài đặt PyTorch với CUDA hỗ trợ RTX 3060
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 2. Cài đặt các thư viện Transformers, PEFT, BitsAndBytes, TRL
pip install -r training/requirements_train.txt
```

*(Tùy chọn nâng cao)*: Nếu muốn tăng tốc độ train lên 2 lần và tiết kiệm thêm 50% VRAM:
```bash
pip install unsloth
```

---

## 🎯 3. Tiến hành Huấn luyện (Train)

### 🔹 Cách 1: Chạy trực tiếp với tham số mặc định (Gemma-2-2b-it)
```bash
python training/train_qlora.py
```

### 🔹 Cách 2: Tùy chỉnh tham số phù hợp nhu cầu
```bash
python training/train_qlora.py \
    --model google/gemma-2-2b-it \
    --epochs 3 \
    --batch_size 2 \
    --grad_accum 4 \
    --lr 2e-4 \
    --max_len 1024
```

### 🔹 Cách 3: Kích hoạt Unsloth tăng tốc (nếu đã cài `unsloth`)
```bash
python training/train_qlora.py --unsloth
```

### ⚙️ Thông số tối ưu sẵn cho RTX 3060 12GB VRAM:
- **Quantization**: BitsAndBytes 4-bit (`nf4`, `bfloat16`/`float16`)
- **Optimizer**: `paged_adamw_8bit` (Tránh tràn VRAM khi tích lũy Gradient)
- **Batch size per device**: `2`
- **Gradient Accumulation**: `4` (Tương đương Effective Batch Size = 8)
- **VRAM Sử dụng thực tế**: **~5.8 GB / 12 GB** (Cực kỳ an toàn, không lo đơ/lag máy)

---

## 💬 4. Test Chat thử nghiệm Model sau khi Train

Sau khi huấn luyện hoàn tất, LoRA Adapter sẽ được lưu tự động tại `models/gemma_medkit_qlora`. Mở terminal và chạy lệnh test:

```bash
python training/inference.py
```
Gõ câu hỏi y tế để trải nghiệm Bác sĩ AI trả lời trực tiếp dạng streaming!

---

## 🔀 5. Merge LoRA thành Model 16-bit (Để xuất GGUF / Ollama)

Nếu bạn muốn đóng gói mô hình để chạy trên **Ollama**, **LM Studio** hoặc **vLLM**:

```bash
python training/merge_lora.py
```
Model hợp nhất 16-bit hoàn chỉnh sẽ được xuất ra tại: `models/gemma_medkit_merged_16bit`.
