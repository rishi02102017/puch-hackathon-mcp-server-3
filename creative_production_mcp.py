import asyncio
from typing import Annotated
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, AnyUrl

import httpx
import json
import re
from datetime import datetime

# --- Load environment variables ---
load_dotenv()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

# --- Auth Provider ---
class SimpleBearerAuthProvider(BearerAuthProvider):
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="puch-client",
                scopes=["*"],
                expires_at=None,
            )
        return None

# --- Rich Tool Description models ---
class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None = None

# --- Tool Descriptions ---
ArtStyleTransferDescription = RichToolDescription(
    description="Transform photos into different art styles using AI",
    use_when="When you want to convert photos into different artistic styles like paintings, sketches, or digital art",
    side_effects=None,
)

VoiceCloningDescription = RichToolDescription(
    description="Create voice-overs and audio content with AI voice cloning",
    use_when="When you need professional voice-overs, audio content, or voice cloning for projects",
    side_effects=None,
)

PodcastProducerDescription = RichToolDescription(
    description="Generate podcast topics, scripts, and episode ideas",
    use_when="When you want to create podcast content, plan episodes, or develop podcast strategies",
    side_effects=None,
)

MusicComposerDescription = RichToolDescription(
    description="Generate melodies, lyrics, and full songs with AI",
    use_when="When you need music composition, songwriting, or musical content creation",
    side_effects=None,
)

TaskAutomatorDescription = RichToolDescription(
    description="Automate repetitive tasks and create workflows",
    use_when="When you want to automate daily tasks, create workflows, or streamline processes",
    side_effects=None,
)

MeetingCalendarAssistantDescription = RichToolDescription(
    description="Schedule, transcribe, and optimize meetings",
    use_when="When you need to manage meetings, schedule appointments, or optimize calendar productivity",
    side_effects=None,
)

GamingTournamentOrganizerDescription = RichToolDescription(
    description="Plan and manage gaming tournaments",
    use_when="When you want to organize gaming tournaments, esports events, or competitive gaming competitions",
    side_effects=None,
)

VideoScriptGeneratorDescription = RichToolDescription(
    description="Create viral video scripts and storyboards",
    use_when="When you need to create engaging video content, scripts, or storyboards for social media or marketing",
    side_effects=None,
)

ThumbnailDesignerDescription = RichToolDescription(
    description="Generate eye-catching thumbnails and social media graphics",
    use_when="When you need to create compelling thumbnails, social media posts, or visual graphics",
    side_effects=None,
)

StreamerCreatorAssistantDescription = RichToolDescription(
    description="Live streaming tools and audience engagement",
    use_when="When you want to improve your live streaming, engage with audiences, or grow your streaming channel",
    side_effects=None,
)

# --- MCP Server Setup ---
mcp = FastMCP(
    "AI Creative & Production Studio Suite",
    auth=SimpleBearerAuthProvider(TOKEN),
)

# --- Required Validate Tool ---
@mcp.tool
async def validate() -> str:
    """Validate the bearer token and return the user's phone number."""
    return MY_NUMBER

# --- AI Creative & Production Studio Tools ---

@mcp.tool(description=ArtStyleTransferDescription.model_dump_json())
async def ai_art_style_transfer(
    image_description: Annotated[str, Field(description="Description of the image you want to transform")],
    art_style: Annotated[str, Field(description="Art style: 'van_gogh', 'picasso', 'monet', 'anime', 'sketch', 'watercolor', 'oil_painting', 'digital_art'")],
    mood: Annotated[str, Field(description="Mood: 'bright', 'dark', 'vibrant', 'muted', 'dramatic', 'peaceful'")] = "vibrant",
) -> str:
    """Transform photos into different art styles using AI."""
    
    style_guide = f"""
# AI Art Style Transfer: {art_style.replace('_', ' ').title()}

## 🎨 Style Analysis
**Target Style:** {art_style.replace('_', ' ').title()}
**Image Description:** {image_description}
**Mood:** {mood.capitalize()}
**Processing Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Style Transformation Guide

### {art_style.replace('_', ' ').title()} Style Characteristics
**Van Gogh Style:**
- **Brushwork:** Bold, swirling brushstrokes
- **Colors:** Vibrant yellows, blues, and greens
- **Texture:** Thick, impasto paint application
- **Mood:** Emotional, expressive, dynamic
- **Best For:** Landscapes, portraits, still life

**Picasso Style:**
- **Technique:** Cubist geometric forms
- **Colors:** Bold, contrasting colors
- **Composition:** Fragmented, abstract shapes
- **Mood:** Modern, avant-garde, intellectual
- **Best For:** Portraits, abstract art, modern subjects

**Monet Style:**
- **Technique:** Impressionist brushwork
- **Colors:** Soft, natural light effects
- **Texture:** Loose, atmospheric strokes
- **Mood:** Peaceful, natural, light-filled
- **Best For:** Landscapes, gardens, outdoor scenes

**Anime Style:**
- **Technique:** Japanese animation style
- **Colors:** Bright, saturated colors
- **Features:** Large eyes, stylized proportions
- **Mood:** Energetic, colorful, expressive
- **Best For:** Portraits, characters, fantasy scenes

**Sketch Style:**
- **Technique:** Pencil or charcoal drawing
- **Colors:** Monochromatic or limited palette
- **Texture:** Fine lines and shading
- **Mood:** Classic, artistic, detailed
- **Best For:** Portraits, architectural drawings, studies

**Watercolor Style:**
- **Technique:** Transparent paint washes
- **Colors:** Soft, flowing color transitions
- **Texture:** Fluid, organic blending
- **Mood:** Gentle, dreamy, ethereal
- **Best For:** Landscapes, flowers, soft subjects

**Oil Painting Style:**
- **Technique:** Traditional oil painting
- **Colors:** Rich, layered colors
- **Texture:** Smooth, blended brushwork
- **Mood:** Classic, sophisticated, timeless
- **Best For:** Portraits, still life, traditional subjects

**Digital Art Style:**
- **Technique:** Modern digital painting
- **Colors:** Vibrant, contemporary palette
- **Texture:** Smooth, clean digital finish
- **Mood:** Modern, sleek, professional
- **Best For:** Concept art, illustrations, modern subjects

## 🎨 Color Palette Recommendations

### {mood.capitalize()} Mood Palette
**Bright Mood:**
- Primary: Vibrant yellows, oranges, bright blues
- Accent: Pure whites, electric pinks, lime greens
- Contrast: Deep blacks, rich purples

**Dark Mood:**
- Primary: Deep blues, purples, dark greens
- Accent: Muted grays, dark reds, navy blues
- Contrast: Bright highlights, warm whites

**Vibrant Mood:**
- Primary: Saturated reds, blues, yellows
- Accent: Electric greens, hot pinks, bright oranges
- Contrast: Pure whites, deep blacks

**Muted Mood:**
- Primary: Soft grays, beiges, pastels
- Accent: Dusty pinks, sage greens, warm browns
- Contrast: Subtle highlights, gentle shadows

**Dramatic Mood:**
- Primary: Deep reds, blacks, dark purples
- Accent: Bright highlights, warm oranges
- Contrast: Stark whites, rich golds

**Peaceful Mood:**
- Primary: Soft blues, greens, lavenders
- Accent: Gentle pinks, warm creams, sage
- Contrast: Subtle highlights, soft shadows

## 🛠️ Technical Specifications

### Processing Parameters
- **Resolution:** 2048x2048 pixels (high quality)
- **Style Strength:** 85% (strong style transfer)
- **Content Preservation:** 70% (maintain original details)
- **Color Enhancement:** {mood.capitalize()} mood optimization
- **Texture Detail:** Enhanced for {art_style.replace('_', ' ').title()} style

### Output Formats
- **Primary:** High-resolution PNG (transparent background)
- **Alternative:** JPEG for web use
- **Print Ready:** 300 DPI for professional printing
- **Social Media:** Optimized for Instagram, Facebook, Twitter

## 🎯 Application Recommendations

### Best Use Cases
1. **Social Media Content:** Eye-catching posts and stories
2. **Marketing Materials:** Unique brand visuals
3. **Personal Art:** Creative self-expression
4. **Digital Products:** Unique merchandise designs
5. **Portfolio Pieces:** Showcase artistic versatility

### Platform Optimization
- **Instagram:** Square format, vibrant colors
- **TikTok:** Vertical format, trending styles
- **YouTube:** Thumbnail optimization, bold styles
- **LinkedIn:** Professional, subtle styles
- **Twitter:** High contrast, readable styles

## 💡 Pro Tips
- **Experiment with different styles** to find your signature look
- **Consider your audience** when choosing styles
- **Maintain brand consistency** across transformations
- **Use style transfer for inspiration** in original artwork
- **Combine multiple styles** for unique hybrid effects
- **Save original images** before transformation
- **Test different moods** to match content tone
- **Optimize for your target platform** specifications
"""
    
    return style_guide

