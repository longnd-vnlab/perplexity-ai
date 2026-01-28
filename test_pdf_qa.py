"""
Test Q&A với PDF - Hỏi đáp về nội dung tài liệu
"""

import perplexity
from my_config import PERPLEXITY_COOKIES
import os

print("\n" + "=" * 80)
print("💬 TEST: Q&A với PDF - Multiple Questions")
print("=" * 80)

# Setup
print("\n[1/2] Setup...")
client = perplexity.Client(PERPLEXITY_COOKIES)
pdf_path = "/home/dinhlong-vnlab/Documents/perplexity-ai/AWS-Black-Belt_2023_AWS-CDK-Basic-1-Overview_0731_v1.pdf"

with open(pdf_path, 'rb') as f:
    pdf_content = f.read()

print(f"✅ Setup OK! (Pro queries: {client.copilot})")

# Danh sách câu hỏi
questions = [
    "CDK L1, L2, L3 constructs khác nhau như thế nào? Cho ví dụ cụ thể.",
    "AWS CDK Bootstrap là gì và tại sao cần thiết?",
    "Trong tài liệu có đề cập đến BLEA không? Nó là gì?",
    "Các lệnh CDK CLI quan trọng nhất là gì?",
    "CDK hỗ trợ những ngôn ngữ lập trình nào?"
]

# Q&A Loop
print(f"\n[2/2] Hỏi đáp với {len(questions)} câu hỏi...\n")
print("=" * 80)

for i, question in enumerate(questions, 1):
    print(f"\n❓ [{i}/{len(questions)}] {question}")
    print("-" * 80)

    try:
        response = client.search(
            query=question,
            mode='pro',
            model='gpt-5.2',
            sources=['web'],
            files={'AWS-CDK.pdf': pdf_content},
            stream=False,
            language='vi-VN'
        )

        if 'answer' in response:
            # In tối đa 300 ký tự
            answer = response['answer']
            if len(answer) > 300:
                print(answer[:300] + "...")
            else:
                print(answer)
        else:
            print("⚠️ Không có câu trả lời")

        print("-" * 80)

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("-" * 80)

# Tổng kết
print("\n" + "=" * 80)
print("🎉 HOÀN THÀNH Q&A!")
print("=" * 80)
print(f"📊 Tổng số câu hỏi: {len(questions)}")
print(f"📊 Pro queries còn: {client.copilot}")
print("=" * 80 + "\n")
