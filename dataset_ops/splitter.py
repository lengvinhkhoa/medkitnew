import json
import random
from pathlib import Path
from typing import List, Dict, Any
from config.settings import PROCESSED_DATA_DIR, SPLIT_RATIOS
from utils.logger import logger

class DatasetSplitter:
    """Phân bổ Dataset thành Train (85%), Eval (7.5%), Test (7.5%) bằng Phân tầng (Stratified Sampling)."""

    @staticmethod
    def split_dataset(
        dataset: List[Dict[str, Any]],
        ratios: Dict[str, float] = SPLIT_RATIOS,
        seed: int = 42
    ) -> Dict[str, Path]:
        random.seed(seed)

        # 1. Phân nhóm theo nhãn an toàn (Stratified Buckets)
        buckets = {
            "red_flag": [],
            "medication": [],
            "ambiguous": [],
            "general": []
        }

        for item in dataset:
            flags = item.get("metadata", {}).get("safety_flags", {})
            if flags.get("is_red_flag"):
                buckets["red_flag"].append(item)
            elif flags.get("is_medication"):
                buckets["medication"].append(item)
            elif flags.get("is_ambiguous"):
                buckets["ambiguous"].append(item)
            else:
                buckets["general"].append(item)

        train_data, eval_data, test_data = [], [], []

        # 2. Phân bổ đồng đều từ từng Bucket
        for cat_name, items in buckets.items():
            random.shuffle(items)
            n_total = len(items)
            n_eval = max(1, int(n_total * ratios["eval"])) if n_total >= 10 else int(n_total * ratios["eval"])
            n_test = max(1, int(n_total * ratios["test"])) if n_total >= 10 else int(n_total * ratios["test"])

            eval_subset = items[:n_eval]
            test_subset = items[n_eval:n_eval + n_test]
            train_subset = items[n_eval + n_test:]

            train_data.extend(train_subset)
            eval_data.extend(eval_subset)
            test_data.extend(test_subset)

        # Tráo ngẫu nhiên từng tập
        random.shuffle(train_data)
        random.shuffle(eval_data)
        random.shuffle(test_data)

        # 3. Ghi file JSONL
        splits = {
            "train": (PROCESSED_DATA_DIR / "train.jsonl", train_data),
            "eval": (PROCESSED_DATA_DIR / "eval.jsonl", eval_data),
            "test": (PROCESSED_DATA_DIR / "test.jsonl", test_data)
        }

        output_paths = {}
        logger.info("=== BÁO CÁO PHÂN BỔ DATASET TRAIN / EVAL / TEST ===")
        total_count = len(dataset)
        for split_name, (filepath, items) in splits.items():
            with open(filepath, "w", encoding="utf-8") as f:
                for entry in items:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            pct = (len(items) / total_count * 100) if total_count > 0 else 0
            logger.info(f"Tập [{split_name.upper()}]: {len(items)} mẫu ({pct:.1f}%) -> {filepath.name}")
            output_paths[split_name] = filepath
        logger.info("==================================================")

        return output_paths