@mcp.tool(description=VoiceCloningDescription.model_dump_json())
async def ai_voice_cloning_audio(
    voice_type: Annotated[str, Field(description="Type of voice: 'professional', 'casual', 'narrator', 'character', 'celebrity'")],
    content_type: Annotated[str, Field(description="Content type: 'voice_over', 'podcast', 'audiobook', 'commercial', 'character_voice'")] = "voice_over",
    language: Annotated[str, Field(description="Language: 'english', 'spanish', 'french', 'german', 'hindi', 'chinese'")] = "english",
) -> str:
    """Create voice-overs and audio content with AI voice cloning."""
    
    voice_guide = f"""
# AI Voice Cloning & Audio Production Guide

## 🎤 Voice Analysis
**Voice Type:** {voice_type.capitalize()}
**Content Type:** {content_type.replace('_', ' ').title()}
**Language:** {language.capitalize()}
**Production Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Voice Type Characteristics

### {voice_type.capitalize()} Voice Profile
**Professional Voice:**
- **Tone:** Clear, authoritative, trustworthy
- **Pace:** Moderate, measured, deliberate
- **Pitch:** Mid-range, balanced, stable
- **Emotion:** Calm, confident, reliable
- **Best For:** Business presentations, corporate videos, educational content

**Casual Voice:**
- **Tone:** Friendly, approachable, conversational
- **Pace:** Natural, relaxed, flowing
- **Pitch:** Varied, expressive, dynamic
- **Emotion:** Warm, engaging, relatable
- **Best For:** Social media content, casual videos, personal projects

**Narrator Voice:**
- **Tone:** Rich, engaging, storytelling
- **Pace:** Varied, dramatic, expressive
- **Pitch:** Deep, resonant, captivating
- **Emotion:** Immersive, emotional, compelling
- **Best For:** Documentaries, audiobooks, storytelling content

**Character Voice:**
- **Tone:** Unique, distinctive, memorable
- **Pace:** Dynamic, expressive, animated
- **Pitch:** Varied, creative, distinctive
- **Emotion:** Expressive, engaging, entertaining
- **Best For:** Animation, gaming, entertainment content

**Celebrity Voice:**
- **Tone:** Recognizable, charismatic, influential
- **Pace:** Natural, confident, engaging
- **Pitch:** Distinctive, memorable, appealing
- **Emotion:** Relatable, inspiring, aspirational
- **Best For:** Brand endorsements, promotional content, influencer videos

## 🎬 Content Type Optimization

### {content_type.replace('_', ' ').title()} Production Guide
**Voice-Over:**
- **Script Length:** 30-120 seconds optimal
- **Pacing:** Clear, measured, professional
- **Emphasis:** Key points, brand names, call-to-actions
- **Background:** Subtle music, sound effects
- **Format:** MP3, WAV, high quality

**Podcast:**
- **Duration:** 15-60 minutes
- **Style:** Conversational, engaging, natural
- **Structure:** Intro, content, outro
- **Quality:** High-fidelity, clear audio
- **Format:** MP3, optimized for streaming

**Audiobook:**
- **Pacing:** Slow, clear, expressive
- **Character Voices:** Distinct, consistent
- **Emotion:** Varied, engaging, immersive
- **Quality:** Studio-grade, noise-free
- **Format:** High-quality MP3, chapter breaks

**Commercial:**
- **Duration:** 15-60 seconds
- **Energy:** High, engaging, persuasive
- **Clarity:** Crystal clear, memorable
- **Branding:** Consistent with brand voice
- **Format:** Broadcast quality, multiple versions

**Character Voice:**
- **Uniqueness:** Distinctive, memorable
- **Consistency:** Same voice across content
- **Emotion:** Expressive, engaging
- **Personality:** Matches character traits
- **Format:** High quality, consistent processing

## 🌍 Language-Specific Considerations

### {language.capitalize()} Language Optimization
**English:**
- **Accent Options:** American, British, Australian, Indian
- **Pronunciation:** Clear, standard, widely understood
- **Pacing:** Natural, conversational
- **Cultural Nuances:** Appropriate for target audience

**Spanish:**
- **Accent Options:** Castilian, Latin American, Mexican
- **Pronunciation:** Clear, authentic, native-like
- **Pacing:** Natural, expressive
- **Cultural Nuances:** Respectful of regional differences

**French:**
- **Accent Options:** Parisian, Canadian, African
- **Pronunciation:** Elegant, clear, authentic
- **Pacing:** Sophisticated, measured
- **Cultural Nuances:** Formal vs. informal contexts

**German:**
- **Accent Options:** Standard German, Austrian, Swiss
- **Pronunciation:** Clear, precise, authoritative
- **Pacing:** Structured, professional
- **Cultural Nuances:** Formal business context

**Hindi:**
- **Accent Options:** Standard Hindi, regional variations
- **Pronunciation:** Clear, respectful, authentic
- **Pacing:** Natural, engaging
- **Cultural Nuances:** Appropriate formality levels

**Chinese:**
- **Accent Options:** Mandarin, Cantonese, regional
- **Pronunciation:** Clear, tonal accuracy
- **Pacing:** Measured, respectful
- **Cultural Nuances:** Formal vs. casual contexts

## 🛠️ Technical Specifications

### Audio Quality Standards
- **Sample Rate:** 44.1 kHz (CD quality)
- **Bit Depth:** 16-bit minimum, 24-bit preferred
- **Format:** WAV for editing, MP3 for distribution
- **Compression:** High quality, minimal artifacts
- **Noise Reduction:** Professional-grade processing

### Voice Cloning Parameters
- **Training Data:** 10-30 minutes of clear speech
- **Processing Time:** 2-4 hours for high-quality clone
- **Accuracy:** 95%+ similarity to original voice
- **Emotion Control:** Adjustable emotional range
- **Language Support:** Multi-language capabilities

## 🎯 Production Workflow

### Pre-Production
1. **Script Preparation:** Clear, well-formatted text
2. **Voice Selection:** Choose appropriate voice type
3. **Style Guide:** Define tone, pace, emotion
4. **Technical Setup:** High-quality recording environment
5. **Rehearsal:** Practice and refine delivery

### Production
1. **Recording:** High-quality audio capture
2. **Voice Cloning:** AI processing and training
3. **Text-to-Speech:** Generate audio from text
4. **Quality Check:** Review and refine output
5. **Export:** Multiple format options

### Post-Production
1. **Audio Editing:** Clean, enhance, optimize
2. **Background Music:** Appropriate, non-distracting
3. **Sound Effects:** Enhance, don't overwhelm
4. **Mastering:** Final quality optimization
5. **Distribution:** Platform-specific formatting

## 💡 Pro Tips
- **Start with clear, high-quality source audio**
- **Choose voice type that matches your brand**
- **Consider your target audience and platform**
- **Test different emotional ranges**
- **Maintain consistency across content**
- **Optimize for your distribution platform**
- **Keep backups of original recordings**
- **Regularly update voice models**
- **Respect copyright and usage rights**
- **Test with focus groups for feedback**
"""
    
    return voice_guide

@mcp.tool(description=PodcastProducerDescription.model_dump_json())
async def ai_podcast_producer(
    podcast_topic: Annotated[str, Field(description="Main topic or theme for your podcast")],
    episode_type: Annotated[str, Field(description="Episode type: 'interview', 'solo', 'panel', 'storytelling', 'educational'")] = "solo",
    target_audience: Annotated[str, Field(description="Target audience: 'beginners', 'intermediate', 'advanced', 'general'")] = "general",
) -> str:
    """Generate podcast topics, scripts, and episode ideas."""
    
    podcast_guide = f"""
# AI Podcast Producer: {podcast_topic}

## 🎙️ Podcast Analysis
**Main Topic:** {podcast_topic}
**Episode Type:** {episode_type.capitalize()}
**Target Audience:** {target_audience.capitalize()}
**Production Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Episode Structure & Content

### {episode_type.capitalize()} Episode Format
**Interview Episode:**
- **Duration:** 30-60 minutes
- **Structure:** Intro → Guest intro → Main interview → Q&A → Outro
- **Key Elements:** Guest research, thoughtful questions, engaging conversation
- **Best For:** Expert insights, diverse perspectives, networking

**Solo Episode:**
- **Duration:** 15-45 minutes
- **Structure:** Intro → Main content → Key takeaways → Outro
- **Key Elements:** Personal insights, storytelling, actionable advice
- **Best For:** Personal branding, thought leadership, tutorials

**Panel Episode:**
- **Duration:** 45-90 minutes
- **Structure:** Intro → Panel intro → Discussion → Audience Q&A → Outro
- **Key Elements:** Diverse viewpoints, moderated discussion, audience engagement
- **Best For:** Industry discussions, debates, community building

**Storytelling Episode:**
- **Duration:** 20-40 minutes
- **Structure:** Intro → Story setup → Main narrative → Reflection → Outro
- **Key Elements:** Compelling narrative, emotional connection, personal insights
- **Best For:** Personal stories, case studies, inspirational content

**Educational Episode:**
- **Duration:** 25-50 minutes
- **Structure:** Intro → Learning objectives → Main content → Summary → Outro
- **Key Elements:** Clear explanations, examples, actionable takeaways
- **Best For:** How-to content, skill development, knowledge sharing

## 📝 Episode Script Template

### Episode Title Ideas
1. **"The Ultimate Guide to {podcast_topic}"**
2. **"How to Master {podcast_topic} in 2025"**
3. **"Secrets of Successful {podcast_topic}"**
4. **"{podcast_topic}: What the Experts Won't Tell You"**
5. **"Transform Your {podcast_topic} Strategy Today"**

### Opening Hook (30 seconds)
**Engaging Question:** "What if I told you that {podcast_topic} could change your life?"
**Shocking Statistic:** "Did you know that 73% of people struggle with {podcast_topic}?"
**Personal Story:** "When I first started with {podcast_topic}, I made every mistake possible..."
**Promise:** "By the end of this episode, you'll have 5 actionable strategies for {podcast_topic}."

### Main Content Outline
**Section 1: Understanding {podcast_topic} (5-8 minutes)**
- What is {podcast_topic}?
- Why it matters in 2025
- Common misconceptions

**Section 2: Key Strategies (10-15 minutes)**
- Strategy 1: [Specific approach]
- Strategy 2: [Specific approach]
- Strategy 3: [Specific approach]
- Real-world examples

**Section 3: Implementation (8-12 minutes)**
- Step-by-step action plan
- Common pitfalls to avoid
- Tools and resources needed

**Section 4: Success Stories (5-8 minutes)**
- Case studies and examples
- Measurable results
- Lessons learned

### Closing & Call-to-Action (2-3 minutes)
**Summary:** "Today we covered..."
**Key Takeaway:** "The most important thing to remember is..."
**Next Steps:** "Your homework for this week is..."
**Call-to-Action:** "Subscribe, rate, and review the podcast"
**Teaser:** "Next week, we'll dive into..."

## 🎤 Interview Questions (if applicable)

### Guest Research Questions
1. **Background:** "What's your journey with {podcast_topic}?"
2. **Expertise:** "What unique perspective do you bring to {podcast_topic}?"
3. **Challenges:** "What's the biggest challenge in {podcast_topic} today?"
4. **Success:** "What's your biggest success story with {podcast_topic}?"
5. **Future:** "Where do you see {podcast_topic} heading in the next 5 years?"

### Audience Engagement Questions
1. **Personal:** "What's your biggest struggle with {podcast_topic}?"
2. **Practical:** "What's one thing you can implement today?"
3. **Reflection:** "How has your perspective on {podcast_topic} changed?"
4. **Action:** "What's your next step after this episode?"

## 📊 Content Calendar Ideas

### Weekly Episode Themes
**Week 1:** "Introduction to {podcast_topic}"
**Week 2:** "The Fundamentals of {podcast_topic}"
**Week 3:** "Advanced Strategies for {podcast_topic}"
**Week 4:** "Common Mistakes in {podcast_topic}"
**Week 5:** "Success Stories in {podcast_topic}"
**Week 6:** "Tools and Resources for {podcast_topic}"
**Week 7:** "Future Trends in {podcast_topic}"
**Week 8:** "Q&A Special on {podcast_topic}"

### Monthly Themes
**Month 1:** "Getting Started with {podcast_topic}"
**Month 2:** "Building Your {podcast_topic} Foundation"
**Month 3:** "Scaling Your {podcast_topic} Efforts"
**Month 4:** "Mastering {podcast_topic}"

## 🎯 Audience-Specific Content

### {target_audience.capitalize()} Audience Focus
**Beginners:**
- **Content:** Basic concepts, step-by-step guides
- **Language:** Simple, jargon-free explanations
- **Pace:** Slower, more detailed explanations
- **Examples:** Real-world, relatable scenarios

**Intermediate:**
- **Content:** Advanced techniques, optimization strategies
- **Language:** Industry terminology, technical details
- **Pace:** Moderate, balanced depth
- **Examples:** Case studies, expert insights

**Advanced:**
- **Content:** Cutting-edge strategies, expert-level insights
- **Language:** Technical, specialized terminology
- **Pace:** Fast-paced, detailed analysis
- **Examples:** Complex scenarios, expert interviews

**General:**
- **Content:** Broad appeal, diverse topics
- **Language:** Accessible, engaging storytelling
- **Pace:** Varied, dynamic presentation
- **Examples:** Universal themes, relatable stories

## 🛠️ Production Tips

### Recording Best Practices
- **Environment:** Quiet, acoustically treated space
- **Equipment:** Quality microphone, headphones
- **Software:** Professional recording software
- **Backup:** Multiple recording sources
- **Editing:** Clean, professional post-production

### Promotion Strategy
- **Social Media:** Teaser clips, behind-the-scenes
- **Email Marketing:** Episode announcements
- **Collaborations:** Guest appearances, cross-promotion
- **SEO:** Optimized titles, descriptions, transcripts
- **Community:** Engage with listeners, respond to feedback

## 💡 Pro Tips
- **Start with a clear episode outline**
- **Keep your audience in mind throughout**
- **Include actionable takeaways**
- **End with a strong call-to-action**
- **Consistency is key - stick to your schedule**
- **Engage with your audience between episodes**
- **Track analytics and adjust based on feedback**
- **Collaborate with other podcasters**
- **Repurpose content for other platforms**
- **Always have backup content ready**
"""
    
    return podcast_guide

