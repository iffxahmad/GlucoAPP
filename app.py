import anthropic
import streamlit as st

# Function to get a meal plan from Claude AI
def get_meal_plan(api_key, fasting_level, pre_meal_level, post_meal_level, dietary_preference):
    # Initialize the Anthropics client with the provided API key
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare the prompt for Claude AI
    prompt = f"""
    You are a world-class nutritionist. Based on the following blood sugar levels and dietary preferences, generate a meal plan for a diabetic patient:

    Fasting Blood Sugar Level: {fasting_level} mg/dL
    Pre-Meal Blood Sugar Level: {pre_meal_level} mg/dL
    Post-Meal Blood Sugar Level: {post_meal_level} mg/dL
    Dietary Preference: {dietary_preference}

    Please include breakfast, lunch, dinner, and a snack option. The meals should be balanced and help in managing blood sugar levels.
    """

    # Create a message to send to Claude AI
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.5,  # Adjust the temperature for more varied meal plans
        system="You are a world-class nutritionist. Respond with a detailed meal plan.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Return the meal plan as plain text
    return message.content

# Streamlit app layout
st.title("Diabetes Meal Plan Generator")

# Load API key from secrets
api_key = st.secrets["api_keys"]["anthropic_key"]

# Input fields for user data
fasting_level = st.number_input("Fasting Blood Sugar Level (mg/dL)", min_value=0)
pre_meal_level = st.number_input("Pre-Meal Blood Sugar Level (mg/dL)", min_value=0)
post_meal_level = st.number_input("Post-Meal Blood Sugar Level (mg/dL)", min_value=0)

dietary_preference = st.selectbox(
    "Dietary Preference",
    ("Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Paleo")
)

# Button to generate meal plan
if st.button("Generate Meal Plan"):
    if api_key:
        meal_plan = get_meal_plan(api_key, fasting_level, pre_meal_level, post_meal_level, dietary_preference)
        st.subheader("Your Personalized Meal Plan")
        st.write(meal_plan)
    else:
        st.error("Please enter a valid API key.")
