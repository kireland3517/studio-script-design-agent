# Studio Script Design - AI Design Agent

A conversational AI design consultant that helps you create modern, brand-aligned website designs with 2025/2026 trends for your Studio Script Design website.

## What It Does

This agent has natural conversations with you about:
- Layout preferences (bento grids, editorial layouts, etc.)
- Interactive elements (hover effects, transitions, animations)
- Spacing and typography decisions
- Color applications
- Section-by-section design decisions

Then generates comprehensive, Wix-ready design specifications.

## Features

- **5-Stage Consultation Flow:** Discovery → Style Direction → Page-by-Page Design → Consistency Review → Specification Generation
- **2025/2026 Trends:** Suggests modern design trends aligned with your brand (kinetic typography, soft glassmorphism, generous whitespace, etc.)
- **Brand-Aware:** Embedded with Studio Script Design brand guidelines
- **Wix-Ready Output:** Generates specifications with step-by-step Wix implementation instructions
- **Context Memory:** Remembers all decisions throughout the conversation
- **Save & Resume:** Save conversations and continue later

## Setup

### 1. Install Python
Make sure you have Python 3.8+ installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
cd design-agent
pip install -r requirements.txt
```

### 3. Get Anthropic API Key
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key

### 4. Configure Environment
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Usage

### Start a New Consultation
```bash
python design_agent.py
```

The agent will greet you and start the consultation. Just chat naturally about your design preferences!

### During Consultation

**Commands:**
- Type normally to chat with the agent
- Type `save` to save the current conversation
- Type `spec` to generate design specifications
- Type `quit` to exit (auto-saves)

**Example Conversation:**
```
Agent: Hello! I'm your AI design consultant for Studio Script Design.
       Let's create something beautiful together. Which pages would you
       like to focus on today?

You: Let's start with the home page

Agent: Perfect! The home page is crucial for first impressions. I can see
       from your sitemap it has six sections: Hero, About Preview, Services,
       Portfolio Teaser, Testimonials, and a CTA.

       Before we dive into layouts, what feeling should visitors have when
       they first land on your home page?

You: I want them to feel calm but inspired, like they found clarity

Agent: Beautiful. "Calm but inspired" - that's very aligned with your
       brand promise of making complexity feel simple.

       Let's talk about style direction. I'd recommend one of these
       approaches for your home page:

       A) Editorial Elegance: Magazine-inspired with generous whitespace,
          large Playfair Display headlines, subtle scroll reveals

       B) Modern Bento: Modular card-based sections with varied sizing,
          clean Sintony headings, hover lift effects on cards

       C) Flowing Minimal: Stacked full-width sections with centered content,
          kinetic typography, soft gradient backgrounds

       Which resonates with you, or would you like a hybrid?

You: I like B but with some of the kinetic typography from C
...
```

### Generate Specifications

Once you've discussed all pages/sections, type `spec` to generate a comprehensive design specification document. The agent will create a detailed Markdown file with:

- Typography scales and specifications
- Color usage guidelines
- Spacing values
- Interactive element details (hover states, transitions)
- Section-by-section layout instructions
- Wix implementation steps
- Custom CSS snippets
- Accessibility checklist
- Asset requirements

## Output Files

The agent creates these files:

- `consultation_YYYYMMDD_HHMMSS.json` - Full conversation history (when you type 'save')
- `design_spec_YYYYMMDD_HHMMSS.md` - Design specifications (when you type 'spec')

## Project Structure

```
design-agent/
├── design_agent.py          # Main agent script
├── brand_guidelines.py      # Brand guidelines and trends
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your API key (not in git)
└── README.md               # This file
```

## Tips for Best Results

1. **Be Specific:** Instead of "I like modern design," try "I want generous spacing with subtle hover effects"
2. **Reference Examples:** "Like Apple's minimalism but warmer"
3. **Give Feedback:** The agent learns your preferences as you chat
4. **Save Often:** Type 'save' after discussing each page
5. **Ask Questions:** The agent can explain why certain trends work for your brand

## Troubleshooting

**"ANTHROPIC_API_KEY not found"**
- Make sure you created a .env file (not .env.example)
- Check that your API key is correctly formatted in .env
- Don't include quotes around the key

**Agent responses seem generic**
- The agent gets better as the conversation progresses
- Provide specific feedback about what you like/dislike
- Reference earlier decisions to maintain context

**Want to resume a saved conversation**
- Currently, you need to start fresh each time
- Use the saved JSON file as reference
- Future versions will support loading conversations

## Customization

### Adding More Trends
Edit `brand_guidelines.py` → `DESIGN_TRENDS_2025` to add new trends

### Modifying Brand Guidelines
Edit `brand_guidelines.py` → `BRAND_GUIDELINES` to update colors, fonts, etc.

### Changing Conversation Flow
Edit `design_agent.py` → `get_system_prompt()` to modify stage instructions

## Cost Estimation

The agent uses Claude Sonnet 4:
- Average consultation: 30-50 messages
- Estimated cost: $1-3 per complete website consultation
- Check current pricing: https://www.anthropic.com/pricing

## Next Steps

1. Run your first consultation
2. Review the generated design specifications
3. Implement in Wix following the step-by-step guide
4. Iterate: Run follow-up consultations for refinements

## Support

For issues or questions:
- Check this README
- Review the conversation history JSON for context
- Start a fresh consultation if things get confusing

---

**Studio Script Design**
Making Complexity Feel Simple
