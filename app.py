import os
import json
from pathlib import Path
from flask import Flask, render_template, request, Response, stream_with_context
import anthropic
from openai import OpenAI
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

DATA_DIR = Path(__file__).parent / "data"


def load_documents() -> str:
    """Load all text and PDF files from the data directory."""
    contents = []

    for path in sorted(DATA_DIR.iterdir()):
        if path.suffix == ".txt":
            text = path.read_text(encoding="utf-8")
            contents.append(f"=== ファイル: {path.name} ===\n{text}")
        elif path.suffix == ".pdf":
            reader = PdfReader(str(path))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n".join(pages)
            contents.append(f"=== ファイル: {path.name} ===\n{text}")

    return "\n\n".join(contents)


SYSTEM_PROMPT = """あなたは補助金・助成金の専門アドバイザーです。
提供された資料をもとに、ユーザーの質問に日本語で丁寧に回答してください。

回答のガイドライン:
- 資料に記載された情報のみを使用し、不明な点は「資料には記載がありません」と伝えてください
- 補助金名、対象者、補助率、補助額、申請期間などを明確に示してください
- 複数の補助金が該当する場合は、それぞれを整理して説明してください
- 最新情報は公式サイトで確認するよう促してください
- 親切で分かりやすい説明を心がけてください"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    history = data.get("history", [])
    provider = data.get("provider", "claude")

    documents = load_documents()
    system_with_docs = f"{SYSTEM_PROMPT}\n\n以下が補助金情報の資料です:\n\n{documents}"

    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
    ]

    if provider == "chatgpt":
        def generate():
            stream = openai_client.chat.completions.create(
                model="gpt-4o",
                max_tokens=2048,
                messages=[{"role": "system", "content": system_with_docs}] + messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield f"data: {json.dumps({'text': delta.content})}\n\n"
            yield "data: [DONE]\n\n"
    else:
        def generate():
            with anthropic_client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=2048,
                system=system_with_docs,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    print(f"データフォルダ: {DATA_DIR}")
    print(f"読み込みファイル数: {len(list(DATA_DIR.iterdir()))}")
    app.run(debug=True, port=5000)
