import re
from bs4 import BeautifulSoup

class TextCleaner:
    """Class xử lý và làm sạch văn bản y tế thô từ HTML / Web Scraping / Augmentation."""

    @staticmethod
    def clean_html(raw_html_or_text: str) -> str:
        if not raw_html_or_text:
            return ""

        if "<" in raw_html_or_text and ">" in raw_html_or_text:
            soup = BeautifulSoup(raw_html_or_text, "lxml")
            for element in soup(["script", "style", "nav", "header", "footer", "iframe"]):
                element.decompose()
            text = soup.get_text(separator=" ")
        else:
            text = raw_html_or_text

        # 1. Loại bỏ số điện thoại hotline, quảng cáo nhà thuốc, link
        text = re.sub(r"(Hotline|Điện thoại|SĐT|Liên hệ|Đặt lịch khám)[:\s]*[\d\.\-\s]{8,15}", "", text, flags=re.I)
        text = re.sub(r"https?://\S+", "", text)

        # 2. Xóa các cụm từ thừa của báo chí/bệnh viện
        text = re.sub(r"(Xem thêm tại|Xem thêm bài viết|Xem thêm|Nguồn tham khảo|Bản quyền thuộc về|Theo dõi thêm tại).*$", "", text, flags=re.I | re.S)

        # 3. Chuẩn hóa dấu câu rác (dấu phẩy kép `,,`, thừa đuôi `ạ? ạ?`, `cho tôi hỏi?`)
        text = re.sub(r",\s*,+", ",", text)
        text = re.sub(r"\?\s*\?+", "?", text)
        text = re.sub(r"(ạ\?|dạ\?|với ạ\?|cho tôi hỏi\?|ad cho mình hỏi\?)\s*(ạ\?|dạ\?|cho tôi hỏi\?|ad cho mình hỏi\?)+", r"\1", text, flags=re.I)

        # 4. Chuẩn hóa khoảng trắng
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def format_question(question: str) -> str:
        """Chuẩn hóa câu hỏi người dùng tự nhiên hơn."""
        q = TextCleaner.clean_html(question)
        q = re.sub(r"^(Hỏi|Khách hàng hỏi|Bệnh nhân hỏi|Thắc mắc)[:\s]*", "", q, flags=re.I).strip()

        # Sửa lỗi viết hoa đầu câu sau dấu phẩy
        q = re.sub(r"^([a-zàáảãạăắằẳẵặânấầnẩẫậnđèéẻẽẹêếềểễệiỉĩịòóỏõọôốồổỗộơớờởỡợuúủũụưứừửữựyỳỷỹỵ])", lambda m: m.group(1).upper(), q)
        return q

    @staticmethod
    def format_answer(answer: str) -> str:
        """Chuẩn hóa câu trả lời y tế."""
        a = TextCleaner.clean_html(answer)
        a = re.sub(r"^(Trả lời|Bác sĩ trả lời|Bác sĩ tư vấn|Giải đáp)[:\s]*", "", a, flags=re.I).strip()
        return a
