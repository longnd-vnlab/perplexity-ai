"""
Test upload Audio và phân tích meeting transcript với Gemini 3 Pro
"""

import perplexity
from my_config import PERPLEXITY_COOKIES
import os
import sys
import json
import glob

print("\n" + "=" * 80)
print("🎙️ TEST: Upload Audio + Meeting Transcript Extraction (Gemini 3 Pro)")
print("=" * 80)

# Định nghĩa thư mục audio
AUDIO_DIR = "/home/dinhlong-vnlab/Audio"

# Chọn file audio
print("\n[1/5] Chọn file audio...")

# Nếu có argument từ command line
if len(sys.argv) > 1:
    audio_path = sys.argv[1]
    if not os.path.isabs(audio_path):
        audio_path = os.path.join(AUDIO_DIR, audio_path)
    print(f"📌 Sử dụng file từ argument: {audio_path}")
else:
    # Lấy tất cả file audio trong thư mục
    audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.ogg', '*.flac']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(AUDIO_DIR, ext)))

    if not audio_files:
        print(f"❌ Không tìm thấy file audio nào trong: {AUDIO_DIR}")
        exit(1)

    # Sắp xếp theo thời gian sửa đổi (mới nhất trước)
    audio_files.sort(key=os.path.getmtime, reverse=True)

    print(f"📂 Tìm thấy {len(audio_files)} file audio:")
    for idx, f in enumerate(audio_files, 1):
        file_size = os.path.getsize(f) / 1024 / 1024  # MB
        mod_time = os.path.getmtime(f)
        from datetime import datetime
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  [{idx}] {os.path.basename(f)} ({file_size:.2f} MB) - {mod_time_str}")

    # Cho user chọn hoặc tự động lấy file mới nhất
    print(f"\n💡 Nhập số thứ tự file muốn xử lý (Enter = file mới nhất):")
    user_input = input("👉 Chọn: ").strip()

    if user_input == "":
        audio_path = audio_files[0]
        print(f"✅ Tự động chọn file mới nhất: {os.path.basename(audio_path)}")
    else:
        try:
            idx = int(user_input) - 1
            if 0 <= idx < len(audio_files):
                audio_path = audio_files[idx]
                print(f"✅ Đã chọn: {os.path.basename(audio_path)}")
            else:
                print(f"❌ Số thứ tự không hợp lệ")
                exit(1)
        except ValueError:
            print(f"❌ Vui lòng nhập số")
            exit(1)

# Kết nối tài khoản
print(f"\n[2/5] Kết nối tài khoản...")
client = perplexity.Client(PERPLEXITY_COOKIES)
print(f"✅ Đã kết nối!")
print(f"📊 Pro queries còn: {client.copilot}")
print(f"📁 File upload available: {client.file_upload}")

# Đọc file Audio
print(f"\n[3/5] Đọc file Audio...")
print(f"🎵 File: {os.path.basename(audio_path)}")

if not os.path.exists(audio_path):
    print(f"❌ Không tìm thấy file: {audio_path}")
    exit(1)

file_size = os.path.getsize(audio_path) / 1024 / 1024  # MB
print(f"📦 Kích thước: {file_size:.2f} MB")

# Đọc nội dung file
with open(audio_path, 'rb') as f:
    audio_content = f.read()

print(f"✅ Đã đọc {len(audio_content)} bytes")

# Upload và phân tích với Gemini 3 Pro
print(f"\n[4/5] Upload + Phân tích với Gemini 3 Pro...")
print("🤖 Đang sử dụng Gemini 3 Pro...")
print("⏳ Quá trình này có thể mất vài phút...\n")

