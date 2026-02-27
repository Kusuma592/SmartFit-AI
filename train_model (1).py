import pandas as pd

data = pd.read_csv("fitness_data.csv")
print(data.columns)
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("fitness_data.csv")

# Create encoders
le_gender = LabelEncoder()
le_activity = LabelEncoder()
le_goal = LabelEncoder()
le_food = LabelEncoder()
le_budget = LabelEncoder()
le_workout = LabelEncoder()
le_diet = LabelEncoder()

# Encode input columns
data["Gender"] = le_gender.fit_transform(data["Gender"])
data["Activity"] = le_activity.fit_transform(data["Activity"])
data["Goal"] = le_goal.fit_transform(data["Goal"])
data["Food"] = le_food.fit_transform(data["Food"])
data["Budget"] = le_budget.fit_transform(data["Budget"])

# Encode outputs
data["Workout Plan"] = le_workout.fit_transform(data["Workout Plan"])
data["Diet Plan"] = le_diet.fit_transform(data["Diet Plan"])

# Features
X = data[["Age","Gender","Height","Weight","Activity","Goal","Food","Budget"]]
y_workout = data["Workout Plan"]
y_diet = data["Diet Plan"]

# Train models
workout_model = RandomForestClassifier()
diet_model = RandomForestClassifier()

workout_model.fit(X, y_workout)
diet_model.fit(X, y_diet)

# Save models
pickle.dump(workout_model, open("workout_model.pkl","wb"))
pickle.dump(diet_model, open("diet_model.pkl","wb"))

# Save encoders
pickle.dump(le_gender, open("le_gender.pkl","wb"))
pickle.dump(le_activity, open("le_activity.pkl","wb"))
pickle.dump(le_goal, open("le_goal.pkl","wb"))
pickle.dump(le_food, open("le_food.pkl","wb"))
pickle.dump(le_budget, open("le_budget.pkl","wb"))
pickle.dump(le_workout, open("le_workout.pkl","wb"))
pickle.dump(le_diet, open("le_diet.pkl","wb"))

print("✅ Training completed & models saved!")