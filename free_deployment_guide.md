# 🆓 Completely Free YouTube Tech Video Agent

**Deploy and run your YouTube video agent with ZERO costs!** No API keys, no paid services, completely free.

## ✅ What's Free?

### **100% Free Components:**
- ✅ **Content Research**: RSS feeds + Hugging Face free models
- ✅ **Video Generation**: Local TTS + OpenCV + MoviePy
- ✅ **AI Script Writing**: Free Hugging Face models (CPU)
- ✅ **Text-to-Speech**: Free pyttsx3 engine
- ✅ **Image Generation**: PIL/OpenCV for backgrounds
- ✅ **Deployment**: Render free tier + GitHub
- ✅ **Storage**: Local disk (1GB free on Render)

### **What You Need (All Free):**
- GitHub account (free)
- Render account (free tier)
- Basic Python knowledge

## 🚀 Quick Start (5 Minutes)

### **Step 1: Fork This Repository**
1. Go to your GitHub
2. Create a new repository
3. Upload all the files from this project
4. Make it public (required for Render free tier)

### **Step 2: Deploy to Render (Free)**
1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your GitHub repository**
5. **Use these settings:**

```yaml
Name: youtube-tech-agent-free
Environment: Python
Build Command: chmod +x build_free.sh && ./build_free.sh
Start Command: python main_free.py --mode automated
Instance Type: Worker (NOT Web Service)
```

### **Step 3: Environment Variables (Optional)**
Add these in Render dashboard (all optional):

```bash
VIDEO_UPLOAD_TIME=09:00
VIDEO_TOPIC=technology
VIDEO_LENGTH=60
UPLOAD_SCHEDULE=daily
LOG_LEVEL=INFO
```

### **Step 4: Add Free Disk Storage**
1. Go to service settings
2. Add Disk:
   - Name: `data`
   - Mount Path: `/app/data`
   - Size: 1GB (free)

### **Step 5: Deploy!**
Click "Create Web Service" and wait 2-3 minutes.

## 📋 How It Works (Free Method)

### **Video Creation Process:**
1. **Content Research**: Scrapes RSS feeds for trending tech topics
2. **Script Generation**: Uses free Hugging Face models
3. **Audio Generation**: Uses free pyttsx3 TTS engine
4. **Video Assembly**: Uses MoviePy + PIL for visuals
5. **Manual Upload**: Creates upload instructions file

### **Manual Upload Workflow:**
Since YouTube API costs money, we use **manual upload**:

1. **Agent creates video** and saves to `/app/data/output/`
2. **Generates upload instructions** with title, description, tags
3. **You manually upload** to YouTube Studio (takes 2 minutes)
4. **Agent continues** creating next video automatically

## 📁 File Structure (Free Version)

```
youtube-tech-agent-free/
├── main_free.py              # Main free agent
├── content_research_free.py  # Free content research
├── video_generator_free.py   # Free video generation
├── config_free.py           # Free configuration
├── requirements_free.txt    # Free dependencies
├── render_free.yaml         # Free Render config
├── free_deployment_guide.md # This guide
├── build_free.sh           # Free build script
└── README.md               # General info
```

## 🎬 Video Creation (Completely Free)

### **What Videos Look Like:**
- **Length**: 30-90 seconds (configurable)
- **Format**: MP4, 1920x1080 HD
- **Content**: Tech tutorials, programming tips, AI news
- **Style**: Text overlays on colored backgrounds
- **Audio**: Free TTS voice narration
- **Music**: Optional (royalty-free)

### **Sample Video Topics:**
- "Python Programming Tips for Beginners"
- "Machine Learning Basics Explained"
- "How to Start Coding in 2024"
- "Best Programming Languages to Learn"
- "Understanding Artificial Intelligence"

## 🔄 Automated Workflow (Free)

### **Daily Schedule:**
```
09:00 AM: Agent creates new video
09:05 AM: Video saved to output folder
09:06 AM: Upload instructions generated
09:07 AM: Ready for manual upload
Next day: Repeat automatically
```

