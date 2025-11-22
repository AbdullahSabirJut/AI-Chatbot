
# Admin AI Chatbot Project

A simple, command-line interface (CLI) driven administrative tool built with **Flask** and the Hugging Face **Transformers** library for basic intent classification. This project allows an admin to manage a simple user database using natural language commands.

##  Features

  * **Natural Language Commands:** Add, delete, and update user information using simple chat commands.
  * **Intent Classification:** Uses a small Hugging Face model (`distilbert`) to classify user input into `add_user`, `delete_user`, or `update_user` intents.
  * **Simple "Database":** User data is stored in a local `user_data.json` file.
  * **Auto-Login:** Simple access control using a predefined admin email (`wpbrigade@company.com`).
  * **Clean Architecture:** Uses standard Flask templating with separate files for logic (`app.py`) and interface (`index.html`).

-----

##  Project Setup

### 1\. Prerequisites

You must have **Python 3** installed. Then, install the required libraries:

```bash
pip install flask transformers torch
```

### 2\. File Structure

Ensure project directory is organized exactly as shown below:

```
AI_Chatbot_Project/
|-- app.py              # Main Flask application and AI logic
|-- user_data.json      # The simple database
|-- templates/
    |-- index.html      # The chat and data viewing interface
```

### 3\. Initialize Data File

The `user_data.json` file must exist and contain a valid empty JSON array:

```json
[]
```

-----

##  How to Run

1.  **Navigate** to the project's root directory in your terminal or command prompt.

    ```bash
    cd AI_Chatbot_Project
    ```

2.  **Start the Flask Server:**

    ```bash
    python app.py
    ```

3.  **Access the Application:** Open your web browser and navigate to:
    $$\text{[http://127.0.0.1:5000/](http://127.0.0.1:5000/)}$$

4.  **Log In:** Use the required admin email: `wpbrigade@company.com`

-----

##  Example Commands

Once logged into the chat interface, you can use the following commands:

| Action | Example Command | Notes |
| :--- | :--- | :--- |
| **Add User** | `can you add the user "alice.wonder@example.com" with phone number "+15551234567"` | Requires an email and a phone number (optional). |
| **Delete User** | `can you remove the user "john.smith@xyz.com"` | Requires the user's email address. |
| **Update User** | `can you update alice.wonder@example.com city to London` | Requires the user's email and the attribute to change. |

-----
