import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv(dotenv_path="App/variables.env")

class HealthChain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.5,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )

    def get_daily_tip(self):
        prompt = PromptTemplate.from_template(
            """
            ### INSTRUCTION:
            Provide a concise, practical daily health tip focused on general wellness, fitness, or nutrition.
            Keep it under 50 words.
            ### HEALTH TIP:
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({})

    def answer_with_context(self, question, context_documents, user_profile=None):
        context_text = "\n\n".join(doc for doc, meta in context_documents)
        user_profile_text = ""
        if user_profile:
            user_profile_text = (
                f"### USER PROFILE:\n"
                f"Body Type: {user_profile.get('body_type')}\n"
                f"Diet: {user_profile.get('diet')}\n"
                f"Goal: {user_profile.get('goal')}\n"
                f"Weight: {user_profile.get('weight')} kg\n"
                f"Height: {user_profile.get('height')} cm\n"
                f"Age: {user_profile.get('age')}\n"
                f"Gender: {user_profile.get('gender')}\n"
                f"BMI: {user_profile.get('bmi')}\n"
            )

        prompt = PromptTemplate.from_template(
            """
            {user_profile}

            ### CONTEXT:
            {context}

            ### QUESTION:
            {question}

            ### INSTRUCTION:
            Answer the question based on the user's profile. Be specific and goal-aligned. Use the context if it's relevant, or fall back to your own health knowledge if needed.

            ### ANSWER:
            """
        )
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "question": question,
            "context": context_text,
            "user_profile": user_profile_text
        })

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))