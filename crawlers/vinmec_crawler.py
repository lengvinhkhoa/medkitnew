import asyncio
import re
from typing import List, Dict, Any
import httpx
from bs4 import BeautifulSoup

from crawlers.base_crawler import BaseCrawler
from config.settings import REQUEST_DELAY
from utils.logger import logger

class VinmecCrawler(BaseCrawler):
    """Crawler chuyên thu thập dữ liệu Hỏi - Đáp Bác sĩ từ hệ thống Y tế Vinmec."""

    def __init__(self):
        super().__init__(source_name="vinmec")
        self.base_url = "https://www.vinmec.com"
        self.qa_section_url = "https://www.vinmec.com/vi/hoi-dap-bac-si/"

    async def crawl(self, max_pages: int = 3) -> List[Dict[str, Any]]:
        logger.info(f"[{self.source_name}] Đang khởi động cào dữ liệu Vinmec (Max pages: {max_pages})...")
        results = []

        async with httpx.AsyncClient() as client:
            # 1. Thu thập danh sách đường dẫn bài viết Hỏi-Đáp
            detail_urls = set()
            for page in range(1, max_pages + 1):
                page_url = f"{self.qa_section_url}?page={page}" if page > 1 else self.qa_section_url
                html = await self.fetch_html(client, page_url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "lxml")
                # Lấy tất cả các thẻ a chứa liên kết bài hỏi đáp
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/vi/hoi-dap-bac-si/" in href or "/vi/tin-tuc/thong-tin-suc-khoe/" in href:
                        full_url = href if href.startswith("http") else f"{self.base_url}{href}"
                        if full_url != self.qa_section_url:
                            detail_urls.add(full_url)
                
                await asyncio.sleep(REQUEST_DELAY)

            logger.info(f"[{self.source_name}] Tìm thấy {len(detail_urls)} liên kết Hỏi-Đáp.")

            # 2. Bóc tách chi tiết từng bài viết Hỏi - Đáp
            for index, url in enumerate(detail_urls):
                try:
                    html = await self.fetch_html(client, url)
                    if not html:
                        continue

                    soup = BeautifulSoup(html, "lxml")
                    qa_pair = self._parse_detail_page(soup, url)
                    if qa_pair:
                        results.append(qa_pair)

                    if (index + 1) % 5 == 0:
                        logger.info(f"[{self.source_name}] Đã xử lý {index + 1}/{len(detail_urls)} bài viết.")

                    await asyncio.sleep(REQUEST_DELAY)
                except Exception as e:
                    logger.error(f"[{self.source_name}] Lỗi khi bóc tách {url}: {e}")

        self.save_raw_data(results)
        return results

    def _parse_detail_page(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Bóc tách câu hỏi và câu trả lời từ trang chi tiết Vinmec."""
        title_el = soup.find("h1") or soup.find("title")
        title = title_el.get_text(strip=True) if title_el else ""

        # Tìm vùng nội dung chính
        content_div = soup.find("div", class_=re.compile(r"content|main-content|detail-content|article-content", re.I))
        if not content_div:
            content_div = soup.body

        if not content_div:
            return {}

        text_content = content_div.get_text(separator="\n", strip=True)

        # Phân tách Hỏi và Độc giả / Bác sĩ trả lời
        question = ""
        answer = ""

        # Thử tìm các phần tiêu đề Hỏi & Trả lời phổ biến
        sections = re.split(r"(Hỏi:|Khách hàng hỏi:|Trả lời:|Bác sĩ tư vấn:|Bác sĩ trả lời:)", text_content, flags=re.I)
        
        if len(sections) >= 3:
            for i in range(1, len(sections) - 1, 2):
                header = sections[i].lower()
                body = sections[i+1].strip()
                if "hỏi" in header:
                    question += body + " "
                elif "trả lời" in header or "tư vấn" in header:
                    answer += body + " "
        else:
            # Fallback nếu không chia rõ rệt
            question = title
            paragraphs = content_div.find_all("p")
            answer = "\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])

        question = question.strip()
        answer = answer.strip()

        if len(question) > 10 and len(answer) > 30:
            return {
                "source": "vinmec",
                "url": url,
                "title": title,
                "question": question,
                "answer": answer
            }
        return {}
