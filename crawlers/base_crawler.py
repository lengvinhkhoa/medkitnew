import asyncio
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import DEFAULT_HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY, MAX_RETRIES, RAW_DATA_DIR
from utils.logger import logger

class BaseCrawler(ABC):
    """Lớp cơ sở cho tất cả các web crawler y tế."""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.headers = DEFAULT_HEADERS.copy()
        self.output_file = RAW_DATA_DIR / f"{source_name}_raw.json"

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
        reraise=False
    )
    async def fetch_html(self, client: httpx.AsyncClient, url: str) -> Optional[str]:
        """Tải nội dung HTML từ URL với cơ chế tự động thử lại (Retry) khi gặp lỗi mạng."""
        try:
            response = await client.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT, follow_redirects=True)
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"[{self.source_name}] HTTP {response.status_code} khi truy cập {url}")
                return None
        except Exception as e:
            logger.error(f"[{self.source_name}] Lỗi fetch URL {url}: {e}")
            raise

    def save_raw_data(self, data: List[Dict[str, Any]]) -> None:
        """Lưu dữ liệu thô cào được vào thư mục data/raw dưới dạng JSON."""
        existing_data = []
        if self.output_file.exists():
            try:
                with open(self.output_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except Exception:
                existing_data = []
        
        existing_data.extend(data)
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        logger.info(f"[{self.source_name}] Đã lưu {len(data)} mẫu dữ liệu thô vào {self.output_file}")

    @abstractmethod
    async def crawl(self, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Phương thức cào dữ liệu chính cần được triển khai riêng cho từng trang web."""
        pass
