FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.app:app", "--timeout", "300"]

