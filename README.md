 Admin AI Chatbot

This project is a simple proof-of-concept application built using Flask and the Hugging Face Transformers library. My goal was to demonstrate how a simple command-line chatbot could be used for basic administrative tasks, specifically managing a local user database using natural language commands.

 Project Highlights

Technology Stack: Built with Python (Flask) and utilizes the transformers library for the AI component.

Intent Classification: I implemented a basic intent classification system (simulated using keyword detection combined with the transformers pipeline structure) to categorize user input into three core actions: add_user, delete_user, and update_user.

Data Management (CRUD): The chatbot allows administrators to perform simple Create, Read, Update, and Delete operations on user records.

Simple Persistence: User data is stored locally in a user_data.json file to maintain state between sessions.

UI/UX: I created a straightforward, split-screen web interface that displays the chat log on one side and the live database table on the other for immediate feedback on commands.

Access Control: The system includes a simple auto-login feature requiring a specific admin email (wpbrigade@company.com).

 Getting Started

Prerequisites

To run my project locally, I need Python 3 and the following dependencies. I can install them using pip:

pip install flask transformers torch


File Structure

The project follows a standard Flask structure to ensure maintainability:

AI_Chatbot_Project/
|-- app.py              # Main Flask server, AI logic, and database handlers
|-- user_data.json      # Simple JSON database file (must start with [])
|-- templates/
    |-- index.html      # The frontend UI (chat interface and data table)


Initialization

I must ensure the database file is initialized correctly before the first run:

Create the file user_data.json.

It must contain only a valid empty JSON array:

[]


 How to Run the Application

Navigate to the project directory in my terminal.

Start the Flask Server:

python app.py


Open in Browser: I access the application at the address provided by Flask (usually $\text{http://127.0.0.1:5000/}$).

Log In: I enter the admin email: wpbrigade@company.com.

💬 Example Commands

Here are some examples of the natural language commands I can use in the chat interface:

Action

Example Command

Create/Add

can you add the user "jane.doe@corp.com" with phone number "+923331234567"

Delete/Remove

please remove the user "jane.doe@corp.com" from the system

Update/Change

update john.smith@xyz.com city to Karachi

 Notes and Limitations

I designed the AI logic to be simple and beginner-friendly, focusing on demonstrating the pipeline structure rather than complex NLP.

Simplified AI: The intent classification is primarily driven by keyword matching (add, remove, update). It is robust enough for the specified command structure but would require fine-tuning for complex or ambiguous sentences.

Non-Production Database: The user_data.json file is purely for demonstration purposes and should not be used in any production environment due to limitations in concurrency and security.
