FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY st_requirements.txt .
RUN pip install torch --no-cache-dir --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r st_requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--browser.gatherUsageStats", "false"]