@mcp.tool(description=MusicComposerDescription.model_dump_json())
async def ai_music_composer(
    music_genre: Annotated[str, Field(description="Music genre: 'pop', 'rock', 'electronic', 'jazz', 'classical', 'hip_hop', 'country', 'ambient'")],
    mood: Annotated[str, Field(description="Mood: 'energetic', 'calm', 'melancholic', 'uplifting', 'dramatic', 'romantic'")] = "energetic",
    duration: Annotated[str, Field(description="Duration: 'short', 'medium', 'long'")] = "medium",
) -> str:
    """Generate melodies, lyrics, and full songs with AI."""
    
    music_guide = f"""
# AI Music Composer: {music_genre.replace('_', ' ').title()}

## 🎵 Music Analysis
**Genre:** {music_genre.replace('_', ' ').title()}
**Mood:** {mood.capitalize()}
**Duration:** {duration.capitalize()}
**Composition Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎼 Genre-Specific Composition Guide

### {music_genre.replace('_', ' ').title()} Characteristics
**Pop Music:**
- **Structure:** Verse-Chorus-Verse-Chorus-Bridge-Chorus
- **Tempo:** 120-140 BPM (beats per minute)
- **Key:** Major keys, catchy melodies
- **Instruments:** Drums, bass, guitar, synthesizers
- **Lyrics:** Relatable, emotional, memorable hooks

**Rock Music:**
- **Structure:** Verse-Chorus-Verse-Chorus-Solo-Chorus
- **Tempo:** 140-180 BPM
- **Key:** Major and minor keys, power chords
- **Instruments:** Electric guitar, bass, drums, vocals
- **Lyrics:** Rebellious, emotional, storytelling

**Electronic Music:**
- **Structure:** Intro-Build-Drop-Breakdown-Build-Drop-Outro
- **Tempo:** 120-140 BPM (house), 140-160 BPM (trance)
- **Key:** Minor keys, atmospheric sounds
- **Instruments:** Synthesizers, drum machines, samples
- **Lyrics:** Minimal, atmospheric, repetitive hooks

**Jazz Music:**
- **Structure:** Head-Solo-Solo-Head (AABA form)
- **Tempo:** 80-160 BPM (varies widely)
- **Key:** Complex harmonies, modal jazz
- **Instruments:** Saxophone, piano, bass, drums
- **Lyrics:** Sophisticated, poetic, improvisational

**Classical Music:**
- **Structure:** Sonata form, theme and variations
- **Tempo:** 60-180 BPM (varies by movement)
- **Key:** Complex harmonic progressions
- **Instruments:** Orchestra, chamber ensembles
- **Lyrics:** Often instrumental, vocal pieces in multiple languages

**Hip Hop Music:**
- **Structure:** Intro-Verse-Chorus-Verse-Chorus-Outro
- **Tempo:** 80-100 BPM
- **Key:** Sample-based, loop-oriented
- **Instruments:** Drum machines, samples, bass
- **Lyrics:** Rhyming, storytelling, social commentary

**Country Music:**
- **Structure:** Verse-Chorus-Verse-Chorus-Bridge-Chorus
- **Tempo:** 80-120 BPM
- **Key:** Major keys, simple harmonies
- **Instruments:** Acoustic guitar, fiddle, steel guitar
- **Lyrics:** Storytelling, rural themes, emotional

**Ambient Music:**
- **Structure:** Free-form, atmospheric
- **Tempo:** 60-90 BPM (or no clear tempo)
- **Key:** Modal, atmospheric, minimal
- **Instruments:** Synthesizers, field recordings, effects
- **Lyrics:** Often instrumental, atmospheric vocals

## 🎯 Mood-Based Composition

### {mood.capitalize()} Mood Elements
**Energetic:**
- **Tempo:** Fast (140-180 BPM)
- **Rhythm:** Strong, driving beats
- **Harmony:** Major keys, bright chords
- **Melody:** Upward movement, strong hooks
- **Dynamics:** Loud, powerful sections

**Calm:**
- **Tempo:** Slow (60-80 BPM)
- **Rhythm:** Gentle, flowing patterns
- **Harmony:** Major keys, soft chords
- **Melody:** Smooth, flowing lines
- **Dynamics:** Soft, peaceful sections

**Melancholic:**
- **Tempo:** Slow to moderate (70-100 BPM)
- **Rhythm:** Gentle, reflective patterns
- **Harmony:** Minor keys, sad chords
- **Melody:** Downward movement, emotional
- **Dynamics:** Soft, intimate sections

**Uplifting:**
- **Tempo:** Moderate to fast (120-160 BPM)
- **Rhythm:** Positive, forward-moving
- **Harmony:** Major keys, bright progressions
- **Melody:** Upward movement, inspiring
- **Dynamics:** Building intensity, powerful climax

**Dramatic:**
- **Tempo:** Variable (60-160 BPM)
- **Rhythm:** Intense, driving patterns
- **Harmony:** Minor keys, tension chords
- **Melody:** Wide intervals, emotional
- **Dynamics:** Extreme contrasts, powerful

**Romantic:**
- **Tempo:** Slow to moderate (70-120 BPM)
- **Rhythm:** Gentle, flowing patterns
- **Harmony:** Major keys, warm chords
- **Melody:** Smooth, expressive lines
- **Dynamics:** Soft, intimate sections

## 📝 Lyric Writing Guide

### Song Structure Templates
**Verse 1:** Introduce the story/theme
**Chorus:** Main message, memorable hook
**Verse 2:** Develop the story/theme
**Chorus:** Repeat main message
**Bridge:** New perspective or twist
**Chorus:** Final repetition

### Lyric Writing Tips
1. **Start with a theme or emotion**
2. **Write the chorus first (most important)**
3. **Use imagery and metaphors**
4. **Keep it simple and relatable**
5. **Focus on rhythm and flow**
6. **Edit and refine multiple times**

### Sample Lyrics for {music_genre.replace('_', ' ').title()} - {mood.capitalize()} Mood
**Verse 1:**
[Genre-specific opening lines that set the mood]

**Chorus:**
[Memorable hook that captures the emotion]

**Verse 2:**
[Development of the theme/story]

**Bridge:**
[New perspective or emotional peak]

## 🎹 Musical Elements

### Chord Progressions
**Pop:** I-V-vi-IV, I-IV-V, vi-IV-I-V
**Rock:** I-IV-V, I-V-vi-IV, power chord progressions
**Electronic:** i-VI-III-VII, minor progressions
**Jazz:** ii-V-I, complex jazz harmonies
**Classical:** I-IV-V-I, classical progressions
**Hip Hop:** Sample-based, loop-oriented
**Country:** I-IV-V, simple major progressions
**Ambient:** Modal, atmospheric progressions

### Melody Writing
**Pop:** Catchy, memorable hooks
**Rock:** Strong, emotional melodies
**Electronic:** Repetitive, hypnotic patterns
**Jazz:** Complex, improvisational lines
**Classical:** Sophisticated, thematic development
**Hip Hop:** Rhythmic, spoken word
**Country:** Simple, storytelling melodies
**Ambient:** Atmospheric, minimal melodies

## ⏱️ Duration Guidelines

### {duration.capitalize()} Duration Structure
**Short (2-3 minutes):**
- **Intro:** 15-20 seconds
- **Verse 1:** 30-45 seconds
- **Chorus:** 30-45 seconds
- **Verse 2:** 30-45 seconds
- **Chorus:** 30-45 seconds
- **Outro:** 15-20 seconds

**Medium (3-5 minutes):**
- **Intro:** 20-30 seconds
- **Verse 1:** 45-60 seconds
- **Chorus:** 45-60 seconds
- **Verse 2:** 45-60 seconds
- **Chorus:** 45-60 seconds
- **Bridge:** 30-45 seconds
- **Chorus:** 45-60 seconds
- **Outro:** 20-30 seconds

**Long (5-8 minutes):**
- **Intro:** 30-45 seconds
- **Verse 1:** 60-90 seconds
- **Chorus:** 60-90 seconds
- **Verse 2:** 60-90 seconds
- **Chorus:** 60-90 seconds
- **Bridge:** 45-60 seconds
- **Instrumental:** 60-90 seconds
- **Chorus:** 60-90 seconds
- **Outro:** 30-45 seconds

## 🛠️ Production Tips

### Recording Setup
- **Quality microphone** for vocals
- **MIDI keyboard** for composition
- **Digital Audio Workstation (DAW)**
- **Virtual instruments** and plugins
- **Headphones** for monitoring

### Mixing Guidelines
- **Balance:** Clear vocal, supporting instruments
- **EQ:** Remove mud, enhance clarity
- **Compression:** Control dynamics
- **Reverb:** Add space and depth
- **Mastering:** Final polish and loudness

## 💡 Pro Tips
- **Start with a strong hook or melody**
- **Keep it simple - less is often more**
- **Focus on emotion and feeling**
- **Don't overthink - trust your instincts**
- **Collaborate with other musicians**
- **Study your favorite songs**
- **Practice regularly**
- **Record everything - you never know**
- **Get feedback from trusted listeners**
- **Keep learning and experimenting**
"""
    
    return music_guide

