"""
Bộ quy tắc & Từ khóa nhận diện Y Tế phục vụ lọc dữ liệu và kiểm soát an toàn AI (Safety Engine).
"""

# Các từ khóa triệu chứng nguy cấp (Red Flags) - Bắt buộc hướng dẫn đi cấp cứu/khám ngay
RED_FLAGS_KEYWORDS = [
    # Tim mạch & Hô hấp
    "đau ngực dữ dội", "đau thắt ngực", "vã mồ hôi hột", "khó thở dữ dội", 
    "tím tái môi", "tím ngón tay", "thở ngáp", "thở khò khè nặng",
    
    # Thần kinh & Đột quỵ
    "méo miệng", "tê yếu nửa người", "nói ngọng đột ngột", "mất thị lực đột ngột",
    "đau đầu dữ dội chưa từng có", "co giật", "mất ý thức", "ngất xỉu", "li bì", "hôn mê",
    
    # Tiêu hóa & Chấn thương / Xuất huyết
    "nôn ra máu", "đi ngoài phân đen như bã cà phê", "đau bụng dữ dội", "bụng cứng như gỗ",
    "chấn thương đầu", "chảy máu không cầm được", "gãy xương",
    
    # Trẻ em & Sơ sinh
    "trẻ sốt cao co giật", "sốt trên 39 độ không hạ", "bỏ bú hoàn toàn",
    "thóp phồng", "trẻ lừ đừ không linh hoạt", "phát ban dạng xuất huyết"
]

# Từ khóa liên quan đến Thuốc & Liều lượng - Bắt buộc khuyến cáo hỏi dược sĩ/bác sĩ
MEDICATION_KEYWORDS = [
    "kháng sinh", "liều lượng", "uống mấy viên", "uống thuốc gì",
    "tác dụng phụ của thuốc", "uống quá liều", "kê đơn", "đơn thuốc",
    "paracetamol", "ibuprofen", "amoxicillin", "corticoid", "aspirin"
]

# Cấu trúc khuyến cáo bổ sung cho Red Flag
EMERGENCY_DISCLAIMER = (
    "\n\n⚠️ **CẢNH BÁO NGUY CẤP:** Các triệu chứng trên có thể là dấu hiệu của tình trạng y tế cấp cứu. "
    "Anh/chị cần đưa bệnh nhân đến **cơ sở y tế gần nhất** hoặc gọi **Cấp cứu 115** NGAY LẬP TỨC để được xử trí kịp thời!"
)

MEDICATION_DISCLAIMER = (
    "\n\n💊 **LƯU Ý VỀ THUỐC:** Việc dùng thuốc (đặc biệt là kháng sinh và thuốc kê đơn) cần có chỉ định chính xác từ Bác sĩ hoặc Dược sĩ dựa trên tình trạng cụ thể. "
    "Không tự ý mua hoặc thay đổi liều lượng thuốc khi chưa có ý kiến chuyên môn."
)

AMBIGUOUS_QUESTION_GUIDANCE = (
    "\n\n❓ **CẦN THÊM THÔNG TIN:** Thông tin anh/chị cung cấp còn khá ngắn gọn. Để hỗ trợ tốt hơn, anh/chị có thể chia sẻ thêm: "
    "(1) Triệu chứng xuất hiện từ bao giờ? (2) Mức độ đau/khó chịu thế nào? (3) Đã dùng thuốc gì chưa hoặc có bệnh lý nền nào không?"
)
