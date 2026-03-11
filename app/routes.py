import json
import anthropic
from flask import Blueprint, render_template, request, Response, stream_with_context, current_app
from .utils import load_documents

main_bp = Blueprint("main", __name__)


def get_client():
    return anthropic.Anthropic(api_key=current_app.config["ANTHROPIC_API_KEY"])


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    history = data.get("history", [])

    data_dir = current_app.config["DATA_DIR"]
    system_prompt = current_app.config["SYSTEM_PROMPT"]
    model = current_app.config["CLAUDE_MODEL"]
    max_tokens = current_app.config["MAX_TOKENS"]

    documents = load_documents(data_dir)
    system_with_docs = f"{system_prompt}\n\n以下が補助金情報の資料です:\n\n{documents}"

    messages = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
    ]

    client = get_client()

    def generate():
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
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
