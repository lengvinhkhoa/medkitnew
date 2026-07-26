import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# OpenRouter LLM Critic Settings (Lớp 4 Verification)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "inclusionai/ling-3.0-flash:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Dataset Splitting Ratios (Total 100%)
SPLIT_RATIOS = {
    "train": 0.85,  # 85% (~8,500 samples for 10k goal)
    "eval": 0.075,  # 7.5% (~750 samples)
    "test": 0.075   # 7.5% (~750 samples)
}

# Audit Sample Percentage for Manual Physician Review
AUDIT_SAMPLE_RATIO = 0.15  # 15% sample for human audit

# Crawler Settings
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

REQUEST_TIMEOUT = 20.0
REQUEST_DELAY = 1.0
MAX_RETRIES = 3

# Gemma 4 e2b System Prompt
DEFAULT_SYSTEM_PROMPT = (
    "Bạn là trợ lý tư vấn sức khỏe thông minh và tận tâm dành cho người dùng phổ thông tại Việt Nam. "
    "Nhiệm vụ của bạn là giải thích nguyên nhân/khả năng dễ hiểu bằng ngôn ngữ đời thường, "
    "đánh giá mức độ nghiêm trọng (Nhẹ / Cần theo dõi / Cần đi khám ngay), "
    "và đưa ra hướng dẫn hành động tiếp theo phù hợp. "
    "LƯU Ý QUAN TRỌNG: Bạn KHÔNG chẩn đoán bệnh thay thế bác sĩ và luôn nhấn mạnh đi khám trực tiếp khi có dấu hiệu bất thường."
)
