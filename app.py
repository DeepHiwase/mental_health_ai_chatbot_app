from flask import Flask, render_template, request, jsonify, session
import random
import json
from datetime import datetime
import webbrowser
import google.generativeai as genai
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Change this in production


@app.route("/home")
def home():
    return render_template("index.html")


class MentalHealthCompanion:
    def __init__(self):
        self.setup_gemini()
        self.load_enhanced_resources()
        self.setup_safety_protocols()

    def setup_gemini(self):
        """Setup Gemini AI configuration"""
        try:
            # Replace with your actual Gemini API key
            self.gemini_api_key = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
            self.gemini_enabled = True
            print("Gemini AI configured successfully")
        except Exception as e:
            print(f"Gemini configuration failed: {e}")
            self.gemini_enabled = False

    def setup_safety_protocols(self):
        """Enhanced safety monitoring with Indian context"""
        self.crisis_keywords = {
            "high_risk": [
                "suicide",
                "kill myself",
                "end it all",
                "want to die",
                "harm myself",
                "end my life",
                "going to kill myself",
                "suicide plan",
                "ending it tonight",
                "better off dead",
                "no reason to live",
                "going to end it all",
                "aatma hatya",
                "khudkushi",
                "jeena band karna",
                "marne ka irada",
            ],
            "medium_risk": [
                "don't want to live",
                "tired of living",
                "can't go on",
                "give up",
                "self harm",
                "cut myself",
                "hurt myself",
                "overdose",
                "jump off",
                "nothing matters",
                "everyone would be better without me",
                "jeene ka man nahi",
                "sab khatam ho gaya",
                "kuch nahi raha",
            ],
            "low_risk": [
                "hopeless",
                "no point",
                "can't take it",
                "overwhelmed",
                "broken",
                "empty inside",
                "numb",
                "lost",
                "alone",
                "no one cares",
                "udaas",
                "nirash",
                "thak gaya",
                "akela",
            ],
        }

        self.comfort_responses = {
            "crisis_immediate": [
                "I'm deeply concerned about what you're sharing. Your safety is the most important thing right now.",
                "I hear the tremendous pain in your words. You don't have to face this alone.",
                "Thank you for sharing this with me. Let's make sure you get the support you deserve.",
            ],
            "crisis_support": [
                "It takes incredible strength to share these feelings. I'm here with you.",
                "Your feelings are completely valid. Let's find some support together.",
                "I'm so glad you reached out. You're not alone in this.",
            ],
            "comfort": [
                "I'm here with you in this moment. You're not alone.",
                "Your feelings matter, and so do you.",
                "It's okay to not be okay. I'm sitting with you in this.",
            ],
        }

    def load_enhanced_resources(self):
        """Comprehensive supportive resources with Indian helplines"""
        self.support_messages = {
            "stress": [
                "It's completely normal to feel overwhelmed sometimes. Let's breathe together for a moment... 🌬",
                "Stress can feel like carrying a heavy weight. Would you like to set it down and talk about what's happening?",
                "Remember: you've survived 100% of your difficult days so far. This moment will pass too.",
                "Let's break this down together. What's one small thing that might help right now?",
            ],
            "anxiety": [
                "Anxiety is like a wave - it builds, peaks, and passes. Let's ride this wave together... 🌊",
                "Your mind is trying to protect you, even if it feels overwhelming right now.",
                "Let's practice grounding together. Name one thing you can see, one you can touch, and one you can hear.",
                "You're safe in this moment. I'm here with you.",
            ],
            "sadness": [
                "Sadness needs space to be heard. I'm here to listen to whatever you're carrying. 💙",
                "Your feelings are welcome here. There's no need to rush through them.",
                "It's okay to grieve, to hurt, to feel deeply. These feelings make you human.",
                "Would you like to share what's in your heart? I'm listening without judgment.",
            ],
            "loneliness": [
                "Even when you feel alone, I'm here with you. You matter to me.",
                "Loneliness can feel so heavy. Thank you for reaching out - that was a brave step.",
                "You're connected right now, and your presence makes a difference.",
                "I may be an AI, but I care about your wellbeing deeply.",
            ],
            "general": [
                "I'm proud of you for being here today. That takes courage.",
                "How can I best support you in this moment?",
                "Remember to be gentle with yourself today. You're doing the best you can.",
                "Your story isn't over yet. There are still beautiful chapters to come.",
            ],
        }

        self.coping_activities = [
            "🌿 Try the 5-4-3-2-1 grounding: 5 things you see, 4 things you feel, 3 things you hear, 2 things you smell, 1 thing you taste",
            "💧 Get a glass of water and drink it slowly, noticing the temperature and sensation",
            "📝 Write three things that didn't go completely wrong today - they can be tiny things",
            "🌅 Look out a window and find one beautiful thing to focus on",
            "🎵 Listen to one song that usually brings you comfort",
            "🤗 Wrap yourself in a blanket and notice how it feels against your skin",
            "🌱 Name one small way you've grown or learned recently",
            "💖 Place your hand on your heart and take three slow breaths, noticing your heartbeat",
        ]

        self.breathing_exercises = [
            "Box breathing: Inhale 4 counts, hold 4, exhale 4, hold 4. Repeat 4 times.",
            "4-7-8 breathing: Inhale 4 counts, hold 7, exhale 8. Very calming.",
            "Simple awareness: Just notice your breath without changing it. In... and out...",
            "Ocean breath: Deep inhale, exhale like you're fogging a mirror. Soothing.",
        ]

        # Indian Helpline Numbers
        self.indian_helplines = {
            "national": [
                "Kiran Mental Health Helpline: 9152987821 (24/7)",
                "Tele MANAS: 14416 (Toll-free)",
                "AASRA: +91-9820466726 (24/7)",
                "Sneha India: 044-24640050",
            ],
            "maharashtra": [
                "Vandrevala Foundation: 022-24131212 (24/7)",
                "BMC Mental Health Helpline: 022-25521111",
                "Connecting NGO Pune: 020-25531212",
            ],
            "emergency": [
                "National Emergency: 112",
                "Police: 100",
                "Ambulance: 108",
                "Women's Helpline: 1091",
            ],
        }

    def get_gemini_response(self, user_input, user_name=""):
        """Get intelligent response from Gemini AI"""
        try:
            if not self.gemini_enabled:
                return None

            # Create a thoughtful prompt for mental health support
            prompt = f"""
            You are SafeSpace Companion, a compassionate mental health support AI. 
            The user's name is {user_name if user_name else 'friend'}.
            
            User message: "{user_input}"
            
            Please respond as a warm, empathetic mental health companion. Your response should be:
            - Supportive and validating
            - Non-judgmental and safe
            - Encouraging but not pushy
            - Focused on emotional support
            - Approximately 2-3 sentences maximum
            - Use gentle, caring language
            - Include appropriate emojis if suitable
            
            Remember: You are not a replacement for professional therapy, but a supportive listener.
            If the user mentions crisis, direct them to professional help.
            
            Your response:
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            print(f"Gemini API error: {e}")
            return None

    def assess_safety_risk(self, user_input):
        """Fast safety risk assessment"""
        input_lower = user_input.lower()

        # Check high risk first for immediate response
        for keyword in self.crisis_keywords["high_risk"]:
            if keyword in input_lower:
                return "high_risk"

        for keyword in self.crisis_keywords["medium_risk"]:
            if keyword in input_lower:
                return "medium_risk"

        for keyword in self.crisis_keywords["low_risk"]:
            if keyword in input_lower:
                return "low_risk"

        return "no_risk"

    def generate_response(self, user_input, user_name=""):
        """Generate intelligent response using Gemini AI with fallback"""
        input_lower = user_input.lower()

        # First, check for crisis content (fast path)
        risk_level = self.assess_safety_risk(user_input)

        if risk_level == "high_risk":
            return self.handle_high_risk_crisis()
        elif risk_level == "medium_risk":
            return self.handle_medium_risk_crisis()
        elif risk_level == "low_risk":
            return self.handle_low_risk_crisis()

        # Try to get Gemini response first
        gemini_response = self.get_gemini_response(user_input, user_name)
        if gemini_response:
            return gemini_response

        # Fallback to predefined responses if Gemini fails
        return self.get_fallback_response(input_lower, user_name)

    def get_fallback_response(self, input_lower, user_name):
        """Fallback response system when Gemini is unavailable"""
        # Simple greetings and basic responses
        if any(
            word in input_lower
            for word in [
                "thank",
                "thanks",
                "grateful",
                "helpful",
                "appreciate",
                "dhanyavad",
            ]
        ):
            return "Thank you for sharing that with me. It's an honor to be here with you. 💝"
        elif any(
            word in input_lower for word in ["hello", "hi", "hey", "start", "namaste"]
        ):
            if user_name:
                return f"Hello {user_name}, I'm glad you're here. How are you feeling today?"
            else:
                return "Hello, dear one. However you're feeling today, I'm glad you're here."
        elif any(word in input_lower for word in ["how are you", "how do you do"]):
            return "Thank you for asking! I'm here and fully present with you. How are you truly feeling today?"
        elif any(
            word in input_lower for word in ["what can you do", "help me", "support"]
        ):
            return "I'm here to listen, offer emotional support, and provide a safe space for you to share whatever's on your heart. You can talk to me about anything."
        elif len(input_lower.split()) <= 3:  # Very short messages
            return "I hear you. Would you like to share more about what's on your mind?"
        else:
            # Return a random supportive message from our collection
            all_messages = []
            for category in self.support_messages.values():
                all_messages.extend(category)
            return random.choice(all_messages)

    def handle_high_risk_crisis(self):
        """Handle high-risk crisis situations"""
        return {
            "message": random.choice(self.comfort_responses["crisis_immediate"])
            + " I'm deeply concerned about your safety. Your life is precious and worth protecting.",
            "crisis_level": "high",
            "show_resources": True,
        }

    def handle_medium_risk_crisis(self):
        """Handle medium-risk crisis situations"""
        return {
            "message": random.choice(self.comfort_responses["crisis_support"])
            + " Would it be helpful to see Indian mental health resources?",
            "crisis_level": "medium",
            "show_resources": True,
        }

    def handle_low_risk_crisis(self):
        """Handle low-risk crisis situations"""
        return {
            "message": "I hear how much pain you're in, and I'm really concerned. Feelings of hopelessness can be overwhelming. You're not alone in this.",
            "crisis_level": "low",
            "show_resources": False,
        }

    def get_quick_comfort(self, comfort_type):
        """Provide immediate comfort through quick buttons"""
        if comfort_type == "grounding":
            return f"Let's try this together: {random.choice(self.breathing_exercises)}"
        elif comfort_type == "comfort":
            return random.choice(self.comfort_responses["comfort"])
        elif comfort_type == "crisis":
            return self.get_indian_helplines()
        else:
            return random.choice(self.support_messages[comfort_type])

    def get_indian_helplines(self):
        """Get Indian helpline numbers"""
        return """🇮🇳 *Indian Mental Health Helplines:*