# Prompt chi tiết cho meeting extraction
meeting_prompt = """You are a precise JSON extractor
Given a meeting transcript, produce only valid JSON that exactly matches the schema above. Do not output any explanation, markdown, or extra fields. If no tasks are found, output "tasks": []. Always provide both Vietnamese, English and Japanese natural content. Use low randomness (deterministic output).

Extract the meeting title and all requirements for the tasks discussed in the following meeting transcript. Rules:

Only include tasks that are explicit action items or very clearly implied as an action. Omit purely informational comments.

Rules:
**vi_full_transcript**
   - Write a **detailed Vietnamese record** of what was discussed.
   - Do NOT paste raw transcript; rewrite into a clean, detailed narrative.
   - Use numbered sections (1, 2, 3…) for main topics.
   - Inside each section, use bullet points (•) instead of dashes for subpoints.
   - Include important context (who reported what, issues, next actions).
- Rule strictly:When detecting a person's name in the meeting content, assign the formatted name 「<Name>-san」 only if the confidence level is greater than 99%.
If the confidence level is 99% or lower, assign the default name Member instead.
Valid name list:
Long-san
Hung-san
Minh-san
Trung-san
Nhan-san
Okuda-san
Miyao-san -> is host frequently
Li-san
Fujita-san
Sato-san
Lin Jonathan
yamato-sasajima
koichi-matsumoto
 **ja_full_transcript**
   - Provide the same structure/content as vi_full_transcript but in **natural Japanese**.
   - Use polite-neutral, professional style.

Example:
```
1. Báo cáo phát hành (Releases)
Hôm qua có hai đợt phát hành:
12:00: phát hành cho dự án Deep Research (không liên quan đến nhóm AI-driven development).
16:00: liên quan đến nhóm AI-driven development, bao gồm:
AI Link Collection: thay đổi URL đích từ trang nội bộ sang Landing Page.
My Agent: sửa lỗi đóng giao diện khi chỉnh sửa system prompt.
Sửa lỗi tải file upload (ví dụ system prompt) khi dùng AI Agent.

2. Báo cáo cá nhân
Host: xử lý công việc release, chạy thử toàn bộ workflow AI-driven development để kiểm tra, liệt kê vấn đề, điều chỉnh lịch phát hành. Hôm nay sẽ ưu tiên:
Tổ chức lại log lỗi và tạo task.
Điều tra bug người dùng không đăng ký mới được qua GMO-ID.
Minh-san: chỉnh sửa comment cho task My Agent, điều tra lỗi linter trong app Oteru Ninja, lên plan bằng workflow AI-driven development. Hôm nay tiếp tục planning & coding.
Son-san: sửa bug truy cập trái phép tính năng AI image generation, hôm nay test local fix và tham dự seminar 16:00–19:00.
Long-san: xử lý bug thay đổi quyền role mặc định trong hệ thống Reach Access, thêm linter check cho dữ liệu user, task UAT Markdown GPT-4 chat, và hôm nay tiếp tục các task Reach Access & feedback workflow AI-driven development.
Fujisawa-san: chỉnh sửa chức năng xuất hóa đơn cho team Hoppo Hoppo Robot Map, hôm nay thêm link FAQ manual, nếu còn thời gian sẽ làm Phase 2 của Deep Research.
Suzuki-san: theo dõi vấn đề traffic từ smartphone/Twitter, chuẩn bị newsletter.
Sato-san: báo cáo hoạt động tại hội chợ (phát tờ rơi, giới thiệu sản phẩm, hi vọng tăng đăng ký cuối tuần).

3. Thông báo khác
Nhắc về seminar từ 16:00.
Không có thông báo bổ sung nào khác, kết thúc cuộc họp lúc 09:50.
```

**Language & style**
   - Vietnamese and Japanese must be **natural and fluent**, not word-for-word machine translation.
   - Keep technical terms (APIs, feature names, code paths) in original form when appropriate.
   - Be deterministic, low randomness.

Please analyze the audio and extract meeting information in JSON format.
"""

