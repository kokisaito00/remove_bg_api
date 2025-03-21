from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

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

# 🔽 ここがRender.comに必要な "追加すべき部分" 🔽
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Renderが動的に割り当てるポート
    app.run(host="0.0.0.0", port=port)        # 全てのリクエストを受け付ける
