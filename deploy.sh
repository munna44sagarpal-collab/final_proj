#!/bin/bash
# Fast deployment script - installs dependencies without compilation

set -e

echo "🚀 Fast Deployment Script"
echo "========================"

# Step 1: Upgrade pip
echo "Step 1: Upgrading pip..."
pip install --no-cache-dir --upgrade "pip==24.0" setuptools wheel

# Step 2: Install from requirements with wheels only
echo "Step 2: Installing dependencies (wheels only)..."
pip install --no-cache-dir \
    --prefer-binary \
    --only-binary :all: \
    -r requirements.txt

echo "✅ Installation complete! Ready to deploy."
echo ""
echo "To run locally:"
echo "  streamlit run streamlit_app.py"