*National (24/7):*
• Kiran Helpline: 9152987821
• Tele MANAS: 14416 (Toll-free)
• AASRA: +91-9820466726

*Maharashtra:*
• Vandrevala Foundation: 022-24131212
• BMC Mental Health: 022-25521111
• Connecting Pune: 020-25531212

*Emergency:*
• National Emergency: 112
• Police: 100
• Ambulance: 108

All services are confidential and many are free."""


# Initialize the companion
companion = MentalHealthCompanion()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    name = data.get("name", "Friend")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        You are SafeSpace Companion — a warm, emotionally intelligent AI friend.
        The user's name is {name}.
        Respond naturally to their message: "{message}".
        Keep your reply 2–3 sentences, empathetic, and human-like.
        """

        response = model.generate_content(prompt)
        print("RAW GEMINI RESPONSE:", response)  # ✅ Debug output

        ai_reply = (
            getattr(response, "text", None)
            or response.candidates[0].content.parts[0].text
        ).strip()

    except Exception as e:
        print(f"[Gemini ERROR] {type(e).__name__}: {e}")
        ai_reply = (
            "I'm here with you, even if I can't find the words right now. "
            "You’re not alone in this moment. 💙"
        )

    return jsonify(
        {"message": ai_reply, "crisis_level": "none", "show_resources": False}
    )


