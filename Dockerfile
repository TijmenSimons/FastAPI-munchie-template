# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python", "main.py"]
