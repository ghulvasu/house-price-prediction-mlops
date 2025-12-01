# 1. Base Image
FROM python:3.9-slim

# 2. Set Working Directory
WORKDIR /app

# 3. Copy Dependencies
COPY requirements.txt .

# 4. Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project
COPY . .

# 6. Expose the port
EXPOSE 8000

# 7. Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]