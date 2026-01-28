"""
Test upload PDF và phân tích với Reasoning Mode
"""

import perplexity
from my_config import PERPLEXITY_COOKIES
import os

print("\n" + "=" * 80)
print("🧠 TEST: Upload PDF + Reasoning Mode (Tư duy sâu)")
print("=" * 80)

# Kết nối tài khoản
print("\n[1/4] Kết nối tài khoản...")
client = perplexity.Client(PERPLEXITY_COOKIES)
print(f"✅ Đã kết nối!")
print(f"📊 Pro queries còn: {client.copilot}")
print(f"📁 File upload available: {client.file_upload}")

# Đọc file PDF
pdf_path = "/home/dinhlong-vnlab/Documents/perplexity-ai/AWS-Black-Belt_2023_AWS-CDK-Basic-1-Overview_0731_v1.pdf"

print(f"\n[2/4] Đọc file PDF...")
print(f"📄 File: {os.path.basename(pdf_path)}")

if not os.path.exists(pdf_path):
    print(f"❌ Không tìm thấy file: {pdf_path}")
    exit(1)

file_size = os.path.getsize(pdf_path) / 1024 / 1024  # MB
print(f"📦 Kích thước: {file_size:.2f} MB")

# Đọc nội dung file
with open(pdf_path, 'rb') as f:
    pdf_content = f.read()

print(f"✅ Đã đọc {len(pdf_content)} bytes")

# Upload và phân tích với Reasoning Mode
print(f"\n[3/4] Upload + Phân tích với REASONING MODE...")
print("🧠 Đang sử dụng GPT-5.2-Thinking (tư duy sâu)...")
print("⏳ Quá trình này có thể mất 30-60 giây...\n")

try:
    # Câu hỏi phân tích chuyên sâu
    query = """
    Hãy phân tích toàn diện tài liệu AWS CDK này và trả lời:

    1. AWS CDK là gì? Giải thích chi tiết kiến trúc và nguyên lý hoạt động
    2. Những điểm khác biệt quan trọng giữa AWS CDK và CloudFormation truyền thống?
    3. Các use cases và best practices khi sử dụng AWS CDK
    4. Ưu điểm và hạn chế của AWS CDK
    5. Roadmap và hướng phát triển

    Hãy phân tích sâu với reasoning logic rõ ràng.
    """

    response = client.search(
        query=query,
        mode='reasoning',
        model='gpt-5.2-thinking',  # Model tư duy sâu
        sources=['web'],
        files={'AWS-CDK-Overview.pdf': pdf_content},
        stream=False,
        language='vi-VN'
    )

    print("=" * 80)
    print("📝 KẾT QUẢ PHÂN TÍCH TƯ DUY SÂU:")
    print("=" * 80)

    if 'answer' in response:
        print(response['answer'])
    else:
        print("⚠️ Không nhận được câu trả lời")
        print(f"Response keys: {response.keys()}")

    print("\n" + "=" * 80)
    print(f"✅ Pro queries còn: {client.copilot}")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()

# Test thêm câu hỏi cụ thể
print(f"\n[4/4] Test câu hỏi cụ thể về code trong PDF...")
print("🔍 Hỏi về code examples...\n")

try:
    query2 = """
    Trong tài liệu có những code examples nào?
    Hãy extract và giải thích chi tiết từng đoạn code,
    giải thích logic và best practices được áp dụng.
    """

    response2 = client.search(
        query=query2,
        mode='reasoning',
        model='gpt-5.2-thinking',
        sources=['web'],
        files={'AWS-CDK-Overview.pdf': pdf_content},
        stream=False,
        language='vi-VN'
    )

    print("=" * 80)
    print("📝 PHÂN TÍCH CODE EXAMPLES:")
    print("=" * 80)

    if 'answer' in response2:
        print(response2['answer'])
    else:
        print("⚠️ Không nhận được câu trả lời")

    print("\n" + "=" * 80)

except Exception as e:
    print(f"❌ Lỗi: {e}")

# Tổng kết
print("\n" + "=" * 80)
print("🎉 HOÀN THÀNH PHÂN TÍCH!")
print("=" * 80)
print(f"📊 Pro queries còn: {client.copilot}")
print(f"📁 File upload: {client.file_upload}")
print("\n💡 Reasoning Mode sử dụng:")
print("   - Phân tích sâu với logic rõ ràng")
print("   - Tốn nhiều Pro query hơn mode thường")
print("   - Thời gian xử lý lâu hơn (30-60s)")
print("   - Kết quả chi tiết và có độ sâu cao")
print("=" * 80 + "\n")
