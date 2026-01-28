# 🎯 Demo Scripts - Phân tích PDF với Perplexity AI

Tổng hợp các scripts demo để test upload PDF và phân tích với các mode khác nhau.

## 📋 Danh sách Scripts

### 1. `test_pdf_reasoning.py` ✅ (ĐÃ CHẠY THÀNH CÔNG)
**Phân tích toàn diện với Reasoning Mode (Tư duy sâu)**

- Upload PDF 2.44 MB
- Sử dụng GPT-5.2-Thinking
- Phân tích kiến trúc, so sánh, best practices
- Extract và giải thích code examples
- Thời gian: ~30-60s/query

**Kết quả đạt được:**
- ✅ Phân tích toàn diện: AWS CDK architecture, so sánh với CloudFormation
- ✅ Extract code: L1/L2/L3 constructs với best practices
- ✅ CLI commands và workflow

```bash
python3 test_pdf_reasoning.py
```

---

### 2. `test_pdf_streaming.py`
**Streaming Response Real-time với PDF**

- Upload PDF
- Nhận response real-time (streaming)
- Hiển thị progress indicator
- Tóm tắt nội dung tài liệu

```bash
python3 test_pdf_streaming.py
```

---

### 3. `test_pdf_qa.py`
**Q&A với PDF - Multiple Questions**

- Hỏi 5 câu hỏi cụ thể về tài liệu
- Mode: Pro với GPT-5.2
- Câu trả lời chi tiết cho từng câu

**Các câu hỏi:**
1. CDK L1, L2, L3 constructs khác nhau như thế nào?
2. AWS CDK Bootstrap là gì?
3. BLEA là gì?
4. CDK CLI commands quan trọng?
5. CDK hỗ trợ ngôn ngữ nào?

```bash
python3 test_pdf_qa.py
```

---

### 4. `test_pdf_compare.py`
**So sánh Auto vs Pro vs Reasoning Mode**

- Test cùng 1 câu hỏi với 3 modes
- So sánh thời gian xử lý
- So sánh độ dài và chi tiết câu trả lời
- Đưa ra nhận xét về từng mode

**So sánh:**
- Auto: Nhanh, free, đơn giản
- Pro: Cân bằng, GPT-5.2
- Reasoning: Sâu nhất, tốn nhiều query

```bash
python3 test_pdf_compare.py
```

---

## 🚀 Quick Start

### Bước 1: Đảm bảo có file config
```bash
# Kiểm tra file my_config.py đã có cookies chưa
cat my_config.py
```

### Bước 2: Kiểm tra file PDF tồn tại
```bash
ls -lh AWS-Black-Belt_2023_AWS-CDK-Basic-1-Overview_0731_v1.pdf
```

### Bước 3: Chạy script demo
```bash
# Reasoning mode (đã test thành công)
python3 test_pdf_reasoning.py

# Streaming response
python3 test_pdf_streaming.py

# Q&A
python3 test_pdf_qa.py

# So sánh modes
python3 test_pdf_compare.py
```

---

## 📊 Kết quả Test thực tế

### ✅ Test Reasoning Mode (Đã chạy)
- **File**: AWS-Black-Belt_2023_AWS-CDK-Basic-1-Overview_0731_v1.pdf (2.44 MB)
- **Mode**: Reasoning với GPT-5.2-Thinking
- **Pro queries**: inf → inf (unlimited account)
- **Kết quả**:
  - Phân tích 5 phần toàn diện
  - Extract 6+ code examples với giải thích
  - Best practices và recommendations
  - Thời gian: ~60s cho phân tích sâu

---

## 💡 Tips Sử dụng

### Chọn Mode phù hợp:

| Use Case | Mode đề xuất | Model |
|----------|--------------|-------|
| Tóm tắt nhanh | `auto` | None |
| Phân tích chi tiết | `pro` | `gpt-5.2` |
| Logic phức tạp, reasoning | `reasoning` | `gpt-5.2-thinking` |
| Nghiên cứu chuyên sâu | `deep research` | None |

### File Upload:

```python
# Đọc file
with open('document.pdf', 'rb') as f:
    content = f.read()

# Upload với query
response = client.search(
    query="Your question",
    mode='pro',
    files={'document.pdf': content},
    language='vi-VN'
)
```

### Streaming Response:

```python
for chunk in client.search(query="...", stream=True):
    if 'answer' in chunk:
        print(chunk['answer'], end='', flush=True)
```

---

## 📝 Các Mode Chi Tiết

### Auto Mode (Free)
- ✅ Không tốn Pro query
- ✅ Phù hợp câu hỏi đơn giản
- ⚠️ Độ sâu phân tích hạn chế

### Pro Mode (GPT-5.2)
- ✅ Model nâng cao
- ✅ Phân tích chi tiết
- ⚠️ Tốn Pro query

### Reasoning Mode (GPT-5.2-Thinking)
- ✅ Tư duy logic sâu
- ✅ Extract code + best practices
- ✅ Phân tích toàn diện
- ⚠️ Tốn nhiều Pro query
- ⚠️ Thời gian xử lý lâu (30-60s)

---

## 🔧 Troubleshooting

### Lỗi "File too large"
- Giới hạn: ~10 MB
- Giải pháp: Nén hoặc chia nhỏ file

### Lỗi cookies hết hạn
```bash
# Lấy cookies mới từ Perplexity.ai
# Cập nhật my_config.py
```

### Timeout khi reasoning
```python
# Tăng timeout trong script
response = client.search(..., timeout=180)
```

---

## 📂 Cấu trúc Files

```
perplexity-ai/
├── my_config.py                # Cookies của bạn
├── test_pdf_reasoning.py       # ✅ Reasoning mode
├── test_pdf_streaming.py       # Streaming
├── test_pdf_qa.py             # Q&A
├── test_pdf_compare.py        # So sánh modes
├── AWS-Black-Belt_*.pdf       # File test
└── README_PDF_DEMO.md         # File này
```

---

## 🎉 Kết luận

Đã test thành công upload PDF 2.44 MB và phân tích với **Reasoning Mode**!

**Highlights:**
- ✅ Upload file lớn OK
- ✅ Reasoning mode phân tích cực kỳ chi tiết
- ✅ Extract code + best practices
- ✅ Support tiếng Việt hoàn hảo
- ✅ Pro queries unlimited

**Next steps:**
- Tích hợp vào project của bạn
- Test với PDF khác
- Tạo chatbot Q&A với documents
- Build knowledge base từ PDFs

---

Made with ❤️ using Perplexity AI + Claude Code
