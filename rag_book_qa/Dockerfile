# 🏗️ Base image with Python & Conda installed
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "app.py"]

