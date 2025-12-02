# Admin AI Chatbot (Natural Language User Management)

A lightweight, beginner-friendly **Flask-based command-line assistant** that allows admins to **manage a user database using natural language commands**.  
Instead of clicking forms or typing structured database queries, admins can interact with the system conversationally:

> “Add a new user named John Doe with email john@example.com and phone +923001234567.”

The chatbot intelligently understands commands, extracts user details using pattern matching, and updates a persistent JSON database.

This project is perfect for learning:  
✔ Natural-language interfaces  
✔ Simple intent recognition  
✔ Data extraction with regex  
✔ CRUD operations  
✔ Flask backend development  
✔ JSON-based persistence

* * *

## Key Features

-   **Natural Language Commands**  
    Add, update, or delete users using plain English instructions.
    
-   **Lightweight Intent Classifier**  
    A simple rule-based classifier determines the user’s intent (add/update/delete).
    
-   **Automatic Detail Extraction**  
    Uses regex to extract names, email addresses, phone numbers, and cities.
    
-   **JSON-Based Persistent Database**  
    Saves all user data in a `user_data.json` file.
    
-   **Admin Login System**  
    Only registered users or the admin email can access the chatbot interface.
    
-   **Clean Flask Backend**  
    No external ML models — fast, easy to understand, and deployable anywhere.
    
-   **Fully Functional API Endpoints**  
    Used by the front-end interface for interaction.
    

* * *

## Tech Stack

| Layer | Technologies Used |
| --- | --- |
| **Backend** | Flask, Python 3 |
| **Data Storage** | JSON file-based DB |
| **Natural Language Processing** | Custom rule-based intent classifier + Regex |
| **Frontend** | HTML template (Flask-rendered), CSS |
| **Runtime** | Works on any OS (Windows, macOS, Linux) |

* * *

## Project Folder Structure

project/
│
├── app.py                  # Main Flask application
├── user_data.json          # JSON-based user database
├── templates/
│   └── index.html          # Chat UI and command interface
├── static/                 # (Optional) CSS/JS assets
│
└── README.md               # Project documentation


* * *

##  Installation Guide (Beginner Friendly)

Follow these steps to run the project locally:

### **1\. Install Python**

Make sure Python 3.8+ is installed.

Check version:

`python --version`

### **2\. Clone the Repository**

`git clone (https://github.com/AbdullahSabirJut/AI-Chatbot)`

### **3\. Create a Virtual Environment (recommended)**

`python -m venv venv`

Activate:

-   Windows:
    
    `venv\Scripts\activate`
    
-   Mac/Linux:
    
    `source venv/bin/activate`
    

### **4\. Install Dependencies**

`pip install flask`

### **5\. Ensure the Database File Exists**

If not present, create an empty `user_data.json`:

`[]`

* * *

## How to Run the Project

Start the Flask server:

`python app.py`

You will see output similar to:

`Running on http://127.0.0.1:5000/`

Open this in your browser to access the login page.

* * *

## Usage Instructions

### **1\. Login**

You must enter:

-   Admin email: `wpbrigade@company.com`
    

### **2\. Enter Natural Language Commands**

Examples:

#### Add User

`Add a new user named "John Doe" with email john@example.com and phone +923001234567`

#### Delete User

`Delete the user with email john@example.com`

or

`Remove "John Doe"`

#### Update User

`Update john@example.com city to Karachi`

or

`Update "John Doe" city to Lahore`

### **3\. View All Users**

Visit:

`GET /users`

* * *

## Screenshots (Placeholders)


### **Login Page**
<img width="485" height="199" alt="image" src="https://github.com/user-attachments/assets/de4e2cc7-2a86-4be9-ba43-8df1d4770513" />


### **Chat Interface**
<img width="626" height="415" alt="image" src="https://github.com/user-attachments/assets/a26a7ab5-8d9c-4827-b688-c648dfc8236d" />


### **User Database**
<img width="290" height="152" alt="image" src="https://github.com/user-attachments/assets/aca1fed2-ec99-4190-ae30-62e069d532d2" />


* * *

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/chat` | Send a natural-language command to the chatbot |
| `GET` | `/users` | Fetch all users from the database |
| `GET`/`POST` | `/` | Login interface |

### Example `/chat` request:

`{   "command": "Add a user named 'Sarah Khan' with email sarah@example.com and phone +923341234567" }`

### Example response:

`{   "response": "✅ User Sarah Khan <sarah@example.com> successfully added with phone: +923341234567." }`

* * *

## How the Code Works (Internal Architecture)

### **1\. Intent Classification**

A simple keyword-based classifier:

-   If text contains `add`, `create` → intent: `add_user`
    
-   If text contains `delete`, `remove` → intent: `delete_user`
    
-   If text contains `update`, `change` → intent: `update_user`
    

### **2\. Information Extraction**

Regex patterns extract:

-   Email
    
-   Phone numbers
    
-   Quoted names
    
-   Cities
    
-   Fallback name patterns ("update John city…")
    

### **3\. CRUD Operations**

Each handler:

-   Loads users from `user_data.json`
    
-   Adds/updates/deletes data
    
-   Saves back to file
    

### **4\. Flask Endpoints**

-   `/` handles login and renders the UI.
    
-   `/chat` receives commands and returns JSON responses.
    
-   `/users` outputs the entire database.
    

### **5\. Frontend**

Simple HTML UI with an input box that sends commands to `/chat`.
