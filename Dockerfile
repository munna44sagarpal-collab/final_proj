FROM python:3.9-slim

WORKDIR /app

# Minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 1: CLEAN pip cache before installing
RUN pip cache purge

# Step 2: Upgrade pip, setuptools, wheel ONLY
RUN pip install --no-cache-dir --upgrade \
    pip==24.0 \
    setuptools==68.0.0 \
    wheel==0.41.0

# Copy requirements FIRST (for layer caching)
COPY requirements.txt .

# Step 3: Install dependencies - wheels only, ignore conflicts
RUN pip install --no-cache-dir \
    --prefer-binary \
    --only-binary :all: \
    --no-deps \
    -r requirements.txt && \
    pip install --no-cache-dir \
    --prefer-binary \
    --only-binary :all: \
    -r requirements.txt

# Copy app
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
