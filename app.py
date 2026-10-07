import io
import re
import operator
from flask import Flask, request, jsonify
from PIL import Image, ImageOps
import pytesseract

app = Flask(__name__)

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    'x': operator.mul,
    '/': operator.floordiv,
}

@app.route("/solve", methods=["POST"])
def solve_captcha():
    if "image" not in request.files:
        return jsonify({"error": "No image field provided"}), 400

    try:
        file = request.files["image"]
        img = Image.open(io.BytesIO(file.read())).convert("L")
        img = ImageOps.invert(img)
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.NEAREST)

        extracted_text = pytesseract.image_to_string(img, config="--psm 6")
        match = re.search(r'(\d+)\s*([\+\-\*x\/])\s*(\d+)\s*=?', extracted_text)

        if not match:
            return jsonify({"error": "No math expression found", "ocr": extracted_text.strip()}), 422

        num1, op_symbol, num2 = int(match.group(1)), match.group(2), int(match.group(3))
        result = OPS[op_symbol](num1, num2)

        return jsonify({"expression": f"{num1}{op_symbol}{num2}", "answer": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
