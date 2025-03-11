FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install virtualenv && python -m venv api-venv
RUN /bin/bash -c "source api-venv/bin/activate && pip install -r requirements.txt"
COPY . .
EXPOSE 8000
CMD ["api-venv/bin/python", "-m", "fastapi", "dev", "src/app.py"]