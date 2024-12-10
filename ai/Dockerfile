FROM python:3.12-slim-bullseye
WORKDIR /app
COPY . .
# Installing OpenCV environments
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "ai.py"]