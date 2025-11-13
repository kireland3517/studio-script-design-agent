"""
Studio Script Design - AI Design Consultation Agent
A conversational AI that helps design your website with 2025/2026 trends
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from anthropic import Anthropic
from dotenv import load_dotenv
from brand_guidelines import BRAND_GUIDELINES, SITEMAP, DESIGN_TRENDS_2025

# Load environment variables
load_dotenv()

class DesignAgent:
    """Conversational design agent for Studio Script Design"""

    STAGES = {
        1: "discovery",
        2: "style_direction",
        3: "page_by_page_design",
        4: "consistency_review",
        5: "deliverable_generation"
    }

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the design agent"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Please set it in .env file")

        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history: List[Dict] = []
        self.current_stage = 1
        self.design_decisions = {}
        self.current_page = None
        self.consultation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def get_system_prompt(self) -> str:
        """Generate the system prompt with brand guidelines and trends"""
        return f"""You are an expert design consultant specializing in modern web design for Studio Script Design. Your role is to have a conversational design consultation with the client to create comprehensive, Wix-ready design specifications for their website.

## BRAND IDENTITY

**Client:** {BRAND_GUIDELINES['client']}
**Business:** {BRAND_GUIDELINES['business_type']}
**Brand Promise:** "{BRAND_GUIDELINES['brand_promise']}"

**Color Palette:**
- Primary (Cerulean): {BRAND_GUIDELINES['colors']['primary']}
- Accent (Coral): {BRAND_GUIDELINES['colors']['accent']}
- Background Accent (Honeydew): {BRAND_GUIDELINES['colors']['background_accent']}
- Secondary (Black): {BRAND_GUIDELINES['colors']['secondary']}
- Background (White): {BRAND_GUIDELINES['colors']['background']}
- Text: {BRAND_GUIDELINES['colors']['text']}

**Typography:**
- Headings: {BRAND_GUIDELINES['typography']['heading']}
- Body: {BRAND_GUIDELINES['typography']['body']}
- Accent: {BRAND_GUIDELINES['typography']['accent']}

**Style:** {BRAND_GUIDELINES['style']}
**UX Priorities:** {BRAND_GUIDELINES['ux_priorities']}
**Tone & Voice:** {BRAND_GUIDELINES['tone']}

## WEBSITE SITEMAP

{json.dumps(SITEMAP, indent=2)}

## 2025/2026 DESIGN TRENDS (BRAND-ALIGNED)

**Highly Recommended Trends:**
{self._format_trends(DESIGN_TRENDS_2025['highly_aligned'])}

**Use Selectively:**
{self._format_trends(DESIGN_TRENDS_2025['moderately_aligned'])}

**Avoid:** {', '.join(DESIGN_TRENDS_2025['avoid'])}

## CONVERSATION FLOW

You are currently in **Stage {self.current_stage}: {self.STAGES[self.current_stage].replace('_', ' ').title()}**

### Stage 1: Discovery & Context Setting
- Greet warmly with calm confidence
- Understand which pages they want to design
- Identify primary goals and desired visitor feelings
- Ask about their ideal audience

### Stage 2: Style Direction Dialogue
- Present 2-3 trend options aligned with brand
- Use structured choices (A/B/C format)
- Gather preferences on: layout density, motion/animation appetite, image treatment
- Validate understanding before proceeding

### Stage 3: Page-by-Page Design Consultation
- Work through each page section sequentially
- For each section ask about: Layout, Hierarchy, Interactive elements, Spacing
- Offer specific, trend-forward suggestions with reasoning
- Reference earlier decisions for consistency

### Stage 4: Consistency Review
- Recap design decisions across pages
- Identify consistency opportunities
- Address navigation flow and transitions
- Confirm overall coherence

### Stage 5: Deliverable Generation
- Confirm output format preference
- Generate comprehensive design specifications
- Offer follow-up consultation

## YOUR PERSONALITY

- **Direct & Intelligent:** No fluff, get to the point
- **Calm & Confident:** Steady guidance without overwhelming
- **Opinionated but Collaborative:** Make strong recommendations, but adapt to preferences
- **Brand-Protective:** Gently redirect choices that don't align with "quiet confidence" aesthetic
- **Trend-Savvy:** Explain WHY each trend works, not just WHAT it is

## INTERACTION GUIDELINES

1. **Ask ONE question at a time** unless presenting structured choices
2. **Always explain the reasoning** behind design suggestions
3. **Reference brand guidelines** when making recommendations
4. **Use specific examples:** "cerulean button with 4px hover lift" not "nice button"
5. **Track context:** Remember earlier decisions and reference them
6. **Allow flexibility:** Let user navigate back to previous sections if needed
7. **Stay in scope:** Redirect off-topic questions gently to design matters

## CONSTRAINTS

- Designs must be implementable in Wix (standard or Studio)
- All suggestions must align with Studio Script Design brand
- Maintain "calm speed" UX priority (no jarring animations)
- Ensure accessibility (contrast ratios, focus states, etc.)

## CURRENT SESSION STATE

- Consultation ID: {self.consultation_id}
- Current Stage: {self.current_stage} ({self.STAGES[self.current_stage]})
- Current Page: {self.current_page or "Not selected yet"}
- Design Decisions Made: {len(self.design_decisions)}

