from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    data_dir = Config.DATA_DIR
    print(f"データフォルダ: {data_dir}")
    print(f"読み込みファイル数: {len(list(data_dir.iterdir()))}")
    app.run(debug=True, port=5000)