@mcp.tool(description=TaskAutomatorDescription.model_dump_json())
async def ai_task_automator(
    task_type: Annotated[str, Field(description="Type of task: 'email', 'data_entry', 'file_management', 'social_media', 'reporting', 'customer_service'")],
    frequency: Annotated[str, Field(description="Frequency: 'daily', 'weekly', 'monthly', 'on_demand'")] = "daily",
    complexity: Annotated[str, Field(description="Complexity: 'simple', 'moderate', 'complex'")] = "moderate",
) -> str:
    """Automate repetitive tasks and create workflows."""
    
    automation_guide = f"""
# AI Task Automator: {task_type.replace('_', ' ').title()}

## 🤖 Automation Analysis
**Task Type:** {task_type.replace('_', ' ').title()}
**Frequency:** {frequency.replace('_', ' ').title()}
**Complexity:** {complexity.capitalize()}
**Setup Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Task-Specific Automation Strategies

### {task_type.replace('_', ' ').title()} Automation Guide
**Email Automation:**
- **Auto-Responses:** Set up smart reply templates
- **Email Sorting:** Automatic categorization and labeling
- **Follow-up Reminders:** Automated follow-up sequences
- **Template Management:** Dynamic email templates
- **Best For:** Customer service, sales, marketing teams

**Data Entry Automation:**
- **Form Processing:** Auto-fill forms from databases
- **Data Validation:** Automatic error checking and correction
- **Data Migration:** Automated data transfer between systems
- **Report Generation:** Automatic data compilation
- **Best For:** Administrative tasks, data management

**File Management Automation:**
- **Auto-Organization:** Automatic file sorting and naming
- **Backup Systems:** Automated backup and sync
- **Version Control:** Automatic file versioning
- **Cleanup Routines:** Remove old/unused files
- **Best For:** Content creators, project managers

**Social Media Automation:**
- **Content Scheduling:** Auto-post at optimal times
- **Engagement Monitoring:** Track mentions and interactions
- **Hashtag Management:** Auto-generate relevant hashtags
- **Analytics Reporting:** Automatic performance reports
- **Best For:** Marketing teams, influencers, businesses

**Reporting Automation:**
- **Data Collection:** Automatic data gathering from multiple sources
- **Report Generation:** Create standardized reports
- **Distribution:** Auto-send reports to stakeholders
- **Trend Analysis:** Identify patterns and insights
- **Best For:** Business analysts, managers, executives

**Customer Service Automation:**
- **Ticket Routing:** Automatic ticket assignment
- **Response Templates:** Smart response suggestions
- **Escalation Rules:** Auto-escalate urgent issues
- **Satisfaction Surveys:** Automatic feedback collection
- **Best For:** Support teams, customer success managers

## ⚙️ Automation Workflow Design

### {frequency.replace('_', ' ').title()} Workflow Structure
**Daily Automation:**
- **Morning Routine:** Check emails, update dashboards
- **Mid-day Tasks:** Process data, send reminders
- **Evening Cleanup:** Organize files, prepare next day
- **Triggers:** Time-based, event-based, manual

**Weekly Automation:**
- **Monday:** Weekly planning and goal setting
- **Mid-week:** Progress tracking and adjustments
- **Friday:** Weekly reports and cleanup
- **Weekend:** Maintenance and optimization

**Monthly Automation:**
- **Month Start:** Goal setting and planning
- **Mid-month:** Progress review and adjustments
- **Month End:** Comprehensive reporting and analysis
- **Next Month Prep:** Planning and preparation

**On-Demand Automation:**
- **Trigger Events:** Specific actions or conditions
- **Manual Activation:** User-initiated processes
- **Conditional Logic:** If-then automation rules
- **Integration Points:** Connect with other systems

## 🛠️ Technical Implementation

### {complexity.capitalize()} Complexity Setup
**Simple Automation:**
- **Tools:** Built-in app features, basic scripts
- **Setup Time:** 1-2 hours
- **Maintenance:** Minimal, occasional updates
- **Cost:** Free to low-cost solutions
- **Examples:** Email filters, calendar reminders

**Moderate Automation:**
- **Tools:** Dedicated automation platforms, APIs
- **Setup Time:** 1-2 days
- **Maintenance:** Regular monitoring and updates
- **Cost:** Mid-range subscription services
- **Examples:** Zapier workflows, IFTTT recipes

**Complex Automation:**
- **Tools:** Custom development, enterprise platforms
- **Setup Time:** 1-2 weeks
- **Maintenance:** Ongoing development and support
- **Cost:** High investment, custom development
- **Examples:** Custom software, AI-powered systems

## 🔧 Automation Tools & Platforms

### Recommended Tools by Task Type
**Email Automation:**
- **Gmail:** Filters, labels, auto-replies
- **Outlook:** Rules, templates, scheduling
- **Mailchimp:** Email marketing automation
- **Zapier:** Cross-platform email workflows

**Data Entry Automation:**
- **Google Sheets:** Formulas, scripts, add-ons
- **Microsoft Excel:** Macros, Power Query
- **Airtable:** Database automation
- **Notion:** Template automation

**File Management:**
- **Google Drive:** Auto-organize, sync
- **Dropbox:** Smart sync, version control
- **OneDrive:** Auto-backup, sharing
- **Box:** Enterprise file management

**Social Media:**
- **Buffer:** Content scheduling
- **Hootsuite:** Multi-platform management
- **Later:** Visual content planning
- **Sprout Social:** Advanced analytics

**Reporting:**
- **Google Data Studio:** Data visualization
- **Tableau:** Advanced analytics
- **Power BI:** Business intelligence
- **Looker:** Data exploration

**Customer Service:**
- **Zendesk:** Ticket automation
- **Intercom:** Chat automation
- **Freshdesk:** Support workflow
- **HubSpot:** CRM automation

## 📊 ROI & Benefits Analysis

### Expected Benefits
**Time Savings:**
- **Simple Tasks:** 2-4 hours per week
- **Moderate Tasks:** 8-12 hours per week
- **Complex Tasks:** 20+ hours per week

**Cost Reduction:**
- **Manual Labor:** Reduce repetitive work
- **Error Reduction:** Improve accuracy
- **Scalability:** Handle increased volume
- **Consistency:** Standardize processes

**Quality Improvement:**
- **Accuracy:** Reduce human errors
- **Speed:** Faster processing times
- **Consistency:** Standardized outputs
- **Compliance:** Automated rule following

## 🚀 Implementation Roadmap

### Phase 1: Assessment (Week 1)
1. **Audit Current Processes:** Identify repetitive tasks
2. **Prioritize Opportunities:** Rank by impact and effort
3. **Select Tools:** Choose appropriate automation platforms
4. **Plan Implementation:** Create detailed roadmap

### Phase 2: Setup (Week 2-3)
1. **Configure Tools:** Set up automation platforms
2. **Create Workflows:** Build initial automation rules
3. **Test Processes:** Validate automation logic
4. **Train Team:** Educate users on new processes

### Phase 3: Optimization (Week 4+)
1. **Monitor Performance:** Track automation effectiveness
2. **Gather Feedback:** Collect user input
3. **Refine Processes:** Improve automation logic
4. **Scale Success:** Expand to other areas

## 💡 Pro Tips
- **Start small** with simple, high-impact automations
- **Document everything** for future reference
- **Test thoroughly** before full deployment
- **Monitor performance** and gather feedback
- **Stay updated** with new automation tools
- **Train your team** on new processes
- **Have backup plans** for when automation fails
- **Measure ROI** to justify continued investment
- **Iterate and improve** based on results
- **Consider security** and data privacy implications
"""
    
    return automation_guide