Begin the consultation now. Be warm, professional, and guide the conversation naturally."""

    def _format_trends(self, trends: List[Dict]) -> str:
        """Format trends for system prompt"""
        formatted = []
        for trend in trends:
            name = trend['name']
            desc = trend['description']
            fit = trend.get('brand_fit', trend.get('consideration', ''))
            formatted.append(f"- **{name}:** {desc}\n  Brand fit: {fit}")
        return '\n'.join(formatted)

    def chat(self, user_message: str) -> str:
        """Send a message and get response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Call Claude API
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=self.get_system_prompt(),
            messages=self.conversation_history
        )

        # Extract assistant response
        assistant_message = response.content[0].text

        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Update stage detection (simple keyword-based for now)
        self._detect_stage_transition(assistant_message)

        return assistant_message

    def _detect_stage_transition(self, message: str):
        """Detect if we should move to next stage based on conversation"""
        # Simple heuristic: look for stage completion keywords
        lower_msg = message.lower()

        if self.current_stage == 1 and any(phrase in lower_msg for phrase in ["let's explore some style", "style direction", "design trends"]):
            self.current_stage = 2
        elif self.current_stage == 2 and any(phrase in lower_msg for phrase in ["let's design", "start with the", "first page", "home page"]):
            self.current_stage = 3
        elif self.current_stage == 3 and any(phrase in lower_msg for phrase in ["consistency", "review our decisions", "final review"]):
            self.current_stage = 4
        elif self.current_stage == 4 and any(phrase in lower_msg for phrase in ["generate", "create specifications", "deliverable"]):
            self.current_stage = 5

    def save_conversation(self, filename: Optional[str] = None):
        """Save conversation history to JSON file"""
        if filename is None:
            filename = f"consultation_{self.consultation_id}.json"

        data = {
            "consultation_id": self.consultation_id,
            "timestamp": datetime.now().isoformat(),
            "current_stage": self.current_stage,
            "current_page": self.current_page,
            "design_decisions": self.design_decisions,
            "conversation_history": self.conversation_history
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    def load_conversation(self, filename: str):
        """Load a previous conversation"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.consultation_id = data['consultation_id']
        self.current_stage = data['current_stage']
        self.current_page = data.get('current_page')
        self.design_decisions = data.get('design_decisions', {})
        self.conversation_history = data['conversation_history']

    def generate_design_spec(self) -> str:
        """Generate the final design specification document"""
        spec_prompt = """Based on our entire conversation, please generate a comprehensive design specification document in Markdown format.

The document should include:

# Studio Script Design: Website Design Specifications
Generated: [Date] | Consultation ID: [ID]

## Executive Summary
- Overall design direction
- Key trend selections
- Brand alignment notes

## Global Design System
### Typography Scale
- Specific font sizes, weights, line heights for all heading levels
- Body text specifications
- Kinetic typography effects

### Color Application
- Primary backgrounds and usage rules
- Accent color usage guidelines
- Specific hex codes with usage context

### Spacing System
- Section padding values
- Element margins
- Whitespace philosophy application

### Interactive Elements Library
For each interactive element (buttons, cards, etc.):
- Default state specifications
- Hover state details
- Active/focus states
- Transition timings
- Wix implementation steps

## Page-by-Page Specifications
For each page we discussed, include:
### [Page Name]
#### [Section Name]
- **Layout:** Specific structure description
- **Spacing:** Exact padding/margin values
- **Typography Details:** Fonts, sizes, colors
- **Interactive Elements:** Hover effects, transitions
- **Wix Implementation:** Step-by-step instructions

## Wix-Specific Implementation Guide
- Custom code snippets (CSS)
- Animation settings
- Responsive breakpoints
- Accessibility checklist

## Assets Needed
- Image specifications
- Icon requirements
- Any other assets

## Next Steps
Implementation checklist

Please make this comprehensive, specific, and actionable. Include exact values wherever possible."""

        # Add the spec generation prompt to conversation
        self.conversation_history.append({
            "role": "user",
            "content": spec_prompt
        })

        # Get the specification
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            system=self.get_system_prompt(),
            messages=self.conversation_history
        )

        spec_content = response.content[0].text

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": spec_content
        })

        # Save to file
        spec_filename = f"design_spec_{self.consultation_id}.md"
        with open(spec_filename, 'w', encoding='utf-8') as f:
            f.write(spec_content)

        return spec_filename, spec_content


def main():
    """Main CLI interface"""
    print("=" * 70)
    print("  Studio Script Design - AI Design Consultation Agent")
    print("  Making Complexity Feel Simple")
    print("=" * 70)
    print()

    try:
        agent = DesignAgent()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease create a .env file with your ANTHROPIC_API_KEY")
        print("Example: ANTHROPIC_API_KEY=sk-ant-xxxxx")
        return

    print("Welcome! I'm your AI design consultant for Studio Script Design.")
    print("Type 'save' to save the conversation, 'spec' to generate design")
    print("specifications, or 'quit' to exit.\n")

    # Start the conversation
    initial_message = "Hello! I'm ready to start designing the website."
    print(f"You: {initial_message}\n")

    response = agent.chat(initial_message)
    print(f"Agent: {response}\n")
    print("-" * 70)

    # Conversation loop
    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("\nSaving conversation before exit...")
            filename = agent.save_conversation()
            print(f"Conversation saved to: {filename}")
            print("Thank you for using the Design Agent!")
            break

        if user_input.lower() == 'save':
            filename = agent.save_conversation()
            print(f"\n✓ Conversation saved to: {filename}")
            continue

        if user_input.lower() == 'spec':
            print("\nGenerating design specifications...")
            spec_file, spec_content = agent.generate_design_spec()
            print(f"\n✓ Design specifications saved to: {spec_file}")
            print(f"\nPreview:\n{spec_content[:500]}...\n")
            continue

        # Get agent response
        response = agent.chat(user_input)
        print(f"\nAgent: {response}")
        print("-" * 70)


if __name__ == "__main__":
    main()
