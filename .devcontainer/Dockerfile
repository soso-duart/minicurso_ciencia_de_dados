FROM mcr.microsoft.com/devcontainers/python:3.13

WORKDIR /workspace

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]
