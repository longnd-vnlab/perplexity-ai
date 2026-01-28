import perplexity
from my_config import PERPLEXITY_COOKIES
import sys
import os
import re
from datetime import datetime

def main():
    # 1. Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python3 deep_research.py \"Your research topic here\"")
        print("Example: python3 deep_research.py \"Tương lai của AI Agent trong năm 2025\"")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])

    print("\n" + "=" * 80)
    print("🚀 DEEP RESEARCH TOOL (Gemini 3 Pro)")
    print("=" * 80)
    print(f"📌 Topic: {user_prompt}")

    # 2. Connect to Perplexity
    print(f"\n[1/3] Connecting to Perplexity...")
    try:
        client = perplexity.Client(PERPLEXITY_COOKIES)
        print(f"✅ Connected!")
        print(f"📊 Pro queries remaining: {client.copilot}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Please check your cookies in my_config.py")
        sys.exit(1)

    # 3. Construct Research Prompt
    # We craft a prompt to ensure high-quality Markdown output
    research_prompt = f"""You are a researcher.
Topic: "{user_prompt}"

Output in Markdown format.
Include full list of sources/citations at the end.
"""

    # 4. Perform Search
    print(f"\n[2/3] Performing Deep Research...")
    print("🤖 Mode: Deep Research")
    print("🧠 Model: Default (pplx_alpha)")
    print("⏳ This may take a few minutes. Please wait...")

    try:
        response = client.search(
            query=research_prompt,
            mode='deep research',
            model=None,
            sources=['web'],
            stream=False,
            language='vi-VN'
        )

        # 5. Process Output
        print(f"\n[3/3] Processing results...")

        if 'answer' in response and response['answer']:
            content = response['answer']

            # Create a filename from the prompt
            # Remove special characters and limit length
            slug = re.sub(r'[^\w\s-]', '', user_prompt).strip().lower()
            slug = re.sub(r'[-\s]+', '_', slug)[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"research_{slug}_{timestamp}.md"

            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Success! Research saved to:")
            print(f"📂 {os.path.abspath(filename)}")

            # Preview
            print("\n" + "=" * 80)
            print("📄 PREVIEW (First 20 lines)")
            print("=" * 80)
            preview_lines = content.split('\n')[:20]
            print('\n'.join(preview_lines))
            print("...\n")

        else:
            print("⚠️ Warning: No answer received from Perplexity.")
            if 'text' in response:
                 print(f"Debug Info (text): {response['text']}")

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