@mcp.tool(description=MeetingCalendarAssistantDescription.model_dump_json())
async def ai_meeting_calendar_assistant(
    meeting_type: Annotated[str, Field(description="Meeting type: 'one_on_one', 'team', 'client', 'interview', 'presentation', 'brainstorming'")],
    duration: Annotated[str, Field(description="Duration: 'short', 'medium', 'long'")] = "medium",
    participants: Annotated[str, Field(description="Number of participants: 'small', 'medium', 'large'")] = "small",
) -> str:
    """Schedule, transcribe, and optimize meetings."""
    
    meeting_guide = f"""
# AI Meeting & Calendar Assistant: {meeting_type.replace('_', ' ').title()}

## 📅 Meeting Analysis
**Meeting Type:** {meeting_type.replace('_', ' ').title()}
**Duration:** {duration.capitalize()}
**Participants:** {participants.capitalize()} Group
**Planning Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Meeting Type Optimization

### {meeting_type.replace('_', ' ').title()} Meeting Guide
**One-on-One Meetings:**
- **Purpose:** Personal check-ins, feedback, coaching
- **Structure:** Open discussion, goal setting, action items
- **Tools:** Video call, screen sharing, note-taking
- **Follow-up:** Individual action items, progress tracking
- **Best Practices:** Prepare agenda, be present, document outcomes

**Team Meetings:**
- **Purpose:** Collaboration, updates, decision-making
- **Structure:** Updates, discussion, decisions, action items
- **Tools:** Video conferencing, collaborative documents
- **Follow-up:** Team action items, shared documentation
- **Best Practices:** Clear agenda, time management, equal participation

**Client Meetings:**
- **Purpose:** Relationship building, project updates, sales
- **Structure:** Introduction, agenda review, discussion, next steps
- **Tools:** Professional video platform, presentation software
- **Follow-up:** Meeting summary, action items, follow-up schedule
- **Best Practices:** Professional preparation, active listening, clear communication

**Interview Meetings:**
- **Purpose:** Candidate evaluation, skill assessment
- **Structure:** Introduction, questions, candidate questions, closing
- **Tools:** Video platform, assessment tools, note-taking
- **Follow-up:** Evaluation forms, decision process, candidate communication
- **Best Practices:** Structured questions, fair evaluation, timely feedback

**Presentation Meetings:**
- **Purpose:** Information sharing, decision-making, training
- **Structure:** Introduction, main content, Q&A, next steps
- **Tools:** Presentation software, screen sharing, recording
- **Follow-up:** Presentation materials, action items, additional resources
- **Best Practices:** Clear structure, engaging content, time management

**Brainstorming Meetings:**
- **Purpose:** Idea generation, problem-solving, innovation
- **Structure:** Problem definition, idea generation, evaluation, next steps
- **Tools:** Whiteboard, collaborative documents, voting tools
- **Follow-up:** Idea documentation, evaluation criteria, implementation plan
- **Best Practices:** Open environment, no judgment, build on ideas

## ⏱️ Duration-Based Planning

### {duration.capitalize()} Meeting Structure
**Short Meetings (15-30 minutes):**
- **Agenda Items:** 2-3 focused topics
- **Time Allocation:** 5-10 minutes per topic
- **Preparation:** Minimal, key points only
- **Follow-up:** Quick summary, immediate action items
- **Best For:** Quick updates, simple decisions, check-ins

**Medium Meetings (30-60 minutes):**
- **Agenda Items:** 3-5 topics with discussion
- **Time Allocation:** 10-15 minutes per topic
- **Preparation:** Moderate, supporting materials
- **Follow-up:** Detailed summary, action items, timeline
- **Best For:** Project updates, team discussions, planning

**Long Meetings (60+ minutes):**
- **Agenda Items:** 5+ topics with deep discussion
- **Time Allocation:** 15-20 minutes per topic
- **Preparation:** Comprehensive, detailed materials
- **Follow-up:** Comprehensive documentation, detailed action plan
- **Best For:** Strategic planning, complex decisions, training

## 👥 Participant Management

### {participants.capitalize()} Group Dynamics
**Small Groups (2-5 people):**
- **Communication:** Direct, personal interaction
- **Decision Making:** Consensus or leader decision
- **Tools:** Video call, shared documents
- **Challenges:** Limited perspectives, groupthink
- **Solutions:** Encourage diverse viewpoints, structured discussion

**Medium Groups (6-15 people):**
- **Communication:** Structured, facilitated discussion
- **Decision Making:** Voting, consensus, or committee
- **Tools:** Video platform, breakout rooms, polling
- **Challenges:** Time management, equal participation
- **Solutions:** Clear facilitation, time limits, participation tracking

**Large Groups (16+ people):**
- **Communication:** Formal presentation with Q&A
- **Decision Making:** Leadership decision with input
- **Tools:** Webinar platform, chat, polling
- **Challenges:** Limited interaction, engagement
- **Solutions:** Interactive elements, breakout sessions, clear structure

## 📝 Meeting Templates

### Pre-Meeting Checklist
**1-2 Days Before:**
- [ ] Send agenda and materials
- [ ] Confirm attendance
- [ ] Prepare presentation materials
- [ ] Test technology and tools
- [ ] Set up meeting room/space

**1 Hour Before:**
- [ ] Review agenda and objectives
- [ ] Prepare opening remarks
- [ ] Test audio/video equipment
- [ ] Have backup materials ready
- [ ] Set up recording if needed

**During Meeting:**
- [ ] Start on time
- [ ] Review agenda and objectives
- [ ] Facilitate discussion
- [ ] Track action items
- [ ] End on time with clear next steps

### Post-Meeting Actions
**Immediately After:**
- [ ] Send meeting summary
- [ ] Assign action items with deadlines
- [ ] Schedule follow-up meetings if needed
- [ ] Update project documentation
- [ ] Share relevant materials

**Within 24 Hours:**
- [ ] Send detailed meeting minutes
- [ ] Follow up on action items
- [ ] Update calendar with next meetings
- [ ] Share meeting recording if applicable
- [ ] Request feedback on meeting effectiveness

## 🛠️ Technology & Tools

### Essential Meeting Tools
**Video Conferencing:**
- **Zoom:** High-quality video, breakout rooms
- **Microsoft Teams:** Integration with Office 365
- **Google Meet:** Simple, browser-based
- **Webex:** Enterprise-grade security

**Collaboration Tools:**
- **Miro:** Virtual whiteboarding
- **Mural:** Collaborative design thinking
- **Figma:** Design collaboration
- **Notion:** Document collaboration

**Note-Taking & Documentation:**
- **Otter.ai:** AI transcription
- **Rev:** Professional transcription
- **Notion:** Meeting documentation
- **OneNote:** Microsoft ecosystem

**Calendar Management:**
- **Google Calendar:** Integration with Gmail
- **Outlook Calendar:** Microsoft ecosystem
- **Calendly:** Automated scheduling
- **Acuity Scheduling:** Advanced booking

## 📊 Meeting Analytics & Optimization

### Key Metrics to Track
**Attendance:**
- **Participation Rate:** Percentage of invited attendees
- **On-Time Rate:** Percentage starting on time
- **Engagement:** Active participation levels

**Effectiveness:**
- **Objective Achievement:** Meeting goals met
- **Decision Quality:** Quality of decisions made
- **Action Item Completion:** Follow-through rate

**Efficiency:**
- **Duration vs. Planned:** Time management
- **Agenda Coverage:** Topics completed
- **Preparation Time:** Time spent preparing

### Optimization Strategies
**Reduce Meeting Time:**
- **Strict Agendas:** Stick to planned topics
- **Time Limits:** Set time limits per topic
- **Async Preparation:** Pre-meeting materials
- **Efficient Facilitation:** Keep discussion focused

**Improve Engagement:**
- **Interactive Elements:** Polls, breakout rooms
- **Clear Roles:** Assign meeting roles
- **Equal Participation:** Encourage all voices
- **Visual Aids:** Use charts, diagrams

**Enhance Follow-up:**
- **Immediate Action Items:** Assign during meeting
- **Clear Deadlines:** Set specific timelines
- **Regular Check-ins:** Follow up on progress
- **Documentation:** Maintain meeting records

## 💡 Pro Tips
- **Always have an agenda** and share it beforehand
- **Start and end on time** to respect everyone's schedule
- **Assign a note-taker** to capture key points
- **Use the right tools** for your meeting type
- **Follow up promptly** with action items and next steps
- **Record important meetings** for future reference
- **Encourage participation** from all attendees
- **Keep meetings focused** on objectives
- **Evaluate meeting effectiveness** regularly
- **Consider async alternatives** when possible
"""
    
    return meeting_guide

@mcp.tool(description=GamingTournamentOrganizerDescription.model_dump_json())
async def ai_gaming_tournament_organizer(
    game_type: Annotated[str, Field(description="Game type: 'fps', 'moba', 'battle_royale', 'fighting', 'card_game', 'strategy'")],
    tournament_size: Annotated[str, Field(description="Tournament size: 'small', 'medium', 'large'")] = "medium",
    format_type: Annotated[str, Field(description="Format: 'single_elimination', 'double_elimination', 'round_robin', 'swiss_system'")] = "single_elimination",
) -> str:
    """Plan and manage gaming tournaments."""
    
    tournament_guide = f"""
# AI Gaming Tournament Organizer: {game_type.replace('_', ' ').title()}

## 🎮 Tournament Analysis
**Game Type:** {game_type.replace('_', ' ').title()}
**Tournament Size:** {tournament_size.capitalize()}
**Format:** {format_type.replace('_', ' ').title()}
**Planning Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Game-Specific Tournament Design

### {game_type.replace('_', ' ').title()} Tournament Structure
**FPS (First-Person Shooter):**
- **Match Duration:** 15-30 minutes per match
- **Team Size:** 5v5 or 6v6 teams
- **Maps:** 3-5 different maps in rotation
- **Format:** Best of 3 or Best of 5 series
- **Special Rules:** Overtime rules, map veto system

**MOBA (Multiplayer Online Battle Arena):**
- **Match Duration:** 30-60 minutes per match
- **Team Size:** 5v5 teams
- **Maps:** Single map (Summoner's Rift, etc.)
- **Format:** Best of 3 or Best of 5 series
- **Special Rules:** Champion bans, draft phase

**Battle Royale:**
- **Match Duration:** 20-30 minutes per match
- **Team Size:** Solo, Duo, or Squad (4 players)
- **Maps:** 1-2 maps in rotation
- **Format:** Points-based system over multiple matches
- **Special Rules:** Scoring system, placement points

**Fighting Games:**
- **Match Duration:** 2-5 minutes per match
- **Team Size:** 1v1 individual players
- **Stages:** Multiple stage selection
- **Format:** Best of 3 or Best of 5 matches
- **Special Rules:** Character bans, stage counter-picks

**Card Games:**
- **Match Duration:** 15-30 minutes per match
- **Team Size:** 1v1 individual players
- **Decks:** Pre-constructed or deck building
- **Format:** Best of 3 or Swiss system
- **Special Rules:** Deck submission, sideboard rules

**Strategy Games:**
- **Match Duration:** 30-90 minutes per match
- **Team Size:** 1v1 or 2v2 teams
- **Maps:** Multiple map options
- **Format:** Best of 3 or round-robin
- **Special Rules:** Map selection, time limits

## 📊 Tournament Size Planning

### {tournament_size.capitalize()} Tournament Structure
**Small Tournament (8-16 players):**
- **Duration:** 1-2 days
- **Venue:** Local venue or online
- **Staff:** 2-4 organizers
- **Budget:** $500-2,000
- **Prizes:** $100-500 total prize pool

**Medium Tournament (32-64 players):**
- **Duration:** 2-3 days
- **Venue:** Convention center or large online event
- **Staff:** 6-12 organizers
- **Budget:** $2,000-10,000
- **Prizes:** $500-2,000 total prize pool

**Large Tournament (128+ players):**
- **Duration:** 3-7 days
- **Venue:** Stadium or major convention center
- **Staff:** 20+ organizers
- **Budget:** $10,000-100,000+
- **Prizes:** $2,000-50,000+ total prize pool

## 🏆 Tournament Format Optimization

### {format_type.replace('_', ' ').title()} Format Guide
**Single Elimination:**
- **Structure:** Lose once, you're out
- **Duration:** Fastest format
- **Matches:** N-1 matches (N = number of players)
- **Pros:** Quick, simple, dramatic
- **Cons:** No second chances, potential for early upsets
- **Best For:** Time-constrained events, large tournaments

**Double Elimination:**
- **Structure:** Lose twice before elimination
- **Duration:** Moderate length
- **Matches:** 2N-2 matches (N = number of players)
- **Pros:** Fair, gives second chances
- **Cons:** More complex, longer duration
- **Best For:** Competitive events, medium-sized tournaments

**Round Robin:**
- **Structure:** Everyone plays everyone
- **Duration:** Longest format
- **Matches:** N(N-1)/2 matches (N = number of players)
- **Pros:** Most fair, comprehensive ranking
- **Cons:** Very long, many matches
- **Best For:** Small tournaments, league play

**Swiss System:**
- **Structure:** Players with similar records face each other
- **Duration:** Moderate length
- **Matches:** 4-6 rounds typically
- **Pros:** Fair, efficient for large groups
- **Cons:** Complex pairing system
- **Best For:** Large tournaments, card games

## 📅 Tournament Timeline

### Pre-Tournament Planning (4-8 weeks)
**Week 1-2: Concept & Planning**
- [ ] Define tournament concept and goals
- [ ] Choose game, format, and rules
- [ ] Set budget and prize pool
- [ ] Select venue or online platform
- [ ] Create tournament website/registration

**Week 3-4: Logistics & Marketing**
- [ ] Finalize venue and equipment
- [ ] Hire staff and volunteers
- [ ] Launch marketing campaign
- [ ] Open player registration
- [ ] Secure sponsorships

**Week 5-6: Preparation & Testing**
- [ ] Test all equipment and systems
- [ ] Create tournament brackets
- [ ] Prepare tournament materials
- [ ] Conduct staff training
- [ ] Finalize schedule and rules

**Week 7-8: Final Preparations**
- [ ] Confirm all registrations
- [ ] Create final brackets
- [ ] Prepare prize distribution
- [ ] Set up streaming/recording
- [ ] Conduct final walkthrough

### Tournament Day Schedule
**Day 1: Setup & Registration**
- **Morning:** Venue setup, equipment testing
- **Afternoon:** Player check-in, registration
- **Evening:** Opening ceremony, rules briefing

**Day 2: Main Tournament**
- **Morning:** Early rounds, group stages
- **Afternoon:** Quarter-finals, semi-finals
- **Evening:** Finals, awards ceremony

**Day 3: Wrap-up (if needed)**
- **Morning:** Tie-breakers, additional matches
- **Afternoon:** Awards, closing ceremony
- **Evening:** Cleanup, feedback collection

## 🛠️ Technical Requirements

### Equipment & Technology
**Hardware Requirements:**
- **Gaming PCs/Consoles:** High-performance systems
- **Monitors/Displays:** Low-latency gaming monitors
- **Audio Equipment:** Headsets, microphones
- **Network Infrastructure:** High-speed internet, LAN setup
- **Backup Equipment:** Spare systems, cables, peripherals

**Software Requirements:**
- **Tournament Management:** Bracket software, scheduling tools
- **Streaming Software:** OBS, Streamlabs, XSplit
- **Communication:** Discord, TeamSpeak, Zoom
- **Analytics:** Match tracking, statistics software
- **Security:** Anti-cheat software, monitoring tools

### Online Tournament Considerations
**Platform Requirements:**
- **Stable Internet:** High-speed, low-latency connections
- **Backup Connections:** Secondary internet options
- **Communication Tools:** Discord servers, voice channels
- **Streaming Setup:** Multiple stream options
- **Technical Support:** IT staff for troubleshooting

## 📊 Tournament Management

### Registration & Bracketing
**Registration System:**
- **Online Registration:** Website or platform-based
- **Player Information:** Name, contact, game ID, experience
- **Payment Processing:** Entry fees, merchandise
- **Waitlist Management:** Handle over-registration
- **Check-in Process:** Day-of verification

**Bracket Creation:**
- **Seeding System:** Based on rankings or random
- **Balance Considerations:** Avoid early top-player matchups
- **Format Compliance:** Follow tournament format rules
- **Backup Plans:** Handle no-shows, technical issues
- **Dynamic Updates:** Real-time bracket updates

### Prize Distribution
**Prize Pool Structure:**
- **1st Place:** 50-60% of total prize pool
- **2nd Place:** 20-30% of total prize pool
- **3rd Place:** 10-15% of total prize pool
- **4th Place:** 5-10% of total prize pool
- **Additional Prizes:** Merchandise, sponsorships

**Payment Methods:**
- **Digital Payments:** PayPal, bank transfers
- **Physical Prizes:** Trophies, merchandise
- **Tax Considerations:** Prize tax reporting
- **Timeline:** Payment within 30 days
- **Documentation:** Prize distribution records

## 🎥 Streaming & Content

### Broadcasting Setup
**Streaming Platforms:**
- **Twitch:** Primary gaming platform
- **YouTube Gaming:** Alternative platform
- **Facebook Gaming:** Social media integration
- **Multi-platform:** Reach wider audience
- **VOD Storage:** Archive for later viewing

**Content Strategy:**
- **Pre-tournament:** Player interviews, predictions
- **During Tournament:** Live matches, commentary
- **Post-tournament:** Highlights, interviews, analysis
- **Social Media:** Updates, behind-the-scenes
- **Marketing:** Promote future tournaments

### Commentary & Analysis
**Commentary Team:**
- **Play-by-Play:** Describe action as it happens
- **Color Commentary:** Provide analysis and insights
- **Expert Analysis:** Former players, coaches
- **Host:** Manage flow, interviews, transitions
- **Technical Support:** Audio, video, graphics

## 💡 Pro Tips
- **Start planning early** - tournaments take time to organize
- **Test everything** - equipment, software, internet
- **Have backup plans** - for technical issues, no-shows
- **Communicate clearly** - rules, schedule, expectations
- **Document everything** - for future tournaments
- **Gather feedback** - from players, staff, viewers
- **Build relationships** - with sponsors, venues, players
- **Stay organized** - use checklists, timelines, systems
- **Be flexible** - adapt to unexpected situations
- **Have fun** - tournaments should be enjoyable for everyone
"""
    
    return tournament_guide

