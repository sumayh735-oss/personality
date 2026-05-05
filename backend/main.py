from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Real MBTI Engine")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://zingy-tiramisu-41c6cc.netlify.app",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================
# QUESTIONS
# =========================
QUESTIONS = [
    "I enjoy solving problems.",
    "I like planning before acting.",
    "I enjoy working with people.",
    "I like group discussions.",
    "I think about future possibilities.",
    "I prefer facts over ideas.",
    "I make logical decisions.",
    "I care about harmony.",
    "I enjoy creativity.",
    "I like structured schedules.",
    "I adapt easily.",
    "I prefer clear goals.",
    "I enjoy learning tech.",
    "I stay calm under pressure.",
    "I focus deeply.",
    "I like creative problem solving.",
    "I prefer working alone.",
    "I enjoy brainstorming.",
    "I help others learn.",
    "I think before speaking.",
    "I like organizing tasks.",
    "I trust data.",
    "I reflect deeply.",
    "I enjoy innovation.",
    "I value efficiency.",
    "I adapt quickly.",
    "I explore ideas.",
    "I finish tasks.",
    "I enjoy analysis.",
    "I like systems thinking.",
    "I enjoy leadership.",
    "I enjoy how things work.",
    "I collaborate well.",
    "I plan long term.",
    "I see patterns.",
    "I value logic.",
    "I like structure.",
    "I test new ideas.",
    "I stay focused.",
    "I like technical challenges.",
    "I enjoy concepts.",
    "I like abstract thinking.",
    "I learn by doing.",
    "I decide carefully.",
    "I build solutions.",
    "I think strategically.",
    "I take initiative.",
    "I prefer direction.",
    "I work alone well.",
    "I learn from mistakes.",
    "I improve systems.",
    "I stay goal focused.",
    "I value accuracy.",
    "I enjoy details.",
    "I adapt fast.",
    "I study independently.",
    "I like planning.",
    "I enjoy debates.",
    "I create ideas.",
    "I like progress."
]

# =========================
# INPUT
# =========================
class InputData(BaseModel):
    answers: list[int]

# =========================
# HELPERS
# =========================
def percent(score):
    score = max(-15, min(15, score))
    return round((abs(score) / 15) * 50 + 50)

def axis(score, positive, negative):
    if score >= 0:
        return {
            "side": positive,
            "percent": percent(score),
            "chart": percent(score)
        }
    return {
        "side": negative,
        "percent": percent(score),
        "chart": percent(score)
    }

# =========================
# DESCRIPTIONS
# =========================
DESCRIPTIONS = {
    "ENTJ": "Think of ENTJ as the natural-born leader personality — the type that likes to take charge, organize people, and turn big ideas into real results.",
    "INTP": "Think of INTP as the curious analyst — someone who enjoys understanding systems, exploring ideas deeply, and solving complex problems.",
    "INTJ": "Think of INTJ as the strategic architect — independent, future-focused, and naturally driven to build efficient long-term systems.",
    "ENFP": "Think of ENFP as the energetic explorer — creative, people-oriented, and motivated by possibilities, growth, and inspiration.",
}

# =========================
# STRENGTHS
# =========================
def strengths(type_code):
    data = {
        "INTP": [
            "Analytical thinking",
            "Deep curiosity",
            "Independent learning",
            "Complex problem solving"
        ],
        "INTJ": [
            "Strategic planning",
            "Long-term vision",
            "Logical decision making",
            "Systems thinking"
        ],
        "ENTJ": [
            "Leadership",
            "Execution",
            "Organization",
            "Goal orientation"
        ],
        "ENFP": [
            "Creativity",
            "Communication",
            "Inspiration",
            "Adaptability"
        ]
    }
    return data.get(type_code, [
        "Problem solving",
        "Self awareness",
        "Critical thinking"
    ])

# =========================
# CAREERS
# =========================
def careers(type_code):
    data = {
        "INTP": [
            "Software Engineer",
            "Data Scientist",
            "Research Analyst",
            "Systems Architect"
        ],
        "INTJ": [
            "Product Strategist",
            "Software Architect",
            "Engineer",
            "Research Scientist"
        ],
        "ENTJ": [
            "Founder",
            "Product Manager",
            "Business Consultant",
            "Operations Lead"
        ],
        "ENFP": [
            "UX Designer",
            "Marketing Strategist",
            "Creative Lead",
            "Community Builder"
        ]
    }

    return data.get(type_code, [
        "Developer",
        "Analyst",
        "Consultant"
    ])

# =========================
# PREDICT
# =========================
@app.post("/predict")
def predict(data: InputData):

    answers = data.answers

    if len(answers) == 0:
        answers = [0] * 60

    ei = sum(answers[:15])
    sn = sum(answers[15:30])
    tf = sum(answers[30:45])
    jp = sum(answers[45:60])

    type_code = ""
    type_code += "E" if ei >= 0 else "I"
    type_code += "S" if sn >= 0 else "N"
    type_code += "T" if tf >= 0 else "F"
    type_code += "J" if jp >= 0 else "P"

    personality_map = {
        "INTP": "INTP - The Logician",
        "INTJ": "INTJ - The Architect",
        "ENTJ": "ENTJ - The Commander",
        "ENFP": "ENFP - The Campaigner",
    }

    personality = personality_map.get(type_code, f"{type_code} - Personality")

    percentages = {
        "E/I": axis(ei, "Extravert", "Introvert"),
        "S/N": axis(sn, "Sensing", "Intuition"),
        "T/F": axis(tf, "Thinking", "Feeling"),
        "J/P": axis(jp, "Judging", "Perceiving"),
    }

    confidence = round(
        (
            abs(ei) +
            abs(sn) +
            abs(tf) +
            abs(jp)
        ) / 60 * 40 + 60
    )

    return {
        "type": personality,
        "title": type_code,
        "description": DESCRIPTIONS.get(
            type_code,
            "Your personality shows how you naturally think, make decisions, and interact with the world."
        ),
        "confidence": confidence,
        "traits": {
            "E/I": percentages["E/I"]["chart"],
            "S/N": percentages["S/N"]["chart"],
            "T/F": percentages["T/F"]["chart"],
            "J/P": percentages["J/P"]["chart"],
        },
        "percentages": percentages,
        "strengths": strengths(type_code),
        "careers": careers(type_code)
    }

# =========================
# QUESTIONS
# =========================
@app.get("/questions")
def get_questions():
    return {"questions": QUESTIONS}
