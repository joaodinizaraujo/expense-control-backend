FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install virtualenv
RUN python -m venv api-venv
RUN source api-venv/bin/activate
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["fastapi", "dev", "src/app.py"]