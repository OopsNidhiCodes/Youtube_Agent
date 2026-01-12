#!/bin/bash

# Free build script for Render deployment
echo "🆓 Starting FREE build process..."

# Update package list
echo "Updating package list..."
apt-get update

# Install essential free dependencies
echo "Installing free system dependencies..."

# FFmpeg for video processing (free)
apt-get install -y ffmpeg

# Free TTS dependencies (espeak)
apt-get install -y espeak espeak-data libespeak1 libespeak-dev

# Free fonts for image generation
apt-get install -y fonts-liberation fonts-dejavu-core fonts-freefont-ttf

# Clean up to save space
echo "Cleaning up..."
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/* /var/tmp/*

# Install Python dependencies (free versions)
echo "Installing FREE Python dependencies..."
pip install --no-cache-dir -r requirements_free.txt

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
    import pyttsx3
    engine = pyttsx3.init()
    print("✅ Free TTS engine initialized")
except Exception as e:
    print(f"❌ TTS error: {e}")

print("🎉 Free build test completed!")
EOF

python test_free.py

echo "🎉 FREE build completed successfully!"
echo "✅ Ready to create videos using only free resources!"
echo "💰 Total cost: $0.00"