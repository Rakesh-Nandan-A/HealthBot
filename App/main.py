import streamlit as st
import yaml
import json
from health_chain import HealthChain
from health_knowledge import HealthKnowledgeBase
from utils import clean_text, classify_body_type
from user_profile_manager import get_user_profile, save_user_profile
from agent_runner import initialize_health_agent

st.session_state.setdefault("page", "login")

def main():
    with open("App/auth_config.yaml") as file:
        config = yaml.safe_load(file)

    with open("App/resource/users_db.json", "r") as f:
        users = json.load(f)

    if st.session_state["page"] == "login":
        st.markdown("### 🔐 welcome to HealthBot")
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Login")

        if login_submit:
            try:
                with open("App/resource/users_db.json", "r") as f:
                    users = json.load(f)
            except FileNotFoundError:
                users = {}

            if username_input in users and users[username_input]["password"] == password_input:
                user_data = get_user_profile(username_input)
                if user_data:
                    st.session_state["user"] = username_input
                    st.success(f"Welcome back, {user_data['name']}!")
                    st.session_state["page"] = "chat"
                    st.rerun()
                else:
                    st.error("Profile not found. Please register first.")
            else:
                st.error("Invalid credentials. Please try again.")

        st.markdown("[Create New Account](#)", help="Click to register")
        if st.button("Create New Account"):
            st.session_state["page"] = "register"
            st.rerun()

    elif st.session_state["page"] == "register":
        st.markdown("### 🧾 Create Your HealthBot Account")
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            new_password = st.text_input("Password", type="password")
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
            height = st.number_input("Height (cm)", min_value=120, max_value=250)
            age = st.number_input("Age", min_value=10, max_value=100)
            gender = st.selectbox("Gender", ["male", "female", "other"])
            diet = st.selectbox("Diet Style", ["clean", "mixed", "oily/junk"])
            goal = st.selectbox("Fitness Goal", ["muscle gain", "fat loss", "general wellness"])
            register_submit = st.form_submit_button("Register")

        if register_submit:
            if not new_username or not new_password:
                st.error("Username and password are required.")
            else:
                try:
                    with open("App/resource/users_db.json", "r") as f:
                        users = json.load(f)
                except FileNotFoundError:
                    users = {}

                if new_username in users:
                    st.error("Username already exists.")
                else:
                    users[new_username] = {
                        "email": new_email,
                        "name": f"{first_name} {last_name}".strip(),
                        "password": new_password
                    }
                    with open("App/resource/users_db.json", "w") as f:
                        json.dump(users, f, indent=4)

                    bmi = round(weight / ((height / 100) ** 2), 1) if height > 0 else 0
                    body_type = classify_body_type(bmi)
                    user_data = {
                        "name": users[new_username]["name"],
                        "body_type": body_type,
                        "diet": diet,
                        "goal": goal,
                        "weight": weight,
                        "height": height,
                        "age": age,
                        "gender": gender,
                        "bmi": bmi
                    }
                    save_user_profile(new_username, user_data)
                    st.success("Registration complete! Please login.")
                    st.session_state["page"] = "login"
                    st.rerun()

        if st.button("⬅️ Back to Login"):
            st.session_state["page"] = "login"
            st.rerun()

    elif st.session_state["page"] == "chat":
        if st.button("🚪 Logout"):
            st.session_state["page"] = "login"
            st.session_state.pop("user", None)
            st.rerun()

        username = st.session_state["user"]
        user_data = get_user_profile(username)
        name = user_data["name"]
        agent = initialize_health_agent(user_data)

        st.markdown("### 🤖 HealthBot Chat")

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display previous messages
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        user_input = st.chat_input("Ask me anything health-related...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                answer = agent.run(user_input)
                st.markdown(answer)

            st.session_state.chat_history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()