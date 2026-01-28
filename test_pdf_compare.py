"""
Test so sánh các modes: auto vs pro vs reasoning
"""

import perplexity
from my_config import PERPLEXITY_COOKIES
import time

print("\n" + "=" * 80)
print("⚔️  TEST: So sánh Auto vs Pro vs Reasoning Mode")
print("=" * 80)

# Setup
client = perplexity.Client(PERPLEXITY_COOKIES)
pdf_path = "/home/dinhlong-vnlab/Documents/perplexity-ai/AWS-Black-Belt_2023_AWS-CDK-Basic-1-Overview_0731_v1.pdf"

with open(pdf_path, 'rb') as f:
    pdf_content = f.read()

query = "AWS CDK có những ưu điểm gì so với CloudFormation truyền thống?"

print(f"\n📝 Câu hỏi: '{query}'")
print(f"📊 Pro queries ban đầu: {client.copilot}\n")

# Test configurations
tests = [
    {
        'name': 'AUTO Mode (Free)',
        'mode': 'auto',
        'model': None
    },
    {
        'name': 'PRO Mode (GPT-5.2)',
        'mode': 'pro',
        'model': 'gpt-5.2'
    },
    {
        'name': 'REASONING Mode (GPT-5.2-Thinking)',
        'mode': 'reasoning',
        'model': 'gpt-5.2-thinking'
    }
]

results = []

# Run tests
for i, test in enumerate(tests, 1):
    print("=" * 80)
    print(f"[{i}/3] Testing: {test['name']}")
    print("=" * 80)

    try:
        start_time = time.time()

        response = client.search(
            query=query,
            mode=test['mode'],
            model=test['model'],
            sources=['web'],
            files={'AWS-CDK.pdf': pdf_content},
            stream=False,
            language='vi-VN'
        )

        elapsed = time.time() - start_time

        if 'answer' in response:
            answer = response['answer']
            answer_length = len(answer)

            result = {
                'name': test['name'],
                'time': elapsed,
                'length': answer_length,
                'answer': answer[:200] + "..." if len(answer) > 200 else answer
            }
            results.append(result)

            print(f"\n⏱️  Thời gian: {elapsed:.2f}s")
            print(f"📏 Độ dài: {answer_length} ký tự")
            print(f"\n💬 Preview (200 ký tự đầu):")
            print("-" * 80)
            print(result['answer'])
            print("-" * 80)
        else:
            print("⚠️ Không có câu trả lời")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print(f"\n✅ Pro queries còn: {client.copilot}\n")

# So sánh kết quả
print("\n" + "=" * 80)
print("📊 SO SÁNH KẾT QUẢ")
print("=" * 80)

if results:
    print(f"\n{'Mode':<35} {'Thời gian':<12} {'Độ dài':<10}")
    print("-" * 80)
    for r in results:
        print(f"{r['name']:<35} {r['time']:.2f}s{'':<6} {r['length']} chars")

    print("\n" + "=" * 80)
    print("💡 NHẬN XÉT:")
    print("=" * 80)
    print("• Auto mode: Nhanh nhất, free, phù hợp câu hỏi đơn giản")
    print("• Pro mode: Cân bằng speed/quality, tốn Pro query")
    print("• Reasoning mode: Chi tiết nhất, logic sâu, tốn nhiều query và thời gian")
    print("=" * 80 + "\n")