@mcp.tool(description=VideoScriptGeneratorDescription.model_dump_json())
async def ai_video_script_generator(
    video_type: Annotated[str, Field(description="Video type: 'youtube', 'tiktok', 'instagram', 'commercial', 'educational', 'entertainment'")],
    target_audience: Annotated[str, Field(description="Target audience: 'gen_z', 'millennials', 'professionals', 'students', 'general'")] = "general",
    video_length: Annotated[str, Field(description="Video length: 'short', 'medium', 'long'")] = "medium",
) -> str:
    """Create viral video scripts and storyboards."""
    
    script_guide = f"""
# AI Video Script Generator: {video_type.replace('_', ' ').title()}

## 🎬 Video Analysis
**Video Type:** {video_type.replace('_', ' ').title()}
**Target Audience:** {target_audience.replace('_', ' ').title()}
**Video Length:** {video_length.capitalize()}
**Creation Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Platform-Specific Script Structure

### {video_type.replace('_', ' ').title()} Video Format
**YouTube Videos:**
- **Hook:** 5-10 seconds to grab attention
- **Introduction:** 10-30 seconds establishing context
- **Main Content:** 3-15 minutes of core content
- **Call-to-Action:** 30-60 seconds encouraging engagement
- **Outro:** 10-30 seconds wrapping up
- **Best Practices:** SEO optimization, end screens, cards

**TikTok Videos:**
- **Hook:** 1-3 seconds immediate attention grabber
- **Main Content:** 15-60 seconds fast-paced content
- **Trending Elements:** Popular sounds, effects, transitions
- **Engagement:** Questions, challenges, duets
- **Hashtags:** Relevant trending hashtags
- **Best Practices:** Vertical format, quick cuts, trending audio

**Instagram Videos:**
- **Hook:** 3-5 seconds visual or audio hook
- **Story Arc:** 15-60 seconds narrative structure
- **Visual Appeal:** High-quality visuals, filters
- **Engagement:** Questions, polls, stories
- **Call-to-Action:** Clear next steps for viewers
- **Best Practices:** Square/vertical format, aesthetic focus

**Commercial Videos:**
- **Problem:** 5-10 seconds establishing pain point
- **Solution:** 10-30 seconds introducing product/service
- **Benefits:** 15-45 seconds highlighting value
- **Call-to-Action:** 10-20 seconds clear next steps
- **Branding:** Consistent brand elements throughout
- **Best Practices:** Clear messaging, professional quality

**Educational Videos:**
- **Introduction:** 10-30 seconds setting learning objectives
- **Content Breakdown:** 2-10 minutes structured learning
- **Examples:** Real-world applications and demonstrations
- **Summary:** 30-60 seconds key takeaways
- **Next Steps:** 15-30 seconds further learning resources
- **Best Practices:** Clear structure, visual aids, engagement

**Entertainment Videos:**
- **Hook:** 5-15 seconds compelling opening
- **Story Development:** 2-10 minutes narrative progression
- **Climax:** Peak moment of interest or humor
- **Resolution:** 30-60 seconds satisfying conclusion
- **Engagement:** Encourages comments, shares, likes
- **Best Practices:** Authentic content, emotional connection

## 📝 Script Template Structure

### {video_length.capitalize()} Video Script Template
**Short Video (15-60 seconds):**
```
HOOK (0-5 seconds):
[Attention-grabbing opening]

MAIN CONTENT (5-50 seconds):
[Core message or story]

CALL-TO-ACTION (50-60 seconds):
[Engagement prompt]
```

**Medium Video (1-5 minutes):**
```
HOOK (0-10 seconds):
[Compelling opening]

INTRODUCTION (10-30 seconds):
[Context and setup]

MAIN CONTENT (30 seconds - 4:30):
[Core content with structure]

CALL-TO-ACTION (4:30-5:00):
[Clear next steps]
```

**Long Video (5+ minutes):**
```
HOOK (0-15 seconds):
[Strong opening hook]

INTRODUCTION (15-60 seconds):
[Background and context]

MAIN CONTENT (1-4 minutes):
[Structured content sections]

CONCLUSION (4-4:30):
[Summary and takeaways]

CALL-TO-ACTION (4:30-5:00):
[Engagement and next steps]
```

## 🎯 Audience-Specific Content

### {target_audience.replace('_', ' ').title()} Audience Strategy
**Gen Z (13-26 years old):**
- **Content Style:** Fast-paced, authentic, trend-focused
- **Language:** Casual, slang, emojis
- **Topics:** Social issues, trends, personal stories
- **Engagement:** Interactive, challenges, duets
- **Platforms:** TikTok, Instagram, YouTube Shorts

**Millennials (27-42 years old):**
- **Content Style:** Relatable, informative, lifestyle-focused
- **Language:** Conversational, professional-casual
- **Topics:** Career, relationships, personal growth
- **Engagement:** Comments, shares, discussions
- **Platforms:** YouTube, Instagram, LinkedIn

**Professionals (25+ years old):**
- **Content Style:** Professional, informative, value-driven
- **Language:** Clear, concise, industry-specific
- **Topics:** Industry insights, career advice, business
- **Engagement:** Networking, professional development
- **Platforms:** LinkedIn, YouTube, industry platforms

**Students (16-24 years old):**
- **Content Style:** Educational, relatable, motivational
- **Language:** Clear, engaging, age-appropriate
- **Topics:** Study tips, life advice, career guidance
- **Engagement:** Questions, study groups, mentorship
- **Platforms:** YouTube, TikTok, Instagram

**General Audience:**
- **Content Style:** Universal appeal, broad topics
- **Language:** Accessible, clear, inclusive
- **Topics:** Entertainment, education, lifestyle
- **Engagement:** Comments, likes, shares
- **Platforms:** Multiple platforms, cross-posting

## 📋 Script Writing Techniques

### Hook Writing Strategies
**Question Hooks:**
- "What if I told you..."
- "Have you ever wondered..."
- "What's the secret to..."

**Statement Hooks:**
- "This changed my life..."
- "The truth about..."
- "I discovered..."

**Action Hooks:**
- "Watch this..."
- "Look what happened..."
- "You won't believe..."

**Story Hooks:**
- "Last week, I..."
- "When I was..."
- "It all started when..."

### Call-to-Action Examples
**Engagement CTAs:**
- "Like and subscribe for more content"
- "Comment your thoughts below"
- "Share this with someone who needs it"

**Action CTAs:**
- "Click the link in the description"
- "Download our free guide"
- "Book a consultation today"

**Community CTAs:**
- "Join our community"
- "Follow us for daily tips"
- "Connect with us on social media"

## 🎨 Storyboard Elements

### Visual Planning
**Scene Breakdown:**
- **Scene 1:** Hook/Opening (5-15 seconds)
- **Scene 2:** Introduction/Setup (10-30 seconds)
- **Scene 3:** Main Content Part 1 (30-60 seconds)
- **Scene 4:** Main Content Part 2 (30-60 seconds)
- **Scene 5:** Conclusion/Call-to-Action (15-30 seconds)

**Visual Elements:**
- **Camera Angles:** Close-up, medium, wide shots
- **Transitions:** Cuts, fades, wipes, zooms
- **Graphics:** Text overlays, logos, animations
- **Background:** Location, lighting, props
- **Movement:** Camera movement, subject movement

### Audio Planning
**Voice-over Script:**
- **Tone:** Match audience and content type
- **Pace:** Appropriate for video length
- **Clarity:** Clear pronunciation, good audio quality
- **Emotion:** Match content mood and message

**Background Music:**
- **Genre:** Match content and audience
- **Volume:** Support, don't overpower
- **Timing:** Sync with video pace
- **Licensing:** Use royalty-free or licensed music

## 📊 Performance Optimization

### SEO & Discovery
**Title Optimization:**
- **Keywords:** Include relevant search terms
- **Length:** 50-60 characters optimal
- **Engagement:** Create curiosity, urgency
- **Branding:** Include channel name if relevant

**Description Optimization:**
- **First Line:** Compelling summary
- **Keywords:** Include relevant terms
- **Links:** Important links in first 3 lines
- **Structure:** Use timestamps, hashtags

**Thumbnail Optimization:**
- **Visual Impact:** Bright, clear, engaging
- **Text Overlay:** 3-5 words maximum
- **Branding:** Consistent with channel
- **Testing:** A/B test different versions

### Engagement Strategies
**Viewer Retention:**
- **Hook Quality:** Strong opening to prevent drop-off
- **Content Value:** Deliver on promise
- **Pacing:** Maintain interest throughout
- **Call-to-Action:** Clear next steps

**Community Building:**
- **Respond to Comments:** Engage with audience
- **Ask Questions:** Encourage discussion
- **Share Behind-the-Scenes:** Build connection
- **Collaborate:** Work with other creators

## 💡 Pro Tips
- **Start with a strong hook** - first 5 seconds are crucial
- **Keep it concise** - respect viewer's time
- **Tell a story** - narrative structure engages viewers
- **Include call-to-action** - guide viewer's next step
- **Optimize for platform** - each platform has different best practices
- **Test and iterate** - analyze performance and improve
- **Be authentic** - genuine content resonates better
- **Plan ahead** - create content calendar and batch produce
- **Engage with audience** - respond to comments and feedback
- **Stay consistent** - regular posting builds audience
"""
    
    return script_guide

