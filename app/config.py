import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent


class Config:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    DATA_DIR = ROOT_DIR / "data"
    CLAUDE_MODEL = "claude-opus-4-6"
    MAX_TOKENS = 2048
    SYSTEM_PROMPT = """あなたは補助金・助成金の専門アドバイザーです。
提供された資料をもとに、ユーザーの質問に日本語で丁寧に回答してください。

回答のガイドライン:
- 資料に記載された情報のみを使用し、不明な点は「資料には記載がありません」と伝えてください
- 補助金名、対象者、補助率、補助額、申請期間などを明確に示してください
- 複数の補助金が該当する場合は、それぞれを整理して説明してください
- 最新情報は公式サイトで確認するよう促してください
- 親切で分かりやすい説明を心がけてください"""
