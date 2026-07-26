import argparse
import asyncio
import json
from pathlib import Path

from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR
from crawlers.sample_generator import SampleGenerator
from crawlers.vinmec_crawler import VinmecCrawler
from crawlers.medlatec_crawler import MedlatecCrawler
from processors.formatter import DataFormatter
from verification.verifier_pipeline import MedicalDataVerifierPipeline
from dataset_ops.generator_10k import Medical10kGenerator
from dataset_ops.splitter import DatasetSplitter
from dataset_ops.auditor import PhysicianAuditor
from utils.exporter import DatasetValidator
from utils.logger import logger

def process_and_verify_pipeline() -> Path:
    """Đọc tất cả file JSON thô trong data/raw, làm sạch, chạy bộ Verify 4 Lớp, phân bổ Train/Eval/Test và xuất audit."""
    raw_files = list(RAW_DATA_DIR.glob("*.json"))
    all_raw_items = []
    if raw_files:
        for rf in raw_files:
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    items = json.load(f)
                    all_raw_items.extend(items)
                    logger.info(f"Đọc {len(items)} mẫu từ {rf.name}")
            except Exception as e:
                logger.error(f"Lỗi đọc file {rf}: {e}")

    formatter = DataFormatter()
    raw_formatted_dataset = formatter.format_to_gemma_messages(all_raw_items)

    verifier = MedicalDataVerifierPipeline(enable_llm_critic=False)
    verification_result = verifier.run_pipeline(raw_formatted_dataset)
    verified_dataset = verification_result["passed_dataset"]

    output_path = formatter.export_to_jsonl(verified_dataset, "patient_medical_dataset.jsonl")
    DatasetSplitter.split_dataset(verified_dataset)
    PhysicianAuditor.extract_audit_sample(verified_dataset)
    DatasetValidator.validate_and_summarize(output_path)
    return output_path

async def main_async():
    parser = argparse.ArgumentParser(description="Tool Cào, Verify 4 Lớp & Sinh Dữ liệu Y tế Việt Nam Quy Mô 10K cho Gemma 4 e2b")
    parser.add_argument("action", choices=["sample", "generate10k", "crawl", "process", "verify", "split", "audit", "validate"], help="Hành động cần thực hiện")
    parser.add_argument("--source", choices=["vinmec", "medlatec", "all"], default="vinmec", help="Nguồn cần cào")
    parser.add_argument("--pages", type=int, default=2, help="Số trang cần cào")
    parser.add_argument("--target", type=int, default=10000, help="Mục tiêu số lượng mẫu sạch (Default: 10000)")

    args = parser.parse_args()

    if args.action == "generate10k":
        logger.info(f"[START] Đang khởi chạy Trình sinh & Verify Dữ liệu mục tiêu {args.target} mẫu...")
        
        # Đọc dữ liệu thô cào được nếu có
        raw_files = list(RAW_DATA_DIR.glob("*.json"))
        crawled_items = []
        for rf in raw_files:
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    crawled_items.extend(json.load(f))
            except Exception:
                pass

        generator = Medical10kGenerator(target_count=args.target)
        dataset = generator.generate_10k_dataset(crawled_items)
        DatasetValidator.validate_and_summarize(PROCESSED_DATA_DIR / "patient_medical_dataset.jsonl")

    elif args.action == "sample":
        logger.info("[START] Đang khởi chạy Trình tạo Dữ liệu mẫu (Sample Generator)...")
        gen = SampleGenerator()
        await gen.crawl()
        process_and_verify_pipeline()

    elif args.action == "crawl":
        logger.info(f"[START] Đang khởi chạy Crawler nguồn [{args.source}] (Max pages: {args.pages})...")
        if args.source == "vinmec" or args.source == "all":
            crawler = VinmecCrawler()
            await crawler.crawl(max_pages=args.pages)
        if args.source == "medlatec" or args.source == "all":
            crawler = MedlatecCrawler()
            await crawler.crawl(max_pages=args.pages)

        process_and_verify_pipeline()

    elif args.action == "process" or args.action == "verify":
        logger.info("[START] Đang xử lý & Chạy BỘ VERIFY 4 LỚP trên toàn bộ dữ liệu...")
        process_and_verify_pipeline()

    elif args.action == "split":
        dataset_path = PROCESSED_DATA_DIR / "patient_medical_dataset.jsonl"
        if dataset_path.exists():
            dataset = []
            with open(dataset_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        dataset.append(json.loads(line))
            DatasetSplitter.split_dataset(dataset)

    elif args.action == "audit":
        dataset_path = PROCESSED_DATA_DIR / "patient_medical_dataset.jsonl"
        if dataset_path.exists():
            dataset = []
            with open(dataset_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        dataset.append(json.loads(line))
            PhysicianAuditor.extract_audit_sample(dataset)

    elif args.action == "validate":
        dataset_path = PROCESSED_DATA_DIR / "patient_medical_dataset.jsonl"
        DatasetValidator.validate_and_summarize(dataset_path)

if __name__ == "__main__":
    asyncio.run(main_async())
