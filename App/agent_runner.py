from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from agent_tools import (
    search_docs,
    get_user_profile_tool,
    bmi_calc_tool,
    tip_of_the_day_tool
)

def initialize_health_agent(user_data: dict):
    tools = [
        Tool(
            name="HealthArticlesSearch",
            func=search_docs,
            description="Useful for answering health or nutrition-related queries using trusted article sources."
        ),
        Tool(
            name="UserProfileLookup",
            func=lambda _: f"User: {user_data['name']}, Goal: {user_data['goal']}, Diet: {user_data['diet']}, Body Type: {user_data['body_type']}",
            description="Retrieves the current user's health profile for personalized reasoning."
        ),
        Tool(
            name="BMICalculator",
            func=lambda _: f"BMI: {user_data['bmi']}, Body Type: {user_data['body_type']}",
            description="Calculates BMI and body type classification."
        ),
        Tool(
            name="DailyTip",
            func=tip_of_the_day_tool,
            description="Provides a daily health or fitness tip."
        )
    ]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = initialize_agent(
        tools=tools,
        llm=ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY")),
        agent="chat-conversational-react-description",
        memory=memory,
        verbose=True
    )
    return agent