### **What You Do:**
1. **Check Render logs** for new video notifications
2. **Download video file** from Render dashboard
3. **Follow upload instructions** (copy-paste title, description, tags)
4. **Upload to YouTube Studio** (2 minutes)
5. **Done!** Agent handles the rest

## 💰 Cost Breakdown (100% Free)

### **Monthly Costs:**
| Service | Cost | Notes |
|---------|------|-------|
| GitHub | $0 | Public repository |
| Render | $0 | 750 hours free tier |
| Hugging Face | $0 | Free models |
| YouTube | $0 | Manual upload |
| **TOTAL** | **$0** | **Completely Free!** |

### **Resource Limits (Free Tier):**
- **CPU**: 100m (sufficient for text/video processing)
- **Memory**: 512MB (enough for our needs)
- **Disk**: 1GB (stores ~50 videos)
- **Hours**: 750/month (runs 24/7)

## 🛠️ Customization (Free)

### **Change Video Topics:**
```bash
VIDEO_TOPIC=programming    # programming, ai, web-dev, mobile
VIDEO_LENGTH=90             # 30, 60, 90, 120 seconds
VIDEO_UPLOAD_TIME=14:00    # Any time in 24h format
UPLOAD_SCHEDULE=daily      # daily, weekly, monthly
```

### **Add RSS Sources:**
Edit `config_free.py` and add more feeds:
```python
RSS_FEEDS = [
    "https://your-favorite-tech-blog.com/feed",
    "https://reddit.com/r/programming/.rss",
    # Add more...
]
```

### **Change AI Model:**
```bash
AI_MODEL_NAME=microsoft/DialoGPT-small  # Faster
AI_MODEL_NAME=distilgpt2               # Even faster
```

## 📊 Monitoring (Free)

### **Check Status:**
```bash
python main_free.py --mode status
```

### **View Logs:**
- Render Dashboard → Logs tab
- Shows video creation progress
- Error messages and debugging info

### **Check Videos:**
- Render Dashboard → Shell tab
- Navigate to `/app/data/output/`
- Download videos and instructions

## 🔧 Troubleshooting (Free)

### **Common Issues:**

1. **Build Fails**
   ```bash
   # Check build_free.sh permissions
   chmod +x build_free.sh
   ```

2. **Memory Issues**
   - Use smaller AI models
   - Reduce video length
   - Lower quality settings

3. **Disk Full**
   - Videos auto-cleanup (keeps 5 latest)
   - Download and delete old videos
   - Increase disk (paid upgrade)

4. **No Videos Created**
   - Check Render logs for errors
   - Verify RSS feeds are accessible
   - Test with `python main_free.py --mode create`

## 🚀 Scaling (Still Free)

### **Multiple Channels:**
1. Create multiple Render services
2. Each with different topics
3. All on free tier

### **Better Quality (Free):**
- Use local Stable Diffusion (if available)
- Add royalty-free music
- Create custom thumbnails
- Use better fonts and colors

## 🎯 Success Tips

### **For Best Results:**
1. **Upload consistently** (same time daily)
2. **Use engaging thumbnails** (create manually)
3. **Respond to comments** (build community)
4. **Share on social media** (increase views)
5. **Monitor analytics** (improve content)

### **Content Ideas:**
- Programming tutorials
- Tech news updates
- Tool reviews
- Career advice
- Industry trends

## 📈 Next Steps

### **After You're Successful:**
1. **Upgrade to paid** for more features
2. **Add YouTube API** for auto-upload
3. **Use better AI models** for quality
4. **Scale to multiple channels**

### **Stay Free Forever:**
- Keep using manual upload
- Optimize for free tier limits
- Community contributions
- Self-host on Raspberry Pi

---

**🎉 You're ready to deploy your completely free YouTube video agent!**

**Total cost: $0.00** | **Setup time: 5 minutes** | **Maintenance: 2 minutes/day**

Start creating content and building your YouTube channel today! 🚀