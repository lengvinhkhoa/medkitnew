"""
Kho Dữ Liệu Hạt Giống Y Tế (Medical Seed Knowledge Base)
Phiên bản chất lượng cao - 52 seeds, 10 chuyên khoa + mơ hồ
Mỗi seed có placeholder {AGE} và {DEMO_REF} để đồng bộ tuổi tuyệt đối.
"""
SEED_MEDICAL_DATABASE = [
    # ======================== 1. NHI KHOA (6 seeds) ========================
    {
        "category": "Nhi khoa",
        "question": "Con em {AGE} sốt 38.5 độ, bé vẫn vui chơi bình thường thì có cần đi viện không ạ?",
        "answer": "Với {DEMO_REF} sốt 38.5°C nhưng vẫn tỉnh táo vui chơi, đây là mức sốt nhẹ-vừa do phản ứng miễn dịch. Anh/chị có thể: (1) Cho bé uống nhiều nước hoặc oresol, (2) Dùng paracetamol liều 10-15mg/kg mỗi 4-6 giờ nếu bé khó chịu, (3) Mặc quần áo thoáng mát, theo dõi 24-48h. Cần đưa bé đi khám NGAY nếu: sốt trên 39°C không hạ, co giật, lừ đừ, bỏ bú/ăn hoặc phát ban bất thường.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Nhi khoa",
        "question": "Bé {AGE} sốt 39.5 độ co giật mắt trợn ngược thì phải làm gì cấp cứu ạ?",
        "answer": "Trẻ sốt cao co giật trợn ngược mắt là DẤU HIỆU CẤP CỨU NGUY CẤP! Anh/chị cần xử trí khẩn cấp: (1) Đặt bé nằm nghiêng trên mặt phẳng thoáng mát để tránh sặc, (2) TUYỆT ĐỐI KHÔNG nhét vật gì vào miệng bé hay giữ chặt tay chân, (3) Đưa bé đến BỆNH VIỆN hoặc gọi CẤP CỨU 115 NGAY LẬP TỨC.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Nhi khoa",
        "question": "Bé {AGE} bị đi ngoài phân sống uống men vi sinh gì tốt ạ?",
        "answer": "Đi ngoài phân sống ở {DEMO_REF} thường do hệ vi sinh đường ruột chưa hoàn thiện hoặc quá tải thức ăn. Anh/chị có thể bổ sung men vi sinh chứa chủng Lactobacillus hoặc Bifidobacterium. Nếu bé đi ngoài kéo dài trên 3 ngày, phân có nhầy máu hoặc sụt cân, hãy đưa bé đi khám bác sĩ Nhi khoa.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Nhi khoa",
        "question": "Bé {AGE} bị ho hắng sổ mũi nước trong 2 ngày nay thì có cần uống kháng sinh không?",
        "answer": "Ho sổ mũi nước trong ở {DEMO_REF} đa phần do cảm lạnh virus thông thường. TUYỆT ĐỐI KHÔNG tự ý cho bé uống kháng sinh vì không diệt được virus. Anh/chị nên: (1) Rửa mũi bằng nước muối sinh lý, (2) Cho bé uống siro ho thảo dược, (3) Theo dõi nhiệt độ. Đưa bé đi khám nếu thở nhanh, rút lõm ngực hoặc sốt cao.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Nhi khoa",
        "question": "Bé {AGE} bị nổi nốt mụn nước ở tay chân và miệng là bệnh gì?",
        "answer": "Mụn nước ở tay chân và niêm mạc miệng ở {DEMO_REF} là dấu hiệu điển hình của bệnh TAY CHÂN MIỆNG. Mức độ cần theo dõi sát. Anh/chị nên: (1) Cách ly bé, cho ăn thức ăn mềm nguội, (2) Bù nước, dùng paracetamol nếu sốt, (3) Đi khám ngay nếu giật mình chới với, đi thắt giật, sốt cao không hạ.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Nhi khoa",
        "question": "Bé {AGE} bị ho từng cơn về đêm kèm thở khò khè là bệnh gì?",
        "answer": "Ho từng cơn về đêm kèm khò khè ở {DEMO_REF} là dấu hiệu nghi ngờ HEN PHẾ QUẢN hoặc VIÊM TIỂU PHẾ QUẢN. Anh/chị nên: (1) Giữ ấm cho bé, tránh tiếp xúc khói bụi, lông thú, (2) Cho bé uống nhiều nước ấm, (3) Đưa bé đi khám chuyên khoa Hô hấp Nhi để được đo chức năng hô hấp và điều trị dự phòng hen.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },

    # ======================== 2. TIM MẠCH (5 seeds) ========================
    {
        "category": "Tim mạch",
        "question": "Bố em {AGE} bị đau thắt ngực trái lan ra vai trái và tay trái, vã mồ hôi hột thì có nguy hiểm không?",
        "answer": "CẢNH BÁO NGUY CẤP: Đau thắt ngực trái lan ra vai/tay trái kèm vã mồ hôi ở {DEMO_REF} là dấu hiệu điển hình của CƠN NHỒI MÁU CƠ TIM CẤP! Cần xử trí NGAY: (1) Cho bác nằm nghỉ nơi thoáng mát, thả lỏng quần áo, (2) Gọi CẤP CỨU 115 hoặc đưa bác đến bệnh viện có khoa Tim mạch gần nhất NGAY trong 'giờ vàng'.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tim mạch",
        "question": "Thỉnh thoảng em bị thắt tim nhói nhẹ 1-2 giây rồi hết có sao không ạ?",
        "answer": "Đau nhói tim ngắn vài giây ở {DEMO_REF} thường liên quan đến đau thần kinh liên sườn hoặc căng thẳng tâm lý, ít nguy cơ tim mạch cấp. Em nên: (1) Tránh thức khuya, giảm cà phê, (2) Tập hít thở sâu, thư giãn. Đi khám chuyên khoa Tim mạch nếu cơn đau thường xuyên hơn, kéo dài trên 5 phút hoặc kèm khó thở.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tim mạch",
        "question": "Mẹ em {AGE} đo huyết áp tại nhà thấy 170/100 mmHg kèm đau đầu nhẹ thì nên làm gì?",
        "answer": "Chỉ số 170/100 mmHg ở {DEMO_REF} là mức TĂNG HUYẾT ÁP ĐỘ 2. Anh/chị cần: (1) Cho bác nghỉ ngơi 15 phút rồi đo lại, (2) Cho uống thuốc huyết áp theo đơn bác sĩ (nếu có), (3) KHÔNG uống cà phê hay xoa dầu nóng. Đưa bác đến cơ sở y tế nếu huyết áp tiếp tục tăng hoặc kèm mờ mắt, tức ngực.",
        "is_red_flag": True, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Tim mạch",
        "question": "Em {AGE} bị phù chân và khó thở khi nằm thì có bị suy tim không?",
        "answer": "Phù chân kèm khó thở khi nằm ở {DEMO_REF} là dấu hiệu nghi ngờ SUY TIM. Đây là tình trạng cần đi khám sớm. Em nên: (1) Hạn chế muối, nước, nằm đầu cao, (2) Không tự ý dùng thuốc lợi tiểu, (3) Đi khám chuyên khoa Tim mạch để siêu âm tim và điện tim đồ kiểm tra chức năng tim.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tim mạch",
        "question": "Bố em {AGE} hay bị tức ngực mỗi khi đi bộ nhanh hoặc lên cầu thang là bệnh gì?",
        "answer": "Đau tức ngực khi gắng sức ở {DEMO_REF} là triệu chứng điển hình của THIẾU MÁU CƠ TIM (Đau thắt ngực ổn định). Em nên: (1) Cho bố đi khám chuyên khoa Tim mạch để làm điện tim và nghiệm pháp gắng sức, (2) Dùng thuốc theo đúng đơn bác sĩ, (3) Tránh gắng sức đột ngột, kiểm soát huyết áp và mỡ máu.",
        "is_red_flag": True, "is_medication": True, "is_ambiguous": False
    },

    # ======================== 3. HÔ HẤP (5 seeds) ========================
    {
        "category": "Hô hấp",
        "question": "Em {AGE} bị ho khan rát họng 3 ngày nay tự mua Amoxicillin uống được không bác sĩ?",
        "answer": "Amoxicillin là kháng sinh chỉ diệt vi khuẩn, không có tác dụng với ho do virus (chiếm 80-90% viêm họng thông thường). Tự ý uống kháng sinh gây kháng thuốc và rối loạn tiêu hóa. Em nên: (1) Súc họng nước muối sinh lý, uống nước ấm pha mật ong, (2) Dùng siro ho thảo dược. Gặp bác sĩ nếu ho kéo dài trên 7 ngày hoặc sốt cao.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Hô hấp",
        "question": "Bệnh nhân {AGE} thở ngáp tím tái môi thì cần cấp cứu như nào?",
        "answer": "Thở ngáp kèm tím tái môi ở {DEMO_REF} là DẤU HIỆU SUY HÔ HẤP NGUY CẤP! Anh/chị cần hành động NGAY: (1) Gọi CẤP CỨU 115, (2) Nâng cao đầu, khai thông đường thở, (3) Ép tim hô hấp nhân tạo (CPR) nếu bệnh nhân ngừng thở.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Hô hấp",
        "question": "Em {AGE} bị ho kéo dài hơn 3 tuần, ho nhiều về đêm và sáng sớm kèm đờm trắng thì là bệnh gì?",
        "answer": "Ho kéo dài trên 3 tuần ở {DEMO_REF} cần cảnh giác với viêm phế quản mạn, hen phế quản, trào ngược dạ dày thực quản hoặc lao phổi. Em nên: (1) Tránh khói thuốc, bụi bẩn, giữ ấm cổ, (2) Đi khám chuyên khoa Hô hấp để chụp X-quang phổi và xét nghiệm đờm.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Hô hấp",
        "question": "Em {AGE} bị khó thở, tức ngực kèm sốt cao 39.5 độ, ho đờm vàng xanh thì có bị viêm phổi không?",
        "answer": "Khó thở tức ngực kèm sốt cao và ho đờm vàng xanh ở {DEMO_REF} là dấu hiệu nghi ngờ VIÊM PHỔI. Cần đi khám NGAY. Kỹ thuật viên y tế sẽ nghe phổi, chụp X-quang và xét nghiệm máu. Đây là tình trạng cần nhập viện dùng kháng sinh tĩnh mạch, không tự điều trị tại nhà.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Hô hấp",
        "question": "Em {AGE} bị ho có đờm kéo dài sau khi bị cảm cúm thì nên uống thuốc gì?",
        "answer": "Ho có đờm kéo dài sau cúm ở {DEMO_REF} thường do tổn thương niêm mạc đường hô hấp sau nhiễm virus. Em nên: (1) Uống nhiều nước ấm, mật ong gừng, (2) Dùng thuốc long đờm như acetylcystein nếu đờm đặc quánh, (3) Nếu ho kéo dài trên 14 ngày hoặc kèm sốt trở lại, hãy đi khám để loại trừ bội nhiễm.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },

    # ======================== 4. THẦN KINH (5 seeds) ========================
    {
        "category": "Thần kinh",
        "question": "Người nhà em {AGE} đang ngồi tự nhiên bị méo miệng, nói ngọng và yếu nửa người bên phải làm sao ạ?",
        "answer": "Méo miệng, nói ngọng, yếu nửa người ở {DEMO_REF} là 3 DẤU HIỆU VÀNG CỦA ĐỘT QUỴ. Tình trạng CỰC KỲ NGUY CẤP! Anh/chị cần: (1) Gọi CẤP CỨU 115 hoặc đưa đến Trung tâm Đột quỵ trong 'giờ vàng', (2) Đặt bệnh nhân nằm nghiêng, TUYỆT ĐỐI KHÔNG cạo gió, nặn máu tai hay cho ăn uống.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Thần kinh",
        "question": "Em {AGE} bị đau nhức đầu âm ỉ sau khi thức khuya làm việc căng thẳng thì uống thuốc gì?",
        "answer": "Đau đầu âm ỉ sau thức khuya căng thẳng ở {DEMO_REF} thường là đau đầu do căng cơ. Mức độ nhẹ. Em có thể: (1) Nghỉ ngơi trong phòng tối yên tĩnh, chườm ấm cổ vai, (2) Uống đủ 2 lít nước/ngày, (3) Có thể dùng Paracetamol 500mg nếu quá khó chịu. Đi khám nếu đau đầu dữ dội đột ngột hoặc kèm nôn mờ mắt.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Thần kinh",
        "question": "Đột nhiên em {AGE} bị đau đầu dữ dội chưa từng có kèm nôn ói và cứng cổ thì có phải cấp cứu không?",
        "answer": "Đau đầu dữ dội đột ngột kèm nôn ói và cứng cổ ở {DEMO_REF} là DẤU HIỆU NGUY CẤP nghi ngờ xuất huyết dưới nhện hoặc viêm màng não! Cần xử trí NGAY: (1) Gọi CẤP CỨU 115 hoặc đưa đến khoa Cấp cứu gần nhất, (2) Giữ bệnh nhân nằm yên, tránh ánh sáng mạnh.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Thần kinh",
        "question": "Em {AGE} hay bị chóng mặt quay cuồng mỗi khi thay đổi tư thế nằm ngồi là bệnh gì?",
        "answer": "Chóng mặt quay cuồng khi thay đổi tư thế ở {DEMO_REF} là dấu hiệu điển hình của Chóng mặt tư thế lành tính (BPPV) do sỏi tai. Đây là bệnh lành tính nhưng gây khó chịu. Em nên: (1) Không xoay đầu đột ngột, (2) Tập thao tác Epley theo hướng dẫn chuyên khoa Thần kinh hoặc Tai Mũi Họng, (3) Nếu chóng mặt kèm ù tai nghe kém thì đi khám sớm.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Thần kinh",
        "question": "Em {AGE} bị tê bì tay chân, cảm giác như kiến bò về đêm là thiếu vitamin gì?",
        "answer": "Tê bì tay chân cảm giác kiến bò ở {DEMO_REF} thường do thiếu vitamin nhóm B (B1, B6, B12) hoặc chèn ép thần kinh ngoại biên. Em nên: (1) Bổ sung thực phẩm giàu vitamin B (thịt, trứng, sữa, rau xanh, ngũ cốc nguyên cám), (2) Hạn chế rượu bia, (3) Nếu tê bì kéo dài, đi khám Thần kinh để làm điện cơ đồ kiểm tra dẫn truyền thần kinh.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },

    # ======================== 5. TIÊU HÓA (5 seeds) ========================
    {
        "category": "Tiêu hóa",
        "question": "Em {AGE} bị đau bụng bên phải sau khi ăn đồ mỡ có sao không ạ?",
        "answer": "Đau bụng hạ sườn phải sau ăn dầu mỡ ở {DEMO_REF} thường liên quan đến quá tải dạ dày hoặc túi mật. Mức độ nhẹ-vừa. Em nên: (1) Hạn chế đồ chiên xào, rượu bia, (2) Uống trà gừng ấm, theo dõi 24-48h. Đi khám ngay nếu đau tăng dữ dội, sốt cao hoặc vàng da.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tiêu hóa",
        "question": "Bệnh nhân {AGE} nôn ra máu tươi và đi ngoài phân đen như bã cà phê có nguy hiểm không?",
        "answer": "Nôn ra máu tươi kèm phân đen ở {DEMO_REF} là DẤU HIỆU XUẤT HUYẾT TIÊU HÓA CẤP! Đây là CẤP CỨU NGUY CẤP. Cần đưa bệnh nhân đến BỆNH VIỆN hoặc gọi CẤP CỨU 115 NGAY để cầm máu, tránh sốc mất máu nguy hiểm tính mạng.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tiêu hóa",
        "question": "Em {AGE} bị đau bụng quặn quanh rốn rồi chuyển sang đau âm ỉ hố chậu phải kèm sốt nhẹ là bị làm sao?",
        "answer": "Đau di chuyển từ quanh rốn xuống hố chậu phải kèm sốt nhẹ ở {DEMO_REF} là triệu chứng điển hình của VIÊM RUỘT THỪA CẤP. Cần đi khám khẩn cấp. (1) Đến ngay bệnh viện có khoa Ngoại, (2) KHÔNG chườm nóng, không uống thuốc giảm đau hay thuốc xổ vì có thể làm vỡ ruột thừa.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tiêu hóa",
        "question": "Em {AGE} hay bị ợ nóng, ợ chua, đau rát vùng thượng vị sau khi ăn no thì uống thuốc gì?",
        "answer": "Ợ nóng ợ chua sau ăn ở {DEMO_REF} là triệu chứng của TRÀO NGƯỢC DẠ DÀY THỰC QUẢN. Em nên: (1) Ăn chậm nhai kỹ, tránh đồ chua cay dầu mỡ, (2) Không nằm ngay sau ăn, kê cao gối khi ngủ, (3) Có thể dùng thuốc kháng acid hoặc ức chế bơm proton (Omeprazole) theo tư vấn dược sĩ. Đi khám nếu kéo dài trên 2 tuần.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Tiêu hóa",
        "question": "Em {AGE} bị đầy hơi chướng bụng kèm đau bụng dưới trước kỳ kinh nguyệt có sao không?",
        "answer": "Đầy hơi chướng bụng và đau bụng dưới trước kỳ kinh ở {DEMO_REF} là triệu chứng phổ biến của HỘI CHỨNG TIỀN KINH NGUYỆT. Đây là hiện tượng sinh lý bình thường. Em nên: (1) Hạn chế muối, đường, cafein, (2) Chườm ấm bụng dưới, tập yoga nhẹ nhàng, (3) Nếu đau quá ảnh hưởng sinh hoạt thì đi khám Phụ khoa.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },

    # ======================== 6. SẢN PHỤ KHOA (5 seeds) ========================
    {
        "category": "Sản phụ khoa",
        "question": "Mang thai tuần thứ 8 bị ra máu tươi kèm đau bụng dưới thì có sao không bác sĩ?",
        "answer": "Mang thai 3 tháng đầu ra máu tươi kèm đau bụng dưới là DẤU HIỆU DỌA SẢY THAI! Cần: (1) Nằm nghỉ tuyệt đối, tránh vận động, (2) Đưa sản phụ đến Bệnh viện Phụ sản gần nhất để siêu âm kiểm tra tim thai và dùng thuốc dưỡng thai kịp thời.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Sản phụ khoa",
        "question": "Chị em {AGE} bị chậm kinh 5 ngày thử que 2 vạch mờ thì nên làm gì?",
        "answer": "Chậm kinh 5 ngày thử que 2 vạch mờ ở {DEMO_REF} khả năng cao đã có thai sớm. Chị nên: (1) Giữ tinh thần thoải mái, bổ sung Acid Folic, tránh làm việc nặng, (2) Thử lại que sau 2-3 ngày hoặc đi khám siêu âm và xét nghiệm Beta-hCG máu để xác định vị trí thai.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Sản phụ khoa",
        "question": "Em {AGE} bị ngứa và ra khí hư màu trắng vón cục như bã đậu là bệnh gì?",
        "answer": "Ngứa kèm khí hư trắng vón cục ở {DEMO_REF} là dấu hiệu điển hình của NHIỄM NẤM Candida âm đạo. Em nên: (1) Vệ sinh vùng kín đúng cách, mặc quần lót thoáng, (2) Không thụt rửa sâu, (3) Đi khám Phụ khoa để được kê thuốc đặt hoặc thuốc uống kháng nấm phù hợp. Tránh tự ý mua thuốc đặt vì có thể không đúng chủng nấm.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Sản phụ khoa",
        "question": "Em {AGE} bị đau bụng kinh dữ dội mỗi tháng, uống thuốc gì cho đỡ?",
        "answer": "Đau bụng kinh dữ dội ở {DEMO_REF} có thể do tăng co bóp tử cung hoặc bệnh lý như lạc nội mạc tử cung. Em có thể: (1) Uống thuốc giảm đau NSAID (Ibuprofen) theo hướng dẫn dược sĩ, (2) Chườm ấm bụng dưới, (3) Đi khám Phụ khoa nếu đau tăng dần hoặc kèm rong kinh để được siêu âm kiểm tra.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Sản phụ khoa",
        "question": "Mẹ bầu {AGE} bị phù chân và tăng huyết áp ở tháng thứ 7 có nguy hiểm không?",
        "answer": "Phù chân kèm tăng huyết áp ở thai phụ {DEMO_REF} là dấu hiệu NGUY CẤP nghi ngờ TIỀN SẢN GIẬT (Preeclampsia). Cần đi khám SẢN KHOA NGAY. Nếu không được xử trí kịp thời có thể gây nguy hiểm cho cả mẹ và thai. Không tự ý dùng thuốc hạ áp.",
        "is_red_flag": True, "is_medication": False, "is_ambiguous": False
    },

    # ======================== 7. DA LIỄU (3 seeds) ========================
    {
        "category": "Da liễu",
        "question": "Em {AGE} bị nổi mụn nước ngứa rát thành chùm ở mạng sườn một bên thân là bệnh gì ạ?",
        "answer": "Mụn nước thành chùm kèm đau rát một bên thân mình ở {DEMO_REF} là dấu hiệu điển hình của ZONA THẦN KINH (Giời bò). Em nên: (1) Đi khám Da liễu sớm trong 72 giờ để uống thuốc kháng virus, (2) Giữ mụn nước khô sạch, KHÔNG gãi vỡ hay đắp lá cây.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Da liễu",
        "question": "Em {AGE} bị nổi mề đay từng mảng đỏ sau khi ăn hải sản thì xử trí thế nào?",
        "answer": "Nổi mề đay sau ăn hải sản ở {DEMO_REF} là DỊ ỨNG THỨC ĂN. Mức độ nhẹ-vừa. Em nên: (1) Ngừng ăn hải sản ngay, uống nhiều nước, (2) Có thể dùng 1 viên kháng histamin (Cetirizine 10mg) theo tư vấn dược sĩ. Đi khám NGAY nếu có khó thở, sưng môi mắt.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Da liễu",
        "question": "Em {AGE} bị mụn trứng cá viêm đỏ ở mặt kéo dài, dùng thuốc gì để hết?",
        "answer": "Mụn trứng cá viêm đỏ ở {DEMO_REF} cần điều trị đúng cách để tránh sẹo. Em nên: (1) Rửa mặt bằng sữa rửa mặt dịu nhẹ 2 lần/ngày, (2) Không tự nặn mụn, (3) Bôi kem chứa benzoyl peroxide hoặc acid salicylic, (4) Nếu mụn nặng, đi khám Da liễu để được kê thuốc bôi kháng sinh hoặc Isotretinoin (tuyệt đối không dùng Isotretinoin nếu đang mang thai).",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },

    # ======================== 8. TAI MŨI HỌNG (3 seeds) ========================
    {
        "category": "Tai Mũi Họng",
        "question": "Em {AGE} bị ù tai chảy mủ tai có hôi thì có đi mổ không?",
        "answer": "Ù tai kèm chảy mủ hôi ở {DEMO_REF} là dấu hiệu của VIÊM TAI GIỮA MẠN TÍNH có thể thủng màng nhĩ hoặc cholesteatoma. Bạn cần đi khám chuyên khoa Tai Mũi Họng để nội soi và đo thính lực. Việc mổ hay không phụ thuộc vào mức độ tổn thương sau khi bác sĩ đánh giá.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tai Mũi Họng",
        "question": "Em {AGE} bị nghẹt mũi kéo dài, không ngửi được mùi, có phải viêm xoang không?",
        "answer": "Nghẹt mũi kéo dài kèm mất khứu giác ở {DEMO_REF} là dấu hiệu của VIÊM XOANG MẠN TÍNH hoặc POLYP MŨI. Em nên: (1) Xịt rửa mũi bằng nước muối sinh lý hàng ngày, (2) Tránh tiếp xúc khói bụi, (3) Đi khám chuyên khoa Tai Mũi Họng để nội soi mũi xoang và chụp CT nếu cần.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Tai Mũi Họng",
        "question": "Em {AGE} bị viêm họng hạt có chữa khỏi hẳn không?",
        "answer": "Viêm họng hạt ở {DEMO_REF} là tình trạng viêm mạn tính của niêm mạc họng, thường do trào ngược dạ dày, viêm xoang mạn hoặc dị ứng. Bệnh có thể kiểm soát tốt chứ khó khỏi hẳn. Em nên: (1) Súc họng nước muối ấm mỗi ngày, (2) Tránh đồ lạnh, nhiều dầu mỡ, (3) Đi khám để điều trị nguyên nhân gốc rễ.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },

    # ======================== 9. CƠ XƯƠNG KHỚP (3 seeds) ========================
    {
        "category": "Cơ xương khớp",
        "question": "Em {AGE} bị ngã xe máy xong cổ chân sưng to không đi được thì làm sao?",
        "answer": "Sau chấn thương cổ chân sưng to ở {DEMO_REF} nghi ngờ BONG GÂN NẶNG HOẶC GÃY XƯƠNG. Em nên: (1) Cố định cổ chân, không cố đi lại, (2) Chườm đá lạnh 15-20 phút, TUYỆT ĐỐI không chườm nóng hay xoa dầu nóng, (3) Đến cơ sở Y tế để chụp X-quang kiểm tra.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Cơ xương khớp",
        "question": "Em {AGE} bị đau lưng dưới âm ỉ kéo dài, ngồi lâu càng đau hơn thì bị bệnh gì?",
        "answer": "Đau lưng dưới âm ỉ kéo dài ở {DEMO_REF} thường do thoái hóa cột sống thắt lưng hoặc thoát vị đĩa đệm. Em nên: (1) Không ngồi quá lâu, tập đi lại nhẹ nhàng, (2) Tập vật lý trị liệu, bơi lội, (3) Đi khám chuyên khoa Cơ xương khớp nếu đau lan xuống chân hoặc tê bì. Không nằm nghỉ quá nhiều vì làm yếu cơ lưng.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Cơ xương khớp",
        "question": "Em {AGE} bị đau khớp gối vào buổi sáng sau khi ngủ dậy, đi lại vài bước là hết đau thì có sao không?",
        "answer": "Đau khớp gối buổi sáng giảm dần khi vận động ở {DEMO_REF} thường là dấu hiệu của VIÊM KHỚP DẠNG THẤP hoặc THOÁI HÓA KHỚP giai đoạn sớm. Em nên: (1) Hạn chế ngồi xổm, điều khiển cân nặng, (2) Chườm ấm vào khớp gối mỗi sáng, (3) Đi khám Cơ xương khớp để chụp X-quang và xét nghiệm máu chẩn đoán chính xác.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },

    # ======================== 10. NỘI TIẾT (3 seeds) ========================
    {
        "category": "Nội tiết",
        "question": "Em {AGE} bị uống nhiều, tiểu nhiều, ăn nhiều mà vẫn sụt cân thì có bị tiểu đường không?",
        "answer": "Tam chứng kinh điển: uống nhiều - tiểu nhiều - ăn nhiều kèm sụt cân ở {DEMO_REF} là dấu hiệu điển hình của ĐÁI THÁO ĐƯỜNG típ 1 hoặc típ 2 chưa kiểm soát. Em cần: (1) Đi khám Nội tiết để làm xét nghiệm đường huyết và HbA1c, (2) Nếu đói bụng run tay, vã mồ hôi có thể là hạ đường huyết cần ăn ngay.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": False
    },
    {
        "category": "Nội tiết",
        "question": "Em {AGE} hay bị hồi hộp, đánh trống ngực, gầy sút cân và sợ nóng là bệnh gì?",
        "answer": "Hồi hộp, đánh trống ngực, sụt cân, sợ nóng ở {DEMO_REF} là triệu chứng điển hình của CƯỜNG GIÁP (Basedow). Em nên: (1) Đi khám Nội tiết để xét nghiệm hormone tuyến giáp (TSH, FT4) và siêu âm tuyến giáp, (2) Hạn chế cafein và thức ăn kích thích, (3) Dùng thuốc kháng giáp theo đúng chỉ định bác sĩ.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": False
    },
    {
        "category": "Nội tiết",
        "question": "Người nhà em {AGE} bị tiểu đường đang uống thuốc, tự nhiên hạ đường huyết phải xử lý thế nào?",
        "answer": "Hạ đường huyết ở {DEMO_REF} là TÌNH TRẠNG KHẨN CẤP! Nếu người bệnh còn tỉnh: (1) Cho uống ngay nước đường, kẹo, nước trái cây hoặc mật ong, (2) Sau 15 phút đo lại nếu chưa tăng thì uống tiếp. Nếu người bệnh hôn mê: (1) KHÔNG đổ nước đường vào miệng vì dễ sặc, (2) Gọi CẤP CỨU 115 và đưa đến bệnh viện gần nhất.",
        "is_red_flag": True, "is_medication": True, "is_ambiguous": False
    },

    # ======================== 11. MƠ HỒ / THIẾU THÔNG TIN (7 seeds) ========================
    {
        "category": "Mơ hồ",
        "question": "Em bị đau bụng thì uống thuốc gì ạ?",
        "answer": "Chào bạn, đau bụng có thể do nhiều nguyên nhân như viêm dạ dày, rối loạn tiêu hóa, viêm ruột thừa hoặc ngộ độc thực phẩm. Vì thông tin còn ngắn, bạn cho biết thêm: (1) Đau vị trí nào (trên rốn, dưới rốn, trái hay phải)? (2) Đau âm ỉ hay quặn từng cơn? (3) Có kèm sốt, nôn hay đi ngoài không? Nếu đau nhẹ nghỉ ngơi uống nước ấm, nếu đau dữ dội đi khám ngay.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": True
    },
    {
        "category": "Mơ hồ",
        "question": "Tôi bị nhức đầu mấy ngày nay thì làm sao bác sĩ?",
        "answer": "Nhức đầu là triệu chứng phổ biến do nhiều nguyên nhân. Bạn cho biết thêm: (1) Đau nửa đầu hay toàn bộ đầu? (2) Đau âm ỉ hay dữ dội? (3) Có kèm sốt, buồn nôn hay mờ mắt không? Nếu đau nhẹ do mệt mỏi, nghỉ ngơi uống đủ nước. Nếu đau dữ dội đột ngột, đi khám ngay.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": True
    },
    {
        "category": "Mơ hồ",
        "question": "Em bị sốt 2 ngày nay uống thuốc gì hết vậy ạ?",
        "answer": "Sốt là phản ứng của cơ thể với nhiễm trùng. Bạn cho biết thêm: (1) Sốt bao nhiêu độ? (2) Có kèm ho, đau họng, phát ban không? (3) Bạn bao nhiêu tuổi? Nếu sốt trên 38.5°C có thể dùng Paracetamol 500mg hạ sốt. Nếu sốt cao không hạ quá 3 ngày, đi khám bác sĩ.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": True
    },
    {
        "category": "Mơ hồ",
        "question": "Cho em hỏi bị ngứa da thì bôi thuốc gì ạ?",
        "answer": "Ngứa da có thể do viêm da dị ứng, mề đay, nấm hoặc chàm. Bạn cho biết thêm: (1) Vùng da ngứa ở đâu, có nổi nốt gì không? (2) Bị từ bao lâu và có tiếp xúc hóa chất/thức ăn lạ không? Rửa sạch da bằng nước ấm, tránh gãi. Đi khám Da liễu để được kê thuốc bôi đúng chủng loại.",
        "is_red_flag": False, "is_medication": True, "is_ambiguous": True
    },
    {
        "category": "Mơ hồ",
        "question": "Tôi bị đau ngực uống thuốc gì được ạ?",
        "answer": "ĐAU NGỰC là triệu chứng CẦN THẬN TRỌNG vì liên quan đến tim mạch, hô hấp hoặc tiêu hóa. Bạn cho biết thêm: (1) Đau bên trái hay giữa ngực? (2) Đau nhói vài giây hay đau thắt kéo dài? (3) Có khó thở hay vã mồ hôi không? TUYỆT ĐỐI không tự mua thuốc. Nếu đau thắt dữ dội lan vai trái, gọi CẤP CỨU 115.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": True
    },
    {
        "category": "Mơ hồ",
        "question": "Chân em bị sưng đau không đi được, bác sĩ cho hỏi bị gì ạ?",
        "answer": "Sưng đau chân không đi được có thể do nhiều nguyên nhân: chấn thương, viêm khớp, gout, hoặc viêm tĩnh mạch. Bạn cho biết thêm: (1) Sưng ở đâu (đầu gối, cổ chân, bàn chân)? (2) Có té ngã trước đó không? (3) Có nóng đỏ tại chỗ hay sốt không? Chườm lạnh trước, nếu đau nhiều cần đi khám chấn thương chỉnh hình.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": True
    },
    {
        "category": "Mơ hồ",
        "question": "Em bị mệt mỏi người không có sức lực là bệnh gì bác sĩ?",
        "answer": "Mệt mỏi kéo dài có thể do thiếu máu, thiếu vitamin, rối loạn giấc ngủ, suy nhược thần kinh hoặc bệnh lý nội tiết (tuyến giáp, tiểu đường). Bạn cho biết thêm: (1) Mệt mỏi bao lâu nay và có kèm sụt cân, sốt nhẹ không? (2) Ngủ được không, có đau đầu hay chóng mặt không? Đi khám tổng quát để kiểm tra công thức máu và các xét nghiệm cơ bản.",
        "is_red_flag": False, "is_medication": False, "is_ambiguous": True
    }
]
