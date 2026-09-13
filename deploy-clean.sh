#!/bin/bash
# Complete clean deployment script
# Removes ALL cached packages and old installs before fresh install

set -e

echo "🧹 COMPLETE CLEAN DEPLOYMENT"
echo "============================"

# Step 1: Remove old Python cache and virtual environment
echo "Step 1: Cleaning old installations..."
pip cache purge
pip freeze | xargs pip uninstall -y > /dev/null 2>&1 || true

# Step 2: Upgrade core tools
echo "Step 2: Upgrading pip, setuptools, wheel..."
pip install --no-cache-dir --upgrade \
    "pip==24.0" \
    "setuptools==68.0.0" \
    "wheel==0.41.0"

# Step 3: Install dependencies fresh (wheels only)
echo "Step 3: Installing dependencies (fresh, wheels only)..."
pip install --no-cache-dir \
    --prefer-binary \
    --only-binary :all: \
    -r requirements.txt

echo ""
echo "✅ Clean installation complete!"
echo "📊 Installed packages:"
pip list

echo ""
echo "🚀 To start the app:"
echo "   streamlit run streamlit_app.py"
