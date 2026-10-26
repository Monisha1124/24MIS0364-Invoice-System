FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG APP_VERSION=v3
ENV APP_VERSION=${APP_VERSION}
ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]