@mcp.tool(description=ThumbnailDesignerDescription.model_dump_json())
async def ai_thumbnail_designer(
    content_type: Annotated[str, Field(description="Content type: 'youtube', 'tiktok', 'instagram', 'twitter', 'linkedin', 'gaming'")],
    style_preference: Annotated[str, Field(description="Style preference: 'bold', 'minimal', 'colorful', 'professional', 'trendy', 'vintage'")] = "bold",
    target_audience: Annotated[str, Field(description="Target audience: 'gen_z', 'millennials', 'professionals', 'gamers', 'general'")] = "general",
) -> str:
    """Generate eye-catching thumbnails and social media graphics."""
    
    thumbnail_guide = f"""
# AI Thumbnail Designer: {content_type.replace('_', ' ').title()}

## 🎨 Thumbnail Analysis
**Content Type:** {content_type.replace('_', ' ').title()}
**Style Preference:** {style_preference.capitalize()}
**Target Audience:** {target_audience.replace('_', ' ').title()}
**Design Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Platform-Specific Design Guidelines

### {content_type.replace('_', ' ').title()} Thumbnail Requirements
**YouTube Thumbnails:**
- **Dimensions:** 1280x720 pixels (16:9 ratio)
- **File Size:** Under 2MB
- **Format:** JPG, PNG, or GIF
- **Key Elements:** Title text, image, branding
- **Best Practices:** High contrast, readable text, emotional faces

**TikTok Thumbnails:**
- **Dimensions:** 1080x1920 pixels (9:16 ratio)
- **File Size:** Under 287.6MB
- **Format:** MP4, MOV, or AVI
- **Key Elements:** First frame, trending elements
- **Best Practices:** Bright colors, trending hashtags, engaging first frame

**Instagram Thumbnails:**
- **Dimensions:** 1080x1080 pixels (1:1 ratio)
- **File Size:** Under 8MB
- **Format:** JPG or PNG
- **Key Elements:** Visual appeal, hashtags, captions
- **Best Practices:** Aesthetic focus, consistent branding, high-quality images

**Twitter Thumbnails:**
- **Dimensions:** 1200x675 pixels (16:9 ratio)
- **File Size:** Under 5MB
- **Format:** JPG, PNG, or GIF
- **Key Elements:** Clear message, brand consistency
- **Best Practices:** Simple design, readable text, brand colors

**LinkedIn Thumbnails:**
- **Dimensions:** 1200x627 pixels (1.91:1 ratio)
- **File Size:** Under 5MB
- **Format:** JPG or PNG
- **Key Elements:** Professional appearance, business focus
- **Best Practices:** Clean design, professional colors, business messaging

**Gaming Thumbnails:**
- **Dimensions:** 1280x720 pixels (16:9 ratio)
- **File Size:** Under 2MB
- **Format:** JPG or PNG
- **Key Elements:** Game footage, reactions, titles
- **Best Practices:** Action shots, emotional reactions, game branding

## 🎨 Style-Specific Design Elements

### {style_preference.capitalize()} Style Guide
**Bold Style:**
- **Colors:** High contrast, vibrant colors
- **Typography:** Large, bold fonts
- **Layout:** Dynamic, asymmetrical
- **Elements:** Strong shadows, dramatic lighting
- **Best For:** Gaming, entertainment, action content

**Minimal Style:**
- **Colors:** Limited palette, neutral tones
- **Typography:** Clean, simple fonts
- **Layout:** Balanced, centered
- **Elements:** Subtle shadows, clean lines
- **Best For:** Professional, educational, business content

**Colorful Style:**
- **Colors:** Bright, saturated colors
- **Typography:** Playful, varied fonts
- **Layout:** Dynamic, energetic
- **Elements:** Gradients, patterns, textures
- **Best For:** Lifestyle, creative, fun content

**Professional Style:**
- **Colors:** Corporate colors, muted tones
- **Typography:** Professional, readable fonts
- **Layout:** Structured, organized
- **Elements:** Clean graphics, subtle effects
- **Best For:** Business, educational, corporate content

**Trendy Style:**
- **Colors:** Current color trends, gradients
- **Typography:** Modern, trendy fonts
- **Layout:** Contemporary, innovative
- **Elements:** Current design trends, effects
- **Best For:** Fashion, lifestyle, trend-focused content

**Vintage Style:**
- **Colors:** Retro colors, sepia tones
- **Typography:** Classic, retro fonts
- **Layout:** Traditional, balanced
- **Elements:** Vintage textures, retro effects
- **Best For:** Nostalgic, retro, classic content

## 👥 Audience-Specific Design Strategies

### {target_audience.replace('_', ' ').title()} Audience Design
**Gen Z (13-26 years old):**
- **Visual Style:** Bold, colorful, trend-focused
- **Typography:** Modern, trendy fonts
- **Colors:** Bright, saturated, gradient effects
- **Elements:** Emojis, trending graphics, pop culture
- **Layout:** Dynamic, asymmetrical, eye-catching

**Millennials (27-42 years old):**
- **Visual Style:** Balanced, relatable, lifestyle-focused
- **Typography:** Clean, readable fonts
- **Colors:** Balanced palette, professional with personality
- **Elements:** Lifestyle imagery, relatable content
- **Layout:** Structured but approachable

**Professionals (25+ years old):**
- **Visual Style:** Clean, professional, trustworthy
- **Typography:** Professional, readable fonts
- **Colors:** Corporate colors, muted tones
- **Elements:** Business imagery, professional graphics
- **Layout:** Structured, organized, clean

**Gamers (All ages):**
- **Visual Style:** Dynamic, action-oriented, exciting
- **Typography:** Bold, gaming-style fonts
- **Colors:** High contrast, vibrant colors
- **Elements:** Game footage, reactions, gaming icons
- **Layout:** Dynamic, energetic, attention-grabbing

**General Audience:**
- **Visual Style:** Universal appeal, clear messaging
- **Typography:** Readable, accessible fonts
- **Colors:** Balanced, appealing palette
- **Elements:** Universal imagery, clear graphics
- **Layout:** Balanced, accessible, engaging

## 🛠️ Design Tools & Resources

### Recommended Design Tools
**Free Tools:**
- **Canva:** User-friendly, templates, free version
- **GIMP:** Advanced, free alternative to Photoshop
- **Pixlr:** Online editor, browser-based
- **Snapseed:** Mobile editing, Google Photos integration
- **VSCO:** Mobile editing, filters, community

**Paid Tools:**
- **Adobe Photoshop:** Professional, industry standard
- **Adobe Illustrator:** Vector graphics, logos
- **Figma:** Collaborative design, web-based
- **Sketch:** Mac-based, UI/UX design
- **Affinity Designer:** Professional, one-time purchase

**AI Tools:**
- **Midjourney:** AI image generation
- **DALL-E:** AI art creation
- **Stable Diffusion:** Open-source AI art
- **Runway ML:** AI video and image editing
- **Remove.bg:** AI background removal

### Design Resources
**Stock Photos:**
- **Unsplash:** High-quality free photos
- **Pexels:** Free stock photos and videos
- **Pixabay:** Free images, illustrations, vectors
- **Shutterstock:** Paid, extensive library
- **Adobe Stock:** Professional stock content

**Fonts:**
- **Google Fonts:** Free, web-optimized fonts
- **DaFont:** Free fonts, extensive collection
- **Font Squirrel:** Free, commercial-use fonts
- **Adobe Fonts:** Professional font library
- **Typekit:** Adobe's font service

**Icons & Graphics:**
- **Flaticon:** Free icons and graphics
- **Icons8:** Icons, illustrations, photos
- **Freepik:** Vectors, photos, PSD files
- **Noun Project:** Simple, clear icons
- **Feather Icons:** Simple, consistent icon set

## 📊 Performance Optimization

### Click-Through Rate (CTR) Optimization
**High-Performing Elements:**
- **Faces:** Human faces, especially with emotions
- **Text:** Clear, readable, compelling titles
- **Colors:** High contrast, attention-grabbing
- **Action:** Dynamic poses, movement
- **Branding:** Consistent, recognizable elements

**A/B Testing Strategy:**
- **Test Variables:** Colors, text, images, layout
- **Sample Size:** Minimum 1000 impressions per variant
- **Duration:** 1-2 weeks for reliable results
- **Metrics:** CTR, watch time, engagement
- **Iteration:** Continuous improvement based on data

### SEO & Discovery
**Title Optimization:**
- **Keywords:** Include relevant search terms
- **Length:** 50-60 characters optimal
- **Emotion:** Create curiosity, urgency
- **Clarity:** Clear, descriptive titles

**Description Optimization:**
- **First Line:** Compelling summary
- **Keywords:** Include relevant terms
- **Links:** Important links in first 3 lines
- **Structure:** Use timestamps, hashtags

## 🎨 Design Best Practices

### Composition Guidelines
**Rule of Thirds:**
- Divide image into 9 equal parts
- Place key elements at intersection points
- Create balanced, visually appealing layout

**Visual Hierarchy:**
- Most important element largest/most prominent
- Use size, color, contrast to guide eye
- Clear reading path from top to bottom

**Color Theory:**
- **Complementary:** Opposite colors for contrast
- **Analogous:** Adjacent colors for harmony
- **Triadic:** Three colors equally spaced
- **Monochromatic:** Variations of one color

### Typography Tips
**Font Selection:**
- **Readability:** Choose clear, legible fonts
- **Hierarchy:** Use different sizes for importance
- **Consistency:** Limit to 2-3 font families
- **Branding:** Match brand personality

**Text Placement:**
- **Safe Areas:** Keep text away from edges
- **Contrast:** Ensure text is readable on background
- **Spacing:** Adequate line height and letter spacing
- **Alignment:** Consistent text alignment

## 💡 Pro Tips
- **Keep it simple** - less is often more effective
- **Test different versions** - A/B test for best performance
- **Stay consistent** - maintain brand identity across thumbnails
- **Use high-quality images** - pixelated images hurt credibility
- **Consider mobile viewing** - many users view on small screens
- **Include text overlay** - helps with SEO and clarity
- **Use emotional triggers** - faces and emotions increase engagement
- **Stay on-trend** - current design trends perform better
- **Optimize for platform** - each platform has different requirements
- **Track performance** - analyze what works and iterate
"""
    
    return thumbnail_guide

