"""
Trình tạo dữ liệu Y tế mẫu (Synthetic Data Generator) phục vụ kiểm thử và tạo dữ liệu ban đầu
đúng chuẩn các trường hợp bắt buộc (Red flags, câu hỏi thuốc, câu hỏi mơ hồ, câu hỏi thông thường).
"""

from typing import List, Dict, Any
from crawlers.base_crawler import BaseCrawler
from utils.logger import logger

SAMPLE_PATIENT_QA_DATA = [
    # Case 1: Thông thường / Nhẹ
    {
        "source": "sample_data",
        "url": "https://example.com/medical/1",
        "title": "Bị đau bụng nhẹ bên phải sau khi ăn đồ nhiều mỡ",
        "question": "Em bị đau bụng nhẹ bên phải sau khi ăn đồ chiên xào nhiều mỡ, có bị làm sao không ạ?",
        "answer": "Chào em, tình trạng đau bụng nhẹ ở hạ sườn phải sau khi ăn đồ dầu mỡ thường do đường tiêu hóa bị quá tải, dạ dày hoặc túi mật co bóp mạnh để tiêu hóa chất béo. Mức độ hiện tại là nhẹ-vừa. Em nên: (1) Tránh thức ăn nhiều dầu mỡ, đồ cay nóng, (2) Uống nhiều nước ấm, nghỉ ngơi nhẹ nhàng, (3) Theo dõi thêm từ 24-48 giờ. Em nên đi khám nếu đau tăng dần, sốt hoặc nôn ói."
    },
    # Case 2: Trẻ em sốt nhẹ/vừa (Ví dụ của User)
    {
        "source": "sample_data",
        "url": "https://example.com/medical/2",
        "title": "Con 3 tuổi sốt 38.5 độ",
        "question": "Con em 3 tuổi sốt 38.5 độ, có cần đi viện không ạ?",
        "answer": "Chào anh/chị, với bé 3 tuổi sốt 38.5°C, đây là mức sốt nhẹ-vừa. Anh/chị có thể: (1) Cho bé uống nhiều nước hoặc oresol, (2) Hạ sốt bằng paracetamol theo liều cân nặng (10-15mg/kg mỗi 4-6h), (3) Lau mát nách bẹn và theo dõi thêm 24h. Cần đưa bé đi khám NGAY nếu: sốt trên 39°C không hạ, co giật, li bì, bỏ ăn/bú, phát ban. Đây chỉ là thông tin tham khảo, nếu lo lắng anh/chị nên đưa bé đi khám trực tiếp."
    },
    # Case 3: Red Flag 1 - Đau ngực thắt lan ra tay
    {
        "source": "sample_data",
        "url": "https://example.com/medical/3",
        "title": "Đau thắt ngực trái lan ra tay",
        "question": "Bố em 58 tuổi đột ngột bị đau thắt ngực bên trái lan ra vai và tay trái, vã mồ hôi hột thì làm sao ạ?",
        "answer": "Tình trạng đau thắt ngực trái lan ra vai/tay kèm vã mồ hôi hột ở người trung niên là DẤU HIỆU NGUY CẤP nghi ngờ cơn cơ thắt mạch vị hoặc NMCT (Nhồi máu cơ tim). Mức độ: CỰC KỲ NGHIÊM TRỌNG. Khuyến nghị hành động NGAY LẬP TỨC: (1) Cho bác nằm nghỉ nơi thoáng mát, (2) Nhanh chóng gọi Cấp cứu 115 hoặc đưa bác đến bệnh viện có khoa Tim mạch gần nhất NGAY LẬP TỨC, không tự đi xe máy hay chờ đợi theo dõi tại nhà."
    },
    # Case 4: Red Flag 2 - Đột quỵ / Méo miệng
    {
        "source": "sample_data",
        "url": "https://example.com/medical/4",
        "title": "Người nhà bị méo miệng nói ngọng đột ngột",
        "question": "Mẹ em đang ngồi xem tivi tự nhiên bị méo miệng, nói ngọng và tay phải không giơ lên được, có sao không?",
        "answer": "Các triệu chứng méo miệng, nói ngọng, yếu một bên tay xuất hiện đột ngột là DẤU HIỆU ĐỘT QUỴ (Tai biến mạch máu não). Đây là tình trạng CẤP CỨU Y TẾ NGUY CẤP. Anh/chị cần hành động ngay: (1) Gọi ngay Cấp cứu 115 hoặc đưa bác đến ngay bệnh viện có trung tâm Đột quỵ trong 'giờ vàng', (2) Đặt bác nằm nghiêng sang một bên nếu nôn ói, tuyệt đối KHÔNG cạo gió, KHÔNG cho ăn uống hay uống bất kỳ thuốc gì tại nhà."
    },
    # Case 5: Hỏi về Thuốc & Liều lượng
    {
        "source": "sample_data",
        "url": "https://example.com/medical/5",
        "title": "Tự mua kháng sinh Amoxicillin uống",
        "question": "Em bị ho đau họng 2 ngày nay, tự mua Amoxicillin 500mg uống ngày 4 viên được không?",
        "answer": "Chào em, Amoxicillin là thuốc kháng sinh chỉ có tác dụng diệt vi khuẩn, không có tác dụng với các trường hợp viêm họng do virus (chiếm 80-90% các ca ho đau họng thông thường). Việc tự ý dùng kháng sinh không đúng liều có thể gây dị ứng, loạn khuẩn ruột và nguy hiểm nhất là ĐỀ KHÁNG KHÁNG SINH. Em nên: (1) Súc họng bằng nước muối sinh lý, uống nước ấm ngậm mật tinh nghệ, (2) Tham khảo ý kiến Dược sĩ hoặc Bác sĩ để được khám và kê đơn đúng chủng loại nếu cần thiết."
    },
    # Case 6: Câu hỏi Mơ hồ / Thiếu thông tin
    {
        "source": "sample_data",
        "url": "https://example.com/medical/6",
        "title": "Bị nhức đầu",
        "question": "Em bị nhức đầu thì uống thuốc gì hết vậy ạ?",
        "answer": "Chào bạn, nhức đầu có thể do rất nhiều nguyên nhân khác nhau như: căng thẳng mệt mỏi, thiếu ngủ, thay đổi thời tiết, huyết áp cao, hoặc vấn đề về thần kinh. Do thông tin bạn cung cấp còn khá ngắn gọn, bạn có thể chia sẻ thêm: (1) Bạn bị đau ở vùng nào (nửa đầu, sau óc, trán)? (2) Đau dữ dội hay âm ỉ và đã kéo dài bao lâu? (3) Có kèm theo sốt, buồn nôn hay mờ mắt không? Nếu đau nhẹ do căng thẳng, bạn có thể nghỉ ngơi, uống đủ nước. Nếu đau dữ dội đột ngột hoặc kèm triệu chứng bất thường, bạn nên đi khám bác sĩ để được chẩn đoán chính xác."
    }
]

class SampleGenerator(BaseCrawler):
    """Trình tạo dữ liệu mẫu chất lượng cao phục vụ sẵn cho Fine-Tuning."""

    def __init__(self):
        super().__init__(source_name="sample_generator")

    async def crawl(self, max_pages: int = 1) -> List[Dict[str, Any]]:
        logger.info(f"[{self.source_name}] Đang nạp {len(SAMPLE_PATIENT_QA_DATA)} mẫu dữ liệu Y tế chuẩn...")
        self.save_raw_data(SAMPLE_PATIENT_QA_DATA)
        return SAMPLE_PATIENT_QA_DATA
