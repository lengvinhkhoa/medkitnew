import os
import sys
import torch
from pathlib import Path
from typing import Optional

# Thêm root path dự án
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Cấu hình Cache HuggingFace lưu trực tiếp vào thư mục dự án trên ổ F:
CACHE_DIR = ROOT_DIR / "models" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(CACHE_DIR)
os.environ["TRANSFORMERS_CACHE"] = str(CACHE_DIR)
os.environ["HF_HUB_CACHE"] = str(CACHE_DIR)

from training.dataset_loader import load_jsonl_dataset, format_messages_for_gemma

# Đường dẫn dữ liệu
TRAIN_FILE = ROOT_DIR / "data" / "processed" / "train.jsonl"
EVAL_FILE = ROOT_DIR / "data" / "processed" / "eval.jsonl"
OUTPUT_DIR = ROOT_DIR / "models" / "gemma_medkit_qlora"

# Model mặc định
DEFAULT_MODEL_NAME = "unsloth/gemma-4-E2B-it-unsloth-bnb-4bit"

def run_training(
    model_name: str = DEFAULT_MODEL_NAME,
    output_dir: Path = OUTPUT_DIR,
    num_epochs: int = 3,
    batch_size: int = 2,
    gradient_accumulation_steps: int = 4,
    learning_rate: float = 2e-4,
    max_seq_length: int = 1024,
    use_unsloth: bool = False
):
    """
    Huấn luyện Gemma bằng kỹ thuật QLoRA 4-bit tối ưu riêng cho GPU RTX 3060 12GB VRAM.
    """
    print("=" * 60)
    print("🚀 KHỞI CHẠY HUẤN LUYỆN GEMMA VỚI TỆP DATASET NGUYÊN BẢN 10.000 MẪU Y TẾ")
    is_cuda_ok = torch.cuda.is_available()
    print(f"📌 GPU Target: RTX 3060 12GB VRAM | CUDA Available: {is_cuda_ok}")
    if is_cuda_ok:
        print(f"📌 Card GPU: {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB VRAM)")
    else:
        print("⚠️ CẢNH BÁO: PyTorch hiện tại KHÔNG nhận diện được GPU CUDA!")
    
    print(f"📌 Base Model Target: {model_name}")
    print(f"📌 Cache Directory (Ổ F): {CACHE_DIR}")
    print(f"📌 Target Output: {output_dir}")
    print("=" * 60)

    # 1. Tải Dataset
    print("\n📂 1. Tải dữ liệu huấn luyện...")
    train_dataset = load_jsonl_dataset(TRAIN_FILE)
    eval_dataset = load_jsonl_dataset(EVAL_FILE)
    print(f"  - Tập Train: {len(train_dataset)} mẫu")
    print(f"  - Tập Eval: {len(eval_dataset)} mẫu")

    # 2. Khởi tạo Unsloth hoặc HuggingFace Standard
    is_unsloth_success = False
    if use_unsloth or "unsloth" in model_name.lower():
        try:
            from unsloth import FastLanguageModel
            print("\n⚡ Kích hoạt Unsloth FastLanguageModel...")
            model, tokenizer = FastLanguageModel.from_pretrained(
                model_name=model_name,
                max_seq_length=max_seq_length,
                load_in_4bit=True,
                dtype=None,
                cache_dir=str(CACHE_DIR)
            )
            model = FastLanguageModel.get_peft_model(
                model,
                r=16,
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
                lora_alpha=32,
                lora_dropout=0,
                bias="none",
                use_gradient_checkpointing="unsloth",
                random_state=42,
            )
            is_unsloth_success = True
            print("✅ Đã khởi tạo Unsloth FastLanguageModel thành công!")
        except Exception as e:
            print(f"⚠️ Chưa khởi tạo được Unsloth Natively ({e}).")
            print("💡 Hãy chạy lệnh 'pip install unsloth_zoo' để kích hoạt đầy đủ Unsloth cho Gemma 4.")
            is_unsloth_success = False

    if not is_unsloth_success:
        from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

        print("\n⚙️ 2. Cấu hình BitsAndBytes 4-bit Quantization tiêu chuẩn...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16 if is_cuda_ok and torch.cuda.is_bf16_supported() else torch.float16,
            bnb_4bit_use_double_quant=True
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=str(CACHE_DIR), trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto" if is_cuda_ok else "cpu",
            cache_dir=str(CACHE_DIR),
            trust_remote_code=True
        )
        model = prepare_model_for_kbit_training(model)

        print("\n🛠️ 3. Thiết lập Cấu hình PEFT / LoRA...")
        # Đăng ký custom module class nếu dùng Gemma4ClippableLinear
        import peft.tuners.lora.model as lora_module
        try:
            for name, module in model.named_modules():
                class_name = module.__class__.__name__
                if "ClippableLinear" in class_name or "Gemma4" in class_name:
                    if hasattr(lora_module, "dispatch_default"):
                        pass
        except Exception:
            pass

        peft_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        try:
            model = get_peft_model(model, peft_config)
            model.print_trainable_parameters()
        except Exception as peft_err:
            print(f"❌ Lỗi cấu hình PEFT: {peft_err}")
            print("💡 Hãy cài 'unsloth_zoo' bằng lệnh: pip install unsloth_zoo")
            return

    # 3. Format dữ liệu theo Chat Template
    print("\n📝 4. Đang Format dữ liệu thành Prompt Gemma...")
    formatted_train = train_dataset.map(lambda x: format_messages_for_gemma(x, tokenizer), batched=True)
    formatted_eval = eval_dataset.map(lambda x: format_messages_for_gemma(x, tokenizer), batched=True)

    # 4. Huấn luyện với SFTTrainer
    from trl import SFTTrainer, SFTConfig

    training_args = SFTConfig(
        output_dir=str(output_dir),
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=2,
        num_train_epochs=num_epochs,
        optim="paged_adamw_8bit" if is_cuda_ok else "adamw_torch",
        fp16=is_cuda_ok and not torch.cuda.is_bf16_supported(),
        bf16=is_cuda_ok and torch.cuda.is_bf16_supported(),
        report_to="none"
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=formatted_train,
        eval_dataset=formatted_eval,
        tokenizer=tokenizer,
        args=training_args
    )

    print("\n🔥 5. Bắt đầu quá trình Huấn luyện QLoRA Fine-tuning...")
    trainer.train()

    print("\n💾 6. Lưu LoRA Adapter đã huấn luyện...")
    trainer.model.save_pretrained(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    print(f"✅ ĐÃ LƯU MODEL TẠI: {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fine-tune Gemma trên RTX 3060 12GB VRAM")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL_NAME, help="Hugging Face Model ID")
    parser.add_argument("--epochs", type=int, default=3, help="Số lượng Epochs")
    parser.add_argument("--batch_size", type=int, default=2, help="Batch size trên mỗi GPU")
    parser.add_argument("--grad_accum", type=int, default=4, help="Gradient accumulation steps")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--max_len", type=int, default=1024, help="Max Sequence Length")
    parser.add_argument("--unsloth", action="store_true", help="Kích hoạt tăng tốc Unsloth")

    args = parser.parse_args()

    run_training(
        model_name=args.model,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        max_seq_length=args.max_len,
        use_unsloth=args.unsloth
    )
