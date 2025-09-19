from app import create_app

app = create_app()

if __name__ == "__main__":
    # 開発時のみ。コンテナでは gunicorn が起動します。
    app.run(host="0.0.0.0", port=8000)
