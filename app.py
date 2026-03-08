import os
import json
from flask import Flask, render_template, request, Response, stream_with_context
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

FORTUNE_SYSTEM_PROMPT = """あなたはポケモン占い師「ミスティック・ポケドラ」です。
ユーザーに割り当てられたポケモンの特性をもとに、その人の今日の運勢を神秘的に占います。

占いのガイドライン:
- ポケモンのタイプ・特性・能力値の特徴を今日の運勢に結びつけてください
- 「✨ 総合運」「💖 恋愛運」「💼 仕事運」「🍀 ラッキーアイテム」を必ず含めてください
- 神秘的で詩的な言葉を使い、ポケモンらしいエッセンスを出してください
- 全体的にポジティブで希望が持てる内容にしてください
- 絵文字を適度に使って楽しい雰囲気を演出してください
- 各項目は改行で区切り、読みやすくしてください"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/fortune", methods=["POST"])
def fortune():
    data = request.get_json()
    user_name = data.get("name", "あなた")
    pokemon = data.get("pokemon", {})

    pokemon_name_ja = pokemon.get("name_ja", pokemon.get("name", "ポケモン"))
    pokemon_name_en = pokemon.get("name", "pokemon")
    pokemon_types = "・".join(pokemon.get("types", []))
    pokemon_abilities = "・".join(pokemon.get("abilities", []))
    stats = pokemon.get("stats", {})
    stats_text = "、".join([f"{k} {v}" for k, v in stats.items()])

    user_message = f"""占い対象者: {user_name}さん
本日の守護ポケモン: {pokemon_name_ja}（{pokemon_name_en}）
タイプ: {pokemon_types}
特性: {pokemon_abilities}
能力値: {stats_text}

{user_name}さんの今日の運勢を占ってください。"""

    def generate():
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=FORTUNE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
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
    app.run(debug=True, port=5000)
