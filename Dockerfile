FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 BIND_HOST=0.0.0.0 PORT=8091
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /app/venv && /app/venv/bin/pip install --no-cache-dir -r requirements.txt
COPY codebase/*.py codebase/index.html codebase/admin.html ./codebase/
COPY data/a1_demo_lesson.json ./data/a1_demo_lesson.json
USER 65532:65532
EXPOSE 8091
HEALTHCHECK --interval=30s --timeout=4s --start-period=5s CMD ["/app/venv/bin/python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8091/health', timeout=2).close()"]
CMD ["/app/venv/bin/python", "codebase/web.py"]
