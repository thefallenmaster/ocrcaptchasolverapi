import io
import re
import operator
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, ImageOps
import pytesseract

app = FastAPI()

# Supported basic math operations
OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    'x': operator.mul,
    '/': operator.floordiv,
}

@app.post("/solve")
async def solve_captcha(image: UploadFile = File(...)):
    try:
        # 1. Read uploaded image
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("L")

        # 2. Invert colors (white text on black background -> black text on white)
        img = ImageOps.invert(img)

        # 3. Upscale 2x for sharper OCR recognition on small bitmap fonts
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.NEAREST)

        # 4. Extract text via OCR
        extracted_text = pytesseract.image_to_string(img, config="--psm 6")

        # 5. Find math expression pattern (e.g., "43+7=")
        match = re.search(r'(\d+)\s*([\+\-\*x\/])\s*(\d+)\s*=?', extracted_text)
        if not match:
            raise HTTPException(
                status_code=422, 
                detail=f"Could not find a math expression. OCR read: {extracted_text.strip()}"
            )

        num1 = int(match.group(1))
        op_symbol = match.group(2)
        num2 = int(match.group(3))

        result = OPS[op_symbol](num1, num2)

        return {
            "expression": f"{num1}{op_symbol}{num2}",
            "answer": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
