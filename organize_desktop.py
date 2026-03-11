"""
デスクトップ整理スクリプト
使い方: python organize_desktop.py
オプション: python organize_desktop.py --dry-run  (実際には移動せず確認だけ)
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


# 整理先フォルダの定義（ファイル拡張子 → フォルダ名）
EXTENSION_MAP = {
    # 画像
    ".jpg": "画像",
    ".jpeg": "画像",
    ".png": "画像",
    ".gif": "画像",
    ".bmp": "画像",
    ".webp": "画像",
    ".svg": "画像",
    ".ico": "画像",
    # 動画
    ".mp4": "動画",
    ".mov": "動画",
    ".avi": "動画",
    ".mkv": "動画",
    # 音声
    ".mp3": "音楽",
    ".wav": "音楽",
    ".flac": "音楽",
    # Excel
    ".xlsx": "Excel",
    ".xls": "Excel",
    ".csv": "Excel",
    # Word
    ".docx": "Word",
    ".doc": "Word",
    # PowerPoint
    ".pptx": "PowerPoint",
    ".ppt": "PowerPoint",
    # PDF
    ".pdf": "PDF",
    # テキスト・メモ
    ".txt": "メモ・テキスト",
    ".md": "メモ・テキスト",
    # スクリプト・コード
    ".py": "スクリプト",
    ".js": "スクリプト",
    ".sh": "スクリプト",
    ".bat": "スクリプト",
    ".ps1": "スクリプト",
    # 圧縮ファイル
    ".zip": "圧縮ファイル",
    ".rar": "圧縮ファイル",
    ".7z": "圧縮ファイル",
    ".tar": "圧縮ファイル",
    ".gz": "圧縮ファイル",
    # 一時ファイル・削除候補
    ".tmp": "削除候補",
    ".bak": "削除候補",
    ".log": "削除候補",
}

# ファイル名のキーワードで分類（拡張子より優先度低）
KEYWORD_MAP = [
    # キーワードリスト → フォルダ名（上から順に最初にマッチしたものを使用）
    (["ZZZ削除予定", "ゴミ箱に入れ忘れ", "あとで消す"], "削除候補"),
    (["スクリーンショット", "screenshot", "Screenshot"], "スクリーンショット"),
    (["TODO", "todo", "タスク"], "メモ・テキスト"),
    (["会議メモ", "議事録", "メモ"], "メモ・テキスト"),
    (["見積書", "請求書", "領収書"], "経理書類"),
    (["売上", "データ分析", "集計"], "データ・分析"),
    (["報告書", "レポート"], "報告書"),
    (["プレゼン", "presentation"], "PowerPoint"),
]

# 移動しないファイル（デスクトップに残す）
SKIP_FILES = {
    "desktop.ini",
    "thumbs.db",
}


def get_desktop_path() -> Path:
    """デスクトップのパスを取得"""
    # Windows
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        return desktop
    # OneDrive経由のデスクトップ
    onedrive_desktop = Path.home() / "OneDrive" / "デスクトップ"
    if onedrive_desktop.exists():
        return onedrive_desktop
    onedrive_desktop_en = Path.home() / "OneDrive" / "Desktop"
    if onedrive_desktop_en.exists():
        return onedrive_desktop_en
    # 日本語のデスクトップ
    desktop_ja = Path.home() / "デスクトップ"
    if desktop_ja.exists():
        return desktop_ja
    raise FileNotFoundError("デスクトップフォルダが見つかりません")


def get_target_folder(file_path: Path) -> str | None:
    """ファイルの移動先フォルダ名を決定"""
    name = file_path.name
    ext = file_path.suffix.lower()

    # スキップするファイル
    if name.lower() in SKIP_FILES:
        return None

    # キーワードで分類（優先）
    for keywords, folder in KEYWORD_MAP:
        if any(kw in name for kw in keywords):
            return folder

    # 拡張子で分類
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext]

    # 拡張子なし・不明
    return "その他"


def organize(desktop: Path, dry_run: bool = False) -> None:
    """デスクトップを整理する"""
    moves: list[tuple[Path, Path]] = []

    for item in sorted(desktop.iterdir()):
        # フォルダは移動しない
        if item.is_dir():
            continue
        # 隠しファイルはスキップ
        if item.name.startswith("."):
            continue

        target_folder = get_target_folder(item)
        if target_folder is None:
            continue

        dest_dir = desktop / target_folder
        dest_file = dest_dir / item.name

        # 同名ファイルが既にある場合はリネーム
        if dest_file.exists():
            stem = item.stem
            suffix = item.suffix
            i = 1
            while dest_file.exists():
                dest_file = dest_dir / f"{stem}_{i}{suffix}"
                i += 1

        moves.append((item, dest_file))

    if not moves:
        print("整理するファイルはありません。")
        return

    # 結果を表示
    print(f"\n{'[ドライラン] ' if dry_run else ''}以下のファイルを移動します:\n")
    current_folder = ""
    for src, dst in moves:
        if dst.parent.name != current_folder:
            current_folder = dst.parent.name
            print(f"\n📁 {current_folder}/")
        print(f"  {src.name}")

    print(f"\n合計 {len(moves)} ファイル")

    if dry_run:
        print("\n[ドライラン] 実際には移動しませんでした。")
        print("移動するには: python organize_desktop.py")
        return

    # 実際に移動
    print("\n整理中...")
    for src, dst in moves:
        dst.parent.mkdir(exist_ok=True)
        shutil.move(str(src), str(dst))

    print(f"✓ {len(moves)} ファイルを整理しました！")
    print("\n作成されたフォルダ:")
    for folder in sorted({dst.parent.name for _, dst in moves}):
        count = sum(1 for _, dst in moves if dst.parent.name == folder)
        print(f"  📁 {folder}/ ({count}ファイル)")


def main():
    # Jupyterノートブック環境かどうかを検出
    in_jupyter = "ipykernel" in sys.modules

    if in_jupyter:
        # Jupyter内では引数を直接変数で指定
        DRY_RUN = False   # Trueにすると確認のみ（移動しない）
        DESKTOP_PATH = None  # Noneで自動検出、例: "C:/Users/yourname/Desktop"

        try:
            desktop = Path(DESKTOP_PATH) if DESKTOP_PATH else get_desktop_path()
        except FileNotFoundError as e:
            print(f"エラー: {e}")
            return

        print(f"デスクトップ: {desktop}")
        organize(desktop, dry_run=DRY_RUN)
    else:
        parser = argparse.ArgumentParser(description="デスクトップを整理するスクリプト")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="実際には移動せず、何が移動されるかだけ確認する",
        )
        parser.add_argument(
            "--desktop",
            type=str,
            help="デスクトップのパスを手動で指定（省略時は自動検出）",
        )
        args = parser.parse_args()

        try:
            desktop = Path(args.desktop) if args.desktop else get_desktop_path()
        except FileNotFoundError as e:
            print(f"エラー: {e}")
            return

        print(f"デスクトップ: {desktop}")
        organize(desktop, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
