
import perplexity
from my_config import PERPLEXITY_COOKIES
import os
import time
import re

def clean_filename(text):
    """Làm sạch tên file để lưu"""
    s = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', s)

def main():
    print("\n" + "=" * 80)
    print("📖 PDF CHAPTER EXTRACTOR (High Performance MySQL 4th)")
    print("=" * 80)

    # 1. Setup
    print("\n[1/3] Setup connection & file...")
    try:
        client = perplexity.Client(PERPLEXITY_COOKIES)
        print(f"✅ Connected to Perplexity!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    pdf_path = "/home/dinhlong-vnlab/Documents/perplexity-ai/high-performance-mysql-4th.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return

    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()

    print(f"✅ Loaded PDF: {os.path.basename(pdf_path)} ({len(pdf_content)/1024/1024:.2f} MB)")

    # 2. Define Chapters
    # Tự định nghĩa danh sách chương để đảm bảo loop chạy đúng
    chapters = [
        "Chapter 12: MySQL in the Cloud",
        "Chapter 13: Compliance with MySQL"
    ]

    output_dir = "mysql_book_extract"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[2/3] Extracting {len(chapters)} chapters...")
    print(f"📂 Output directory: {output_dir}/")

    # 3. Process Loop
    for i, chapter in enumerate(chapters, 12):
        print(f"\n⏳ Processing [{i}/{len(chapters) + 11}]: {chapter}")

        prompt = f"""
Act as: vietnamese-tech-writer
Role: Technical blogger & architect, viết bài kỹ thuật tiếng Việt với giọng chia sẻ kinh nghiệm thực tế cho developer.

---

Nhiệm vụ

Viết một bài technical blog hoàn chỉnh (KHÔNG phải tóm tắt) dựa trên nội dung {chapter} từ sách “High Performance MySQL, 4th Edition” (PDF đính kèm).

---

Yêu cầu bắt buộc

- KHÔNG viết dạng summary / bullet-only
- KHÔNG sử dụng hình ảnh, diagram, illustration
- Nội dung phải giống bài blog kỹ thuật publish được
- Độ sâu: intermediate → advanced backend / infra engineer
- Xuất duy nhất bằng Markdown
- Không có lời dẫn hội thoại, không nhắc lại prompt

---

Phong cách viết (BẮT BUỘC)

- Viết theo style tự nhiên của architect
- Xưng hô: mình – mọi người – anh em – chúng ta
- Giọng văn:
  - Thân thiện như đang chia sẻ kinh nghiệm dự án
  - Có humor nhẹ: (hẹ hẹ), (haizz), (sad)
  - Dùng từ quen thuộc với dev: ảo ma, ngon lành, bùm, lằng nhằng
- KHÔNG dùng emoji/icon, chỉ dùng text expression

---

Cấu trúc bài viết (BẮT BUỘC)

    # [Tiêu đề bài viết – Hấp dẫn, dựa trên nội dung {chapter}]

    ## Mở đầu – Tản mạn dev
    - Dẫn dắt bằng tình huống thực tế, pain point liên quan đến chủ đề của chương
    - Nêu rõ bài viết sẽ giúp người đọc giải quyết vấn đề gì

    ## Tổng quan
    - Vai trò và tầm quan trọng của chủ đề trong MySQL
    - Các concept cốt lõi

    [Phần nội dung chính: Hãy trích xuất 3-5 chủ đề kỹ thuật quan trọng nhất trong chương này để phân tích sâu. Mỗi chủ đề là một mục H2 riêng biệt. Với mỗi mục cần có phân tích sâu, ví dụ cấu hình, code minh họa nếu có]

    ## Các sai lầm thường gặp (Common Pitfalls)
    - Các cấu hình hay bị hiểu sai hoặc lạm dụng
    - Các lỗi phổ biến

    ## Kinh nghiệm thực tế / Lesson Learned
    - Case study hoặc kinh nghiệm thực chiến liên quan
    - Lỗi từng gặp khi scale hệ thống

    ## Kết luận
    - Tư duy đúng khi tiếp cận chủ đề này
    - Gợi ý topic nên tìm hiểu tiếp

    **Nguồn:**
    - High Performance MySQL, 4th Edition – {chapter}
    - Official MySQL Documentation

---

Nội dung kỹ thuật
"""

        try:
            # Dùng model 'gemini-3.0-pro' như test_audio_meeting.py
            response = client.search(
                query=prompt,
                mode='reasoning',       # Dùng reasoning mode cho phân tích sâu
                model='gemini-3.0-pro', # Theo test_audio_meeting.py
                sources=['web'],
                files={'book.pdf': pdf_content},
                stream=False,
                language='vi-VN'
            )

            if 'answer' in response:
                content = response['answer']

                # Save
                safe_name = clean_filename(chapter)
                filename = f"{output_dir}/{str(i).zfill(2)}_{safe_name}.md"

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"   ✅ Saved: {filename}")

            else:
                print("   ⚠️ No answer returned.")

        except Exception as e:
            print(f"   ❌ Error extracting {chapter}: {e}")

        # Nghỉ xíu tránh rate limit nếu có
        # time.sleep(2)

    print("\n" + "=" * 80)
    print("🎉 EXTRACTION COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    main()
