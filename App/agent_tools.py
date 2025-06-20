import random
from health_knowledge import HealthKnowledgeBase
from user_profile_manager import get_user_profile
from utils import classify_body_type

def search_docs(query: str) -> str:
    kb = HealthKnowledgeBase()
    results = kb.query_articles([query])
    if not results:
        return "No relevant articles found."
    return "\n\n".join(doc for doc, _ in results)

def get_user_profile_tool(username: str) -> str:
    profile = get_user_profile(username)
    if not profile:
        return "User profile not found."
    return f"User: {profile['name']}\nGoal: {profile['goal']}\nDiet: {profile['diet']}\nBody Type: {profile['body_type']}"

def bmi_calc_tool(weight: float, height: float) -> str:
    if height <= 0:
        return "Invalid height."
    bmi = round(weight / ((height / 100) ** 2), 1)
    body_type = classify_body_type(bmi)
    return f"BMI: {bmi} ({body_type})"

def tip_of_the_day_tool() -> str:
    tips = [
        "Stay hydrated — drink at least 2 liters of water daily.",
        "Include at least 30 minutes of movement every day.",
        "Choose whole grains over refined ones.",
        "Avoid sugary snacks and opt for fruits.",
        "Stretch regularly to improve posture and mobility."
    ]
    return random.choice(tips)