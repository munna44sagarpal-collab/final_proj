FROM python:3.9-slim

WORKDIR /app

# Minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 1: CRITICAL - Install setuptools BEFORE anything else
RUN pip install --no-cache-dir --upgrade \
    "pip==24.0" \
    "setuptools==68.0.0" \
    "wheel==0.41.0"

# Verify setuptools is installed
RUN python -c "import setuptools; print(f'setuptools {setuptools.__version__} ✓')"

# Step 2: Clear cache
RUN pip cache purge

# Step 3: Copy requirements
COPY requirements.txt .

# Step 4: Install ONLY wheels (no compilation)
RUN pip install --no-cache-dir \
    --prefer-binary \
    --only-binary :all: \
    -r requirements.txt

# Step 5: Verify packages installed
RUN python -c "import streamlit; import pandas; print('✓ All dependencies installed successfully')"

# Copy app
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
