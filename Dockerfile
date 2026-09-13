FROM python:3.9-slim

WORKDIR /app

# Minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# CRITICAL: Install setuptools, pip, wheel FIRST
# This MUST run before any package installation
RUN pip install --no-cache-dir --upgrade \
    "pip==24.0" \
    "setuptools==68.0.0" \
    "wheel==0.41.0"

# Verify setuptools is installed
RUN python -c "import setuptools; print(f'setuptools {setuptools.__version__} installed')"

# Clear cache
RUN pip cache purge

# Copy requirements
COPY requirements.txt .

# Install dependencies - wheels ONLY
RUN pip install --no-cache-dir \
    --prefer-binary \
    --only-binary :all: \
    -r requirements.txt

# Copy app
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
