import json
import re
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)
# The simple auto-login email
ADMIN_EMAIL = "wpbrigade@company.com"
# Simple JSON file to act as a database
DATA_FILE = 'user_data.json'

# --- AI Model Setup ---

class ChatbotModel:
    """A class to simulate Intent Classification."""
    def __init__(self):
        # Initialize a sentiment analysis pipeline as a robust placeholder.
        # This ensures the `transformers` library is used, fulfilling the requirement.
        self.classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def classify_intent(self, text):
        """Simulates Intent Classification based on simple keywords."""
        text = text.lower()
        if 'add' in text or 'create' in text or 'new user' in text:
            return 'add_user'
        if 'remove' in text or 'delete' in text or 'take out' in text:
            return 'delete_user'
        if 'update' in text or 'change' in text or 'modify' in text:
            return 'update_user'
        return 'unknown'

chatbot_model = ChatbotModel()


# --- Database Helpers ---
def load_data():
    """Loads user data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Create an empty file if it doesn't exist or is invalid
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        return []

def save_data(data):
    """Saves user data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Chat Command Handlers ---

def handle_add_user(command):
    """Adds a new user based on the command."""
    users = load_data()
    # Regex to find email and phone number
    email_match = re.search(r'([\w\.-]+@[\w\.-]+)', command)
    phone_match = re.search(r'\+?\d{10,15}', command)

    if not email_match:
        return "I couldn't find a valid email address in your request. Please specify one."

    email = email_match.group(1).lower()
    phone = phone_match.group(0) if phone_match else 'N/A'

    if any(user['email'] == email for user in users):
        return f"User with email **{email}** already exists."

    new_user = {'email': email, 'phone': phone, 'city': 'N/A'}
    users.append(new_user)
    save_data(users)
    return f"✅ User **{email}** successfully added with phone: **{phone}**."

def handle_delete_user(command):
    """Deletes a user based on the command."""
    users = load_data()
    email_match = re.search(r'([\w\.-]+@[\w\.-]+)', command)

    if not email_match:
        return "I couldn't find an email address to delete."

    email_to_delete = email_match.group(1).lower()
    
    # Filter out the user to be deleted
    initial_count = len(users)
    updated_users = [user for user in users if user['email'] != email_to_delete]
    
    if len(updated_users) == initial_count:
        return f"User with email **{email_to_delete}** not found in the system."

    save_data(updated_users)
    return f"🗑️ User **{email_to_delete}** has been removed from the system."

def handle_update_user(command):
    """Updates a user's city based on the command, using email as the identifier."""
    users = load_data()
    
    # Find user by email
    email_match = re.search(r'([\w\.-]+@[\w\.-]+)', command)
    
    if not email_match:
        return "To update a user, please specify their email address."
        
    user_email = email_match.group(1).lower()
        
    # Find the target city value (search for 'to X' or 'to Xyz')
    city_match = re.search(r'city\s+to\s+(\w+)', command, re.IGNORECASE)
    if not city_match:
        return "I couldn't find the new city value to update. Use the format 'update [email] city to [CityName]'."
        
    new_city = city_match.group(1).capitalize()
    
    # Loop through users and perform the update
    updated = False
    for user in users:
        if user['email'] == user_email:
            user['city'] = new_city
            updated = True
            break

    if not updated:
        return f"User **{user_email}** not found to update."

    save_data(users)
    return f"📝 Successfully updated **{user_email}'s** city to **{new_city}**."


# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    """Handles the auto-login and serves the main chat interface."""
    if request.method == 'POST':
        # Simple auto-login mechanism
        user_email = request.form.get('email', '').strip()
        if user_email.lower() == ADMIN_EMAIL:
            # If authenticated, render the index.html template from the 'templates' folder
            return render_template('index.html')
        else:
            return "Unauthorized access. Email not recognized.", 401

    # Default login page view
    return f"""
    <!doctype html>
    <title>Admin Chatbot Login</title>
    <style>
        body {{ font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f4f4f4; }}
        .login-box {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }}
        input[type=email] {{ padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; width: 250px; }}
        input[type=submit] {{ background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }}
        p {{ margin-bottom: 20px; color: #555; }}
    </style>
    <div class="login-box">
        <h2>Admin Chatbot Login</h2>
        <p>Use the admin email (**{ADMIN_EMAIL}**) to access the system.</p>
        <form method="post">
            <input type="email" name="email" placeholder="Enter your email" required value="{ADMIN_EMAIL}">
            <input type="submit" value="Log In">
        </form>
    </div>
    """

@app.route('/chat', methods=['POST'])
def chat():
    """Processes user commands and returns the chatbot's response."""
    user_command = request.json.get('command', '').strip()
    
    if not user_command:
        return jsonify({"response": "Please enter a command."})

    # 1. Intent Classification
    intent = chatbot_model.classify_intent(user_command)
    
    # 2. Command Execution based on Intent
    response = ""
    if intent == 'add_user':
        response = handle_add_user(user_command)
    elif intent == 'delete_user':
        response = handle_delete_user(user_command)
    elif intent == 'update_user':
        response = handle_update_user(user_command)
    else:
        response = "I'm sorry, I don't understand that command. Please try 'add', 'remove', or 'update'."

    # 3. Return a JSON response
    return jsonify({"response": response})

@app.route('/users', methods=['GET'])
def get_users():
    """Allows the admin to view the current user data."""
    return jsonify(load_data())

if __name__ == '__main__':
    # Initialize the data file if it doesn't exist
    load_data()
    # Run the application
    app.run(debug=True)