@mcp.tool(description=StreamerCreatorAssistantDescription.model_dump_json())
async def ai_streamer_creator_assistant(
    streaming_platform: Annotated[str, Field(description="Streaming platform: 'twitch', 'youtube', 'facebook', 'tiktok', 'instagram'")],
    content_type: Annotated[str, Field(description="Content type: 'gaming', 'just_chatting', 'creative', 'irl', 'educational'")] = "gaming",
    experience_level: Annotated[str, Field(description="Experience level: 'beginner', 'intermediate', 'advanced'")] = "beginner",
) -> str:
    """Live streaming tools and audience engagement."""
    
    streaming_guide = f"""
# AI Streamer & Creator Assistant: {streaming_platform.replace('_', ' ').title()}

## 🎥 Streaming Analysis
**Platform:** {streaming_platform.replace('_', ' ').title()}
**Content Type:** {content_type.replace('_', ' ').title()}
**Experience Level:** {experience_level.capitalize()}
**Setup Date:** {datetime.now().strftime('%B %d, %Y')}

## 🎯 Platform-Specific Streaming Guide

### {streaming_platform.replace('_', ' ').title()} Optimization
**Twitch Streaming:**
- **Best Times:** 7-11 PM EST, weekends peak
- **Content Focus:** Gaming, Just Chatting, Creative
- **Monetization:** Subscriptions, bits, ads, donations
- **Community:** Strong gaming community, emotes
- **Features:** Chat integration, clips, raids

**YouTube Live:**
- **Best Times:** 2-6 PM EST, consistent schedule
- **Content Focus:** Gaming, educational, lifestyle
- **Monetization:** Super Chat, memberships, ads
- **Community:** Broader audience, discoverability
- **Features:** Chat, live chat replay, highlights

**Facebook Gaming:**
- **Best Times:** 6-10 PM EST, mobile-friendly
- **Content Focus:** Mobile gaming, casual games
- **Monetization:** Stars, fan subscriptions, ads
- **Community:** Social media integration
- **Features:** Facebook integration, mobile streaming

**TikTok Live:**
- **Best Times:** 7-10 PM EST, short-form content
- **Content Focus:** Entertainment, trends, challenges
- **Monetization:** Virtual gifts, diamonds
- **Community:** Young audience, trend-focused
- **Features:** Short streams, trend integration

**Instagram Live:**
- **Best Times:** 6-9 PM EST, visual content
- **Content Focus:** Lifestyle, behind-the-scenes, Q&A
- **Monetization:** Badges, brand partnerships
- **Community:** Visual-focused, influencer audience
- **Features:** Stories integration, visual effects

## 🎮 Content Type Strategies

### {content_type.replace('_', ' ').title()} Content Guide
**Gaming Streams:**
- **Setup:** High-quality gaming PC, capture card
- **Content:** Gameplay, commentary, reactions
- **Engagement:** Chat interaction, game discussions
- **Schedule:** Regular gaming sessions, new releases
- **Growth:** Game variety, skill improvement, community

**Just Chatting Streams:**
- **Setup:** Good microphone, comfortable space
- **Content:** Personal stories, Q&A, discussions
- **Engagement:** Chat participation, topic discussions
- **Schedule:** Consistent chat times, current events
- **Growth:** Authenticity, relatability, community building

**Creative Streams:**
- **Setup:** Art supplies, digital tools, good lighting
- **Content:** Art creation, design work, tutorials
- **Engagement:** Process discussions, technique sharing
- **Schedule:** Regular creative sessions, project updates
- **Growth:** Skill development, portfolio building

**IRL (In Real Life) Streams:**
- **Setup:** Mobile streaming equipment, stable internet
- **Content:** Daily activities, travel, events
- **Engagement:** Location discussions, activity sharing
- **Schedule:** Spontaneous, event-based
- **Growth:** Authentic experiences, community connection

**Educational Streams:**
- **Setup:** Screen sharing, presentation tools
- **Content:** Tutorials, lectures, skill sharing
- **Engagement:** Q&A sessions, interactive learning
- **Schedule:** Regular educational content
- **Growth:** Expertise sharing, community learning

## 🚀 Experience Level Optimization

### {experience_level.capitalize()} Streamer Guide
**Beginner Streamers:**
- **Equipment:** Basic setup, focus on content
- **Schedule:** 2-3 streams per week, 2-4 hours each
- **Goals:** Build community, learn platform
- **Monetization:** Focus on growth, not income
- **Growth Strategy:** Consistency, authenticity, engagement

**Intermediate Streamers:**
- **Equipment:** Upgraded setup, professional quality
- **Schedule:** 4-5 streams per week, 4-6 hours each
- **Goals:** Increase viewership, develop brand
- **Monetization:** Multiple revenue streams
- **Growth Strategy:** Brand building, networking, collaboration

**Advanced Streamers:**
- **Equipment:** Professional setup, multiple platforms
- **Schedule:** Daily streams, 6+ hours each
- **Goals:** Full-time income, brand expansion
- **Monetization:** Diversified income sources
- **Growth Strategy:** Business development, team building

## 🛠️ Technical Setup Guide

### Essential Equipment
**Hardware Requirements:**
- **Computer:** High-performance PC for gaming/streaming
- **Microphone:** Quality USB or XLR microphone
- **Webcam:** HD webcam for face cam
- **Capture Card:** For console streaming
- **Lighting:** Ring light or studio lighting
- **Internet:** High-speed, stable connection

**Software Requirements:**
- **Streaming Software:** OBS Studio, Streamlabs, XSplit
- **Audio Software:** Voicemeeter, Audacity
- **Graphics Software:** Photoshop, Canva, GIMP
- **Chat Management:** StreamElements, Nightbot
- **Analytics:** Streamlabs, Twitch Analytics

### Setup Optimization
**Audio Setup:**
- **Microphone Placement:** 6-8 inches from mouth
- **Noise Reduction:** Pop filter, noise gate
- **Audio Levels:** -12dB to -6dB peak
- **Background Music:** Royalty-free music
- **Voice Effects:** Compression, equalization

**Video Setup:**
- **Resolution:** 1080p or 720p for stability
- **Frame Rate:** 30fps or 60fps for gaming
- **Bitrate:** 3000-6000 kbps for 1080p
- **Lighting:** Even, flattering lighting
- **Background:** Clean, uncluttered space

## 📊 Audience Engagement Strategies

### Chat Management
**Moderation Tools:**
- **Auto-moderation:** Filter inappropriate content
- **Moderator Team:** Trusted community members
- **Commands:** Custom chat commands
- **Timers:** Regular engagement prompts
- **Rules:** Clear community guidelines

**Engagement Techniques:**
- **Call-outs:** Acknowledge chat messages
- **Questions:** Ask for opinions and input
- **Polls:** Interactive voting systems
- **Games:** Chat-based mini-games
- **Rewards:** Channel points, loyalty programs

### Community Building
**Discord Integration:**
- **Server Setup:** Organized channels, roles
- **Events:** Regular community events
- **Exclusive Content:** Subscriber-only content
- **Networking:** Connect with other streamers
- **Feedback:** Regular community surveys

**Social Media:**
- **Cross-promotion:** Share highlights on other platforms
- **Behind-the-scenes:** Show preparation and setup
- **Community updates:** Keep followers informed
- **Collaboration:** Work with other creators
- **Trending topics:** Stay relevant and current

## 💰 Monetization Strategies

### Revenue Streams
**Platform Revenue:**
- **Subscriptions:** Monthly recurring revenue
- **Donations:** Direct viewer support
- **Bits/Tokens:** Platform-specific currency
- **Ads:** Pre-roll, mid-roll advertisements
- **Memberships:** Exclusive content access

**External Revenue:**
- **Sponsorships:** Brand partnerships
- **Merchandise:** Custom branded products
- **Patreon:** Subscription-based content
- **YouTube:** Highlight videos, tutorials
- **Consulting:** Streaming advice, coaching

### Growth Strategies
**Content Strategy:**
- **Consistency:** Regular streaming schedule
- **Quality:** High-quality audio and video
- **Variety:** Mix of content types
- **Trending:** Stay current with trends
- **Authenticity:** Be genuine and relatable

**Marketing Strategy:**
- **SEO:** Optimize stream titles and descriptions
- **Networking:** Connect with other streamers
- **Collaboration:** Cross-promotion opportunities
- **Social Media:** Active presence on platforms
- **Community:** Build and engage with audience

## 📈 Analytics & Performance

### Key Metrics to Track
**Viewership Metrics:**
- **Average Viewers:** Consistent viewership
- **Peak Viewers:** Maximum concurrent viewers
- **Watch Time:** Total hours watched
- **Retention Rate:** How long viewers stay
- **Growth Rate:** Channel growth over time

**Engagement Metrics:**
- **Chat Activity:** Messages per minute
- **Followers Gained:** New follower growth
- **Subscriptions:** Paid subscriber growth
- **Donations:** Viewer support metrics
- **Social Media:** Cross-platform engagement

### Performance Optimization
**Schedule Optimization:**
- **Best Times:** Analyze when viewers are active
- **Consistency:** Stream at same times regularly
- **Duration:** Optimal stream length for audience
- **Frequency:** Balance between content and rest
- **Events:** Special streams for growth

**Content Optimization:**
- **Game Selection:** Popular, trending games
- **Title Optimization:** SEO-friendly stream titles
- **Thumbnail Design:** Eye-catching stream previews
- **Description:** Detailed, keyword-rich descriptions
- **Tags:** Relevant, trending tags

## 💡 Pro Tips
- **Start with what you have** - don't wait for perfect equipment
- **Be consistent** - regular schedule builds audience
- **Engage with chat** - viewer interaction is key
- **Network with other streamers** - collaboration grows both channels
- **Stay authentic** - viewers connect with genuine personalities
- **Learn from analytics** - data guides improvement
- **Take breaks** - avoid burnout, maintain quality
- **Invest in quality** - upgrade equipment as you grow
- **Build community** - loyal viewers are your foundation
- **Have fun** - enjoyment translates to better content
"""
    
    return streaming_guide

# --- Main Function ---
async def main():
    """Start the MCP server."""
    print("🚀 Starting AI Creative & Production Studio Suite MCP Server...")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)

if __name__ == "__main__":
    asyncio.run(main())
