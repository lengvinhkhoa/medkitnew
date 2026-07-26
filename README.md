# 🏥 Bộ Crawler & Xử lý Dữ liệu Y Tế Việt Nam cho Fine-Tuning Gemma 4 e2b

Hệ thống chuyên dụng để cào, làm sạch, lọc an toàn y tế và đóng gói dữ liệu Hỏi-Đáp sức khỏe từ các nguồn uy tín Việt Nam (Vinmec, Medlatec,...) dành cho đối tượng **Bệnh nhân / Người dùng phổ thông**, định dạng sẵn theo chuẩn `messages` của **Gemma 4 e2b** (Google DeepMind).

---

## 🌟 Đặc điểm nổi bật & Quy tắc an toàn bắt buộc

1. **Văn phong đời thường & Trấn an:** Giải thích nguyên nhân dễ hiểu, đánh giá mức độ nghiêm trọng (Nhẹ / Cần theo dõi / Cần đi khám ngay) và hướng dẫn hành động.
2. **Red Flags Safety Engine:** Tự động phát hiện triệu chứng nguy cấp (*đau ngực thắt, đột quỵ méo miệng, sốt cao co giật...*) và điều hướng bệnh nhân đi **Cấp cứu 115 / Bệnh viện ngay lập tức**.
3. **Thận trọng với Thuốc:** Tự động chèn khuyến cáo không tự ý uống kháng sinh/kê đơn và tư vấn bác sĩ/dược sĩ.
4. **Xử lý câu hỏi mơ hồ:** Hướng dẫn mô hình biết cách hỏi ngược lại người dùng để lấy thêm thông tin triệu chứng thay vì chẩn đoán đoán mò.
5. **Tối ưu phần cứng:** Dùng Python Async, không tốn VRAM/RAM, thích hợp chạy trực tiếp trên máy RTX 2050 (4GB VRAM), Core i5, 16GB RAM.

---

## 🛠️ Hướng dẫn cài đặt & Sử dụng

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Tạo dữ liệu mẫu & Kiểm thử nhanh (Sample Data Generator)
```bash
python main.py sample
```
Lệnh này sẽ nạp ngay dữ liệu mẫu chuẩn y tế bao gồm cả 4 trường hợp bắt buộc và xuất ra file `data/processed/patient_medical_dataset.jsonl`.

### 3. Cào dữ liệu thực tế từ Website Y tế
```bash
# Cào 3 trang từ Vinmec
python main.py crawl --source vinmec --pages 3

# Cào từ tất cả các nguồn
python main.py crawl --source all --pages 5
```

### 4. Xử lý & Đóng gói dữ liệu thô sang JSONL
```bash
python main.py process
```

### 5. Kiểm tra chất lượng & Báo cáo thống kê
```bash
python main.py validate
```

### 6. Chạy Unit Test kiểm thử logic
```bash
pytest tests/
```

---

## 📋 Đã đóng gói định dạng JSONL Fine-tune Gemma 4 e2b

Mỗi mẫu dữ liệu trong `data/processed/patient_medical_dataset.jsonl` có dạng:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "Bạn là trợ lý tư vấn sức khỏe thông minh và tận tâm dành cho người dùng phổ thông tại Việt Nam..."
    },
    {
      "role": "user",
      "content": "Con em 3 tuổi sốt 38.5 độ, có cần đi viện không ạ?"
    },
    {
      "role": "assistant",
      "content": "Với bé 3 tuổi sốt 38.5°C, đây là mức sốt nhẹ-vừa. Anh/chị có thể: (1) Cho bé uống nhiều nước hoặc oresol, (2) Hạ sốt bằng paracetamol theo liều cân nặng (10-15mg/kg mỗi 4-6h), (3) Lau mát nách bẹn và theo dõi thêm 24h. Cần đưa bé đi khám NGAY nếu: sốt trên 39°C không hạ, co giật, li bì, bỏ ăn/bú, phát ban. Đây chỉ là thông tin tham khảo, nếu lo lắng anh/chị nên đưa bé đi khám trực tiếp."
    }
  ],
  "metadata": {
    "source": "sample_data",
    "url": "https://example.com/medical/2",
    "safety_flags": {
      "is_red_flag": false,
      "is_medication": false,
      "is_ambiguous": false
    }
  }
}
```
