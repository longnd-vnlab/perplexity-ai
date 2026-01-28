"""
Test upload PDF và streaming response real-time
"""

import perplexity
from my_config import PERPLEXITY_COOKIES
import os

print("\n" + "=" * 80)
print("📡 TEST: Upload PDF + Streaming Response (Real-time)")
print("=" * 80)

# Kết nối
print("\n[1/3] Kết nối tài khoản...")
client = perplexity.Client(PERPLEXITY_COOKIES)
print(f"✅ Kết nối OK! Pro queries: {client.copilot}")

# Đọc PDF
pdf_path = "/home/dinhlong-vnlab/Documents/perplexity-ai/AWS-Black-Belt_2023_AWS-CDK-Basic-1-Overview_0731_v1.pdf"
print(f"\n[2/3] Đọc file PDF...")

with open(pdf_path, 'rb') as f:
    pdf_content = f.read()

file_size = len(pdf_content) / 1024 / 1024
print(f"✅ Đã đọc {file_size:.2f} MB")

# Streaming query
print(f"\n[3/3] Streaming response real-time...")
print("📝 Câu hỏi: 'Tóm tắt nội dung chính của tài liệu AWS CDK này'\n")
print("=" * 80)

try:
    chunk_count = 0
    answer_buffer = ""

    for chunk in client.search(
        query="Hãy tóm tắt nội dung chính của tài liệu AWS CDK này, bao gồm: định nghĩa, kiến trúc, use cases và best practices. Trả lời bằng tiếng Việt.",
        mode='pro',
        model='gpt-5.2',
        sources=['web'],
        files={'AWS-CDK.pdf': pdf_content},
        stream=True,
        language='vi-VN'
    ):
        chunk_count += 1

        # In progress indicator mỗi 10 chunks
        if chunk_count % 10 == 0:
            print(".", end="", flush=True)

        # Lưu answer
        if 'answer' in chunk:
            answer_buffer = chunk['answer']

    print(f"\n✅ Đã nhận {chunk_count} chunks!")
    print("\n" + "=" * 80)
    print("📝 KẾT QUẢ TÓM TẮT:")
    print("=" * 80)
    print(answer_buffer)
    print("=" * 80)

except Exception as e:
    print(f"\n❌ Lỗi: {e}")

print(f"\n✅ Hoàn thành! Pro queries còn: {client.copilot}\n")
