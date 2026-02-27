import streamlit as st
import pickle
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SmartFit AI", page_icon="💪", layout="centered")

# ---------------- ULTRA DARK NEON THEME ----------------
st.markdown("""
<style>

/* Full Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Glass Container */
[data-testid="stVerticalBlock"] > div {
    background: rgba(0, 0, 0, 0.65);
    backdrop-filter: blur(20px);
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 0 40px rgba(0,255,255,0.2);
    color: white;
    animation: fadeIn 1s ease-in-out;
}

/* Fade Animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Neon Button */
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 30px;
    height: 3.2em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
    box-shadow: 0 0 20px rgba(0,198,255,0.6);
    transition: 0.3s;
}

.stButton>button:hover {
    box-shadow: 0 0 40px rgba(0,198,255,1);
    transform: scale(1.05);
}

/* Rounded Inputs */
.stNumberInput input, .stSelectbox div {
    border-radius: 12px !important;
}

section.main > div {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center;
color:#00f5ff;
font-size:50px;
text-shadow: 0 0 20px #00f5ff;'>
⚡ SmartFit AI
</h1>
<p style='text-align:center; color:white; font-size:20px;'>
Next-Gen AI Powered Fitness Planner
</p>
<hr style='border:1px solid rgba(255,255,255,0.2);'>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
workout_model = pickle.load(open("workout_model.pkl","rb"))
diet_model = pickle.load(open("diet_model.pkl","rb"))

le_gender = pickle.load(open("le_gender.pkl","rb"))
le_activity = pickle.load(open("le_activity.pkl","rb"))
le_goal = pickle.load(open("le_goal.pkl","rb"))
le_food = pickle.load(open("le_food.pkl","rb"))
le_budget = pickle.load(open("le_budget.pkl","rb"))
le_workout = pickle.load(open("le_workout.pkl","rb"))
le_diet = pickle.load(open("le_diet.pkl","rb"))

# ---------------- DIET SUGGESTIONS ----------------
diet_suggestions = {
    "Balanced Diet": ["🥚 Eggs", "🍚 Rice + Dal", "🥗 Veg Curry", "🍎 Fruits", "🥛 Milk"],
    "Weight Loss Diet": ["🥗 Salad", "🍲 Veg Soup", "🥒 Cucumber", "🍎 Apple", "🥛 Buttermilk"],
    "Muscle Gain Diet": ["🍗 Chicken Breast", "🥚 Eggs", "🥜 Groundnuts", "🥛 Milk", "🍌 Banana"]
}

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 10, 80)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
    activity = st.selectbox("Activity Level", le_activity.classes_)
    food_pref = st.selectbox("Food Preference", le_food.classes_)

with col2:
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=200.0)
    gender = st.selectbox("Gender", le_gender.classes_)
    goal = st.selectbox("Goal", le_goal.classes_)
    budget = st.selectbox("Budget", le_budget.classes_)

# ---------------- BUTTON ----------------
if st.button("🚀 Generate My Fitness Plan"):

    # BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    st.markdown("## 📊 Health Summary")
    st.markdown(f"<h3 style='color:#00f5ff;'>BMI: {bmi:.2f}</h3>", unsafe_allow_html=True)

    bmi_score = min(int(bmi * 4), 100)
    st.progress(bmi_score)

    if bmi < 18.5:
        st.warning("⚠ Underweight")
    elif 18.5 <= bmi < 24.9:
        st.success("🟢 Normal Weight")
    elif 25 <= bmi < 29.9:
        st.warning("🟠 Overweight")
    else:
        st.error("🔴 Obese")

    # Model Prediction
    input_data = np.array([[age,
                            le_gender.transform([gender])[0],
                            height,
                            weight,
                            le_activity.transform([activity])[0],
                            le_goal.transform([goal])[0],
                            le_food.transform([food_pref])[0],
                            le_budget.transform([budget])[0]]])

    workout_pred = workout_model.predict(input_data)[0]
    diet_pred = diet_model.predict(input_data)[0]

    workout_result = le_workout.inverse_transform([workout_pred])[0]
    diet_result = le_diet.inverse_transform([diet_pred])[0]

    st.markdown("## 🎯 Your Personalized Plan")

    # Workout Card
    st.markdown(f"""
    <div style="
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    padding:20px;
    border-radius:20px;
    color:white;">
    <h3>🏋 Workout Plan</h3>
    <p style='font-size:18px;'>{workout_result}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Diet Foods
    foods = diet_suggestions.get(diet_result, ["🍎 Fruits", "🥗 Vegetables", "🥛 Milk"])

    if food_pref == "Non-Veg":
        foods.append("🍗 Chicken Curry (2-3 times/week)")

    food_items = ""
    for item in foods:
        food_items += f"<li>{item}</li>"

    # Diet Card
    st.markdown(f"""
    <div style="
    background: linear-gradient(45deg, #ff512f, #dd2476);
    padding:20px;
    border-radius:20px;
    color:white;">
    <h3>🥗 Diet Plan</h3>
    <p style='font-size:18px;'><b>{diet_result}</b></p>
    <ul>
    {food_items}
    </ul>
    </div>
    """, unsafe_allow_html=True)