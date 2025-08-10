<h1 align="center"> AI Creative & Production Studio Suite - MCP Server</h1>

<p align="center">
  <img src="puch_ai_banner.jpeg" alt="Banner image" width="500"/>
</p>

A powerful Model Context Protocol (MCP) server that provides 10 cutting-edge AI tools for creative content creation, media production, automation, and entertainment.

## 🎨 **Server Overview**

**Server Name:** AI Creative & Production Studio Suite  
**Port:** 8086  
**Status:** Ready for deployment

## 🛠️ **Available Tools**

### 🎭 **Creative Tools**
1. **AI Art Style Transfer** - Transform photos into different art styles
2. **AI Voice Cloning & Audio** - Create voice-overs and audio content
3. **AI Thumbnail Designer** - Generate eye-catching thumbnails and social media graphics

### 📺 **Media Production**
4. **AI Video Script Generator** - Create viral video scripts and storyboards
5. **AI Podcast Producer** - Generate podcast topics, scripts, and episode ideas
6. **AI Music Composer** - Generate melodies, lyrics, and full songs

### ⚡ **Automation & Productivity**
7. **AI Task Automator** - Automate repetitive tasks and create workflows
8. **AI Meeting & Calendar Assistant** - Schedule, transcribe, and optimize meetings

### 🎮 **Entertainment & Gaming**
9. **AI Gaming Tournament Organizer** - Plan and manage gaming tournaments
10. **AI Streamer & Creator Assistant** - Provide live streaming tools and audience engagement

## 🚀 **Quick Start**

### Prerequisites
- Python 3.11+
- Git
- Render account (for deployment)

### Local Development
```bash
# Clone the repository
git clone https://github.com/rishi02102017/puch-hackathon-mcp-server-3.git
cd puch-hackathon-mcp-server-3

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python creative_production_mcp.py
```

### Environment Variables
Create a `.env` file in the root directory:
```env
AUTH_TOKEN=your_auth_token_here
MY_NUMBER=your_phone_number_here
```

## 🌐 **Deployment on Render**

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
python creative_production_mcp.py
```

### Environment Variables (Render)
- `AUTH_TOKEN`: Your authentication token
- `MY_NUMBER`: Your phone number (format: country_code + number)

## 🔗 **Puch AI Integration**

1. **Deploy** the server on Render
2. **Connect** to Puch AI using: `/mcp connect <your_render_url>`
3. **Get Server ID** from Puch AI
4. **Submit** to hackathon: `/hackathon submission add <server_id> <github_url>`
5. **Share** your server: `https://puch.ai/mcp/<server_id>`

## 📋 **Tool Usage Examples**

### AI Art Style Transfer
```
Transform my photo into a Van Gogh painting style
```

### AI Voice Cloning
```
Create a professional voice-over for my YouTube video
```

### AI Video Script Generator
```
Generate a viral TikTok script about AI trends
```

### AI Podcast Producer
```
Create a podcast episode about the future of AI in gaming
```

### AI Music Composer
```
Compose an upbeat song about innovation and technology
```

## 🏆 **Hackathon Project**

This server is part of the **Puch AI Hackathon** submission, featuring:
- ✅ 10 unique AI-powered tools
- ✅ Creative content generation
- ✅ Media production automation
- ✅ Gaming and entertainment features
- ✅ Productivity enhancement tools


**Team:** Jyotishman Das and Suvadip Chakraborty
**Project:** AI Creative & Production Suite
**Hashtag:** #BuildWithPuch

## 📞 **Support**

For issues or questions:
- Check the [Puch AI Hackathon Discord](https://discord.gg/puch-ai)
- Review the [MCP Documentation](https://modelcontextprotocol.io/)

## 📄 **License**

This project is created for the Puch AI Hackathon 2025.

---

Built for **Puch AI Hackathon** - "What's the coolest way you can build with AI?"
