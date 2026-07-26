import asyncio
import re
from typing import List, Dict, Any
import httpx
from bs4 import BeautifulSoup

from crawlers.base_crawler import BaseCrawler
from config.settings import REQUEST_DELAY
from utils.logger import logger

class MedlatecCrawler(BaseCrawler):
    """Crawler thu thập dữ liệu tư vấn sức khỏe từ trang Medlatec."""

    def __init__(self):
        super().__init__(source_name="medlatec")
        self.base_url = "https://medlatec.vn"
        self.qa_url = "https://medlatec.vn/hoi-dap-bac-si"

    async def crawl(self, max_pages: int = 3) -> List[Dict[str, Any]]:
        logger.info(f"[{self.source_name}] Đang khởi động cào dữ liệu Medlatec (Max pages: {max_pages})...")
        results = []

        async with httpx.AsyncClient() as client:
            detail_urls = set()
            for page in range(1, max_pages + 1):
                url = f"{self.qa_url}?page={page}" if page > 1 else self.qa_url
                html = await self.fetch_html(client, url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "lxml")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/tin-tuc/" in href or "/hoi-dap-bac-si/" in href:
                        full_url = href if href.startswith("http") else f"{self.base_url}{href}"
                        if full_url != self.qa_url:
                            detail_urls.add(full_url)

                await asyncio.sleep(REQUEST_DELAY)

            logger.info(f"[{self.source_name}] Tìm thấy {len(detail_urls)} liên kết tư vấn.")

            for index, url in enumerate(detail_urls):
                try:
                    html = await self.fetch_html(client, url)
                    if not html:
                        continue

                    soup = BeautifulSoup(html, "lxml")
                    qa_pair = self._parse_medlatec(soup, url)
                    if qa_pair:
                        results.append(qa_pair)

                    await asyncio.sleep(REQUEST_DELAY)
                except Exception as e:
                    logger.error(f"[{self.source_name}] Lỗi bóc tách {url}: {e}")

        self.save_raw_data(results)
        return results

    def _parse_medlatec(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        title_el = soup.find("h1")
        title = title_el.get_text(strip=True) if title_el else ""

        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 15]

        if not paragraphs:
            return {}

        question = title
        answer = "\n".join(paragraphs[1:6]) if len(paragraphs) > 1 else "\n".join(paragraphs)

        if len(question) > 5 and len(answer) > 30:
            return {
                "source": "medlatec",
                "url": url,
                "title": title,
                "question": question,
                "answer": answer
            }
        return {}
