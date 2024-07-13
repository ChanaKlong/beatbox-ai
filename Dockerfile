# Base Python 3.9
FROM python:3.9-slim

WORKDIR /app

# COPY REQURIMENT
COPY requirements.txt .
# Install REQURIMENT
RUN pip install --no-cache-dir -r requirements.txt

# COPY
COPY . .

# PORT
EXPOSE 5000

# RUN UVICORN
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]