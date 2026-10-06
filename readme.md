# Math Captcha Solver API

A lightweight, headless FastAPI service that uses Tesseract OCR to read math captcha images via `POST` requests and return the calculated answer.

## 📁 Repository Structure

Ensure your GitHub repository contains these files:
```text
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## 🚀 Deploy on Render (Brief Instructions)

1. **Push to GitHub:** Upload `app.py`, `requirements.txt`, and `Dockerfile` to a new GitHub repository.
2. **Create Service:** Log in to [Render](https://render.com/), click **New +** -> **Web Service**, and connect your GitHub repository.
3. **Configure Settings:**
   * **Runtime / Environment:** Select `Docker` (Render will automatically detect the `Dockerfile` and install Tesseract OCR).
   * **Instance Type:** Select `Free`.
4. **Add Port Variable (Optional):** Under **Environment Variables**, add `PORT` with the value `8000`.
5. **Deploy:** Click **Create Web Service**. Once the build finishes, copy your live URL (e.g., `https://your-app-name.onrender.com`).

---

## 📡 API Usage

### Endpoint
`POST /solve`

### Test with `curl`
```bash
curl -X POST "https://your-app-name.onrender.com/solve" \
  -F "image=@download.png"
```

### Test with Python
```python
import requests

url = "https://your-app-name.onrender.com/solve"
with open("download.png", "rb") as f:
    response = requests.post(url, files={"image": f})

print(response.json())
```

### Example Response
```json
{
  "expression": "43+7",
  "answer": 50
}
```