from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

# 🔽 Render 環境変数から PORT を取得（デフォルト: 10000）
port = int(os.environ.get("PORT", 10000))

# 🔽 モデルを事前ダウンロード（初回起動対策）
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

# 🔽 Render.comの仕様に合わせて起動（0.0.0.0で全リクエスト受信）
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)