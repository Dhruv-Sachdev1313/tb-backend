# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies (including gunicorn)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Run Flask with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