try:
    response = client.search(
        query=meeting_prompt,
        mode='reasoning',
        model='gemini-3.0-pro',  # Sử dụng Gemini 3.0 Pro
        sources=['web'],
        files={'meeting_audio.mp3': audio_content},
        stream=False,
        language='vi-VN'
    )

    print("=" * 80)
    print("📝 KẾT QUẢ PHÂN TÍCH MEETING:")
    print("=" * 80)

    if 'answer' in response:
        answer = response['answer']
        print(answer)

        # Thử parse JSON nếu có trong response
        print("\n" + "=" * 80)
        print("🔍 EXTRACT JSON:")
        print("=" * 80)

        # Tìm JSON trong response
        try:
            # Tìm JSON block trong markdown code block
            if '```json' in answer:
                json_start = answer.find('```json') + 7
                json_end = answer.find('```', json_start)
                json_str = answer[json_start:json_end].strip()
            elif '```' in answer:
                json_start = answer.find('```') + 3
                json_end = answer.find('```', json_start)
                json_str = answer[json_start:json_end].strip()
            else:
                # Thử parse toàn bộ response
                json_str = answer

            # Parse JSON
            meeting_data = json.loads(json_str)
            print(json.dumps(meeting_data, indent=2, ensure_ascii=False))

            # Lưu kết quả JSON
            base_filename = os.path.splitext(os.path.basename(audio_path))[0]
            output_dir = os.path.dirname(audio_path)

            json_file = os.path.join(output_dir, f"{base_filename}_meeting.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(meeting_data, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Đã lưu JSON vào: {json_file}")

            # Tạo file Markdown từ vi_full_transcript
            if 'vi_full_transcript' in meeting_data:
                print("\n" + "=" * 80)
                print("📄 TẠO MEETING REPORT MARKDOWN:")
                print("=" * 80)

                md_file = os.path.join(output_dir, f"{base_filename}_meeting_report.md")

                with open(md_file, 'w', encoding='utf-8') as f:
                    # Header
                    f.write("# Meeting Report\n\n")

                    # Metadata
                    f.write("## Thông tin cuộc họp\n\n")
                    if 'meeting_title' in meeting_data:
                        f.write(f"**Tiêu đề:** {meeting_data['meeting_title']}\n\n")
                    if 'date' in meeting_data:
                        f.write(f"**Ngày:** {meeting_data['date']}\n\n")
                    f.write(f"**File audio:** {os.path.basename(audio_path)}\n\n")
                    f.write("---\n\n")

                    # Nội dung chi tiết
                    f.write("## Nội dung chi tiết\n\n")
                    f.write(meeting_data['vi_full_transcript'])
                    f.write("\n\n")

                    # Tasks nếu có
                    if 'tasks' in meeting_data and meeting_data['tasks']:
                        f.write("---\n\n")
                        f.write("## Danh sách Tasks\n\n")
                        for idx, task in enumerate(meeting_data['tasks'], 1):
                            f.write(f"### Task {idx}\n\n")
                            if 'assignee' in task:
                                f.write(f"**Người thực hiện:** {task['assignee']}\n\n")
                            if 'description' in task:
                                f.write(f"**Mô tả:** {task['description']}\n\n")
                            if 'deadline' in task:
                                f.write(f"**Deadline:** {task['deadline']}\n\n")
                            if 'priority' in task:
                                f.write(f"**Priority:** {task['priority']}\n\n")
                            f.write("\n")

                    # Footer
                    f.write("---\n\n")
                    f.write(f"*Report được tạo tự động từ file audio bằng Gemini 3.0 Pro*\n")

                print(f"✅ Đã tạo Meeting Report: {md_file}")

                # Hiển thị preview
                print("\n📄 PREVIEW MARKDOWN:")
                print("=" * 80)
                with open(md_file, 'r', encoding='utf-8') as f:
                    preview = f.read()
                    # Hiển thị 50 dòng đầu
                    preview_lines = preview.split('\n')[:50]
                    print('\n'.join(preview_lines))
                    if len(preview.split('\n')) > 50:
                        print("\n... (còn tiếp)")
                print("=" * 80)
            else:
                print("⚠️ Không tìm thấy vi_full_transcript trong response")

        except json.JSONDecodeError as je:
            print(f"⚠️ Không thể parse JSON: {je}")
            print(f"Raw response được lưu vào file text")
            base_filename = os.path.splitext(os.path.basename(audio_path))[0]
            output_dir = os.path.dirname(audio_path)
            output_file = os.path.join(output_dir, f"{base_filename}_meeting.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(answer)
            print(f"✅ Đã lưu kết quả vào: {output_file}")

    else:
        print("⚠️ Không nhận được câu trả lời")
        print(f"Response keys: {response.keys()}")

    print("\n" + "=" * 80)
    print(f"✅ Pro queries còn: {client.copilot}")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()

# Test thêm câu hỏi cụ thể - DISABLED
# print(f"\n[5/5] Test extract tasks summary...")
# print("📋 Tổng hợp tasks từ meeting...\n")
#
# try:
#     query2 = """
#     Từ transcript meeting này, hãy liệt kê tất cả tasks/action items theo format:
#
#     - [Tên người] - Task description - Deadline/Priority
#
#     Chỉ liệt kê tasks rõ ràng, không bao gồm thông tin chung.
#     Trả lời bằng tiếng Việt.
#     """
#
#     response2 = client.search(
#         query=query2,
#         mode='reasoning',
#         model='gemini-3.0-pro',
#         sources=['web'],
#         files={'meeting_audio.mp3': audio_content},
#         stream=False,
#         language='vi-VN'
#     )
#
#     print("=" * 80)
#     print("📋 DANH SÁCH TASKS:")
#     print("=" * 80)
#
#     if 'answer' in response2:
#         print(response2['answer'])
#     else:
#         print("⚠️ Không nhận được câu trả lời")
#
#     print("\n" + "=" * 80)
#
# except Exception as e:
#     print(f"❌ Lỗi: {e}")

# Tổng kết
print("\n" + "=" * 80)
print("🎉 HOÀN THÀNH PHÂN TÍCH!")
print("=" * 80)
print(f"📊 Pro queries còn: {client.copilot}")
print(f"📁 File upload: {client.file_upload}")
print("\n💡 Gemini 3 Pro features:")
print("   - Hỗ trợ audio transcription và analysis")
print("   - Model mạnh mẽ nhất của Gemini")
print("   - Multi-language support (Vi, En, Ja)")
print("   - JSON structured output")
print("   - Phân tích sâu và chính xác cao")
print("=" * 80 + "\n")