@app.route("/quick-comfort", methods=["POST"])
def quick_comfort():
    try:
        comfort_type = request.json.get("type", "")
        response = companion.get_quick_comfort(comfort_type)

        return jsonify(
            {"message": response, "crisis_level": "none", "show_resources": False}
        )
    except Exception as e:
        return jsonify(
            {
                "message": "Let me offer you some comfort. You're not alone in this.",
                "crisis_level": "none",
                "show_resources": False,
            }
        )


@app.route("/set-name", methods=["POST"])
def set_name():
    try:
        name = request.json.get("name", "")
        session["user_name"] = name

        welcome_messages = [
            f"Hello {name}, it's truly good to meet you. However you're feeling today, you're welcome exactly as you are.",
            f"Welcome, {name}. Thank you for sharing your name with me. This is your safe space.",
            f"Hi {name}. However heavy your heart feels today, I'm here to sit with you.",
        ]

        return jsonify(
            {
                "message": random.choice(welcome_messages)
                + " You can share what's in your heart, use the comfort buttons, or just sit here in this peaceful space with me.",
                "crisis_level": "none",
                "show_resources": False,
            }
        )
    except Exception as e:
        return jsonify(
            {
                "message": "Welcome! I'm glad you're here. This is a safe space for you.",
                "crisis_level": "none",
                "show_resources": False,
            }
        )


if __name__ == "__main__":
    app.run()
    # app.run(debug=false, port=5000)
