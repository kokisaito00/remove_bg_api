from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

# 🔽 環境変数から PORT を取得（Render 仕様に従う）
port = int(os.environ.get("PORT", 10000))

# 🔽 追加：初回実行時にモデルをダウンロード
os.system("rembg i")

app = Flask(__name__)

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    image_file = request.files.get("image")
    if not image_file:
        return {"error": "画像ファイルが必要です"}, 400

    try:
        input_bytes = image_file.read()
        output_bytes = remove(input_bytes)

        output_img = Image.open(io.BytesIO(output_bytes))
        buffer = io.BytesIO()
        output_img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype="image/png")

    except Exception as e:
        return {"error": str(e)}, 500

# 🔽 Render に必要なポート設定（環境変数を参照）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)  # ここを環境変数の `PORT` に合わせる
