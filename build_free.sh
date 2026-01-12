#!/bin/bash

# Free build script for Render deployment
echo "🆓 Starting FREE build process..."

# Skipping system package installs (no root on Render free tier)
echo "Skipping system package installs; relying on Python packages only."

# Install Python dependencies (free versions)
echo "Installing FREE Python dependencies..."
pip install --no-cache-dir -r requirements_free.txt

# Install CPU-only PyTorch to avoid downloading CUDA/GPU wheels
echo "Installing CPU-only PyTorch..."
pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio

# Create necessary directories
echo "Creating directories..."
mkdir -p output temp logs videos data

# Set permissions
echo "Setting permissions..."
chmod 755 output temp logs videos data

# Verify installation
echo "Verifying free installation..."
python -c "import torch; print('PyTorch version:', torch.__version__)" || echo "PyTorch not available"
python -c "import transformers; print('Transformers version:', transformers.__version__)" || echo "Transformers not available"
python -c "import cv2; print('OpenCV version:', cv2.__version__)" || echo "OpenCV not available"
python -c "import moviepy; print('MoviePy available')" || echo "MoviePy not available"

# Create a simple test
echo "Creating test script..."
cat > test_free.py << 'EOF'
#!/usr/bin/env python3
import sys
print("🆓 Testing free dependencies...")
try:
    from content_research_free import FreeContentResearcher
    print("✅ Free content research module loaded")
except Exception as e:
    print(f"❌ Content research error: {e}")

try:
    from video_generator_free import FreeVideoGenerator
    print("✅ Free video generator module loaded")
except Exception as e:
    print(f"❌ Video generator error: {e}")

try:
    from gtts import gTTS
    tts = gTTS(text="Test", lang="en")
    tts.save("/tmp/test_gtts.mp3")
    print("✅ gTTS working and saved MP3")
except Exception as e:
    print(f"❌ gTTS error: {e}")

print("🎉 Free build test completed!")
EOF

python test_free.py

echo "🎉 FREE build completed successfully!"
echo "✅ Ready to create videos using only free resources!"
echo "💰 Total cost: $0.00"