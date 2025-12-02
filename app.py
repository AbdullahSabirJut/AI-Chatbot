import json
import re
from pathlib import Path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

ADMIN_EMAIL = "wpbrigade@company.com"
DATA_FILE = Path("user_data.json")


# ---------- Simple intent classifier (keyword rules) ----------
def classify_intent(text: str) -> str:
    t = (text or "").lower()
    if any(k in t for k in ("add", "create", "new user", "add the user")):
        return "add_user"
    if any(k in t for k in ("remove", "delete", "take out")):
        return "delete_user"
    if any(k in t for k in ("update", "change", "modify")):
        return "update_user"
    return "unknown"


# ---------- Data persistence ----------
def load_data():
    """Return a normalized list of users from the JSON file."""
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []
    out = []
    for u in data:
        out.append({
            "name": u.get("name", "N/A"),
            "email": (u.get("email") or "").lower(),
            "phone": u.get("phone", "N/A"),
            "city": u.get("city", "N/A"),
        })
    return out


def save_data(users):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


# ---------- Utilities ----------
def safe_name_from_email(email: str) -> str:
    """Convert local-part of email to a readable name: john.smith -> John Smith"""
    local = (email or "").split("@")[0]
    local = re.sub(r"[._\-]+", " ", local)         # replace separators with space
    local = re.sub(r"\d+", "", local).strip()      # drop digits
    parts = [p.capitalize() for p in local.split() if p]
    return " ".join(parts) if parts else "N/A"


def normalize_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def find_by_email(users, email):
    key = (email or "").lower()
    for u in users:
        if u.get("email", "") == key:
            return u
    return None


def find_by_normalized_name(users, name_token):
    norm = normalize_key(name_token)
    for u in users:
        if normalize_key(u.get("name", "")) == norm or normalize_key(u.get("email", "")) == norm:
            return u
    return None


# ---------- Command handlers ----------
def handle_add_user(command: str) -> str:
    users = load_data()

    # quoted name if present (prefer quoted name)
    quoted = re.search(r'["\']\s*([A-Za-z0-9 .\'\-]+?)\s*["\']', command)
    quoted_name = None
    if quoted:
        candidate = quoted.group(1).strip()
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', candidate):  # ignore quoted emails
            quoted_name = candidate

    # email (require it)
    email_m = re.search(r'([\w\.-]+@[\w\.-]+\.[A-Za-z]{2,})', command)
    if not email_m:
        return "I couldn't find a valid email address in your request. Please provide an email like john@example.com."
    email = email_m.group(1).lower()

    # phone (optional) - accept + and 3-15 digits
    phone_m = re.search(r'(\+?\d{3,15})', command)
    phone = phone_m.group(1) if phone_m else "N/A"

    # choose name: quoted overrides; otherwise derive from email
    name = quoted_name if quoted_name else safe_name_from_email(email)

    # duplicate check
    if any(u["email"] == email for u in users):
        return f"User with email **{email}** already exists."

    users.append({"name": name, "email": email, "phone": phone, "city": "N/A"})
    save_data(users)
    return f"✅ User **{name}** <{email}> successfully added with phone: **{phone}**."


def handle_delete_user(command: str) -> str:
    users = load_data()

    # 1) by email
    email_m = re.search(r'([\w\.-]+@[\w\.-]+\.[A-Za-z]{2,})', command)
    if email_m:
        key = email_m.group(1).lower()
        new = [u for u in users if u["email"] != key]
        if len(new) == len(users):
            return f"User with email **{key}** not found."
        save_data(new)
        return f"🗑️ User **{key}** removed."

    # 2) by quoted name
    quoted = re.search(r'["\']\s*([A-Za-z0-9 .\'\-]+?)\s*["\']', command)
    if quoted:
        name_key = quoted.group(1).strip().lower()
        new = [u for u in users if u["name"].lower() != name_key]
        if len(new) == len(users):
            return f"User named **{quoted.group(1).strip()}** not found."
        save_data(new)
        return f"🗑️ User **{quoted.group(1).strip()}** removed."

    # 3) fallback: patterns like "delete John Smith" or "remove samanthas"
    fallback = re.search(r'(?:remove|delete)\s+(?:the\s+)?(?:user\s+)?([A-Za-z0-9\.\' \-]{1,60})(?:\s+with|\s+email|\s+phone|$)', command, re.IGNORECASE)
    if fallback:
        candidate = fallback.group(1).strip().lower()
        # handle simple possessive forms ("samanthas" -> "samantha")
        candidate = re.sub(r"'s$", "", candidate)
        if " " not in candidate and candidate.endswith("s"):
            candidate = candidate[:-1]
        norm = normalize_key(candidate)
        new = [u for u in users if normalize_key(u["name"]) != norm and normalize_key(u["email"]) != norm]
        if len(new) == len(users):
            return f"User **{fallback.group(1).strip()}** not found."
        save_data(new)
        return f"🗑️ User **{fallback.group(1).strip()}** removed."

    return "I couldn't find which user to delete. Please specify an email or a quoted name."


def handle_update_user(command: str) -> str:
    users = load_data()

    # find new city (multi-word allowed)
    city_m = re.search(r'city\s+to\s+([A-Za-z0-9 \-]+)', command, re.IGNORECASE)
    if not city_m:
        return "I couldn't find the new city. Use format: 'update [email|name] city to [CityName]'."
    new_city = city_m.group(1).strip()

    # 1) prefer email if present
    email_m = re.search(r'([\w\.-]+@[\w\.-]+\.[A-Za-z]{2,})', command)
    if email_m:
        email = email_m.group(1).lower()
        target = find_by_email(users, email)
        if not target:
            return f"User with email **{email}** not found."
        target["city"] = new_city
        save_data(users)
        return f"📝 Successfully updated **{email}** city to **{new_city}**."

    # 2) quoted name
    quoted = re.search(r'["\']\s*([A-Za-z0-9 .\'\-]+?)\s*["\']', command)
    candidate = quoted.group(1).strip().lower() if quoted else None

    # 3) name before word 'city' (e.g., "update samanthas city to Cordoba")
    if not candidate:
        m = re.search(r'update\s+([A-Za-z0-9\.\' \-]{1,60}?)\s+city', command, re.IGNORECASE)
        if m:
            candidate = m.group(1).strip().lower()

    if not candidate:
        return "Please specify which user to update (email or name)."

    candidate = re.sub(r"'s$", "", candidate)
    if " " not in candidate and candidate.endswith("s"):
        candidate = candidate[:-1]
    target = find_by_normalized_name(users, candidate)
    if not target:
        return f"User **{candidate}** not found."
    target["city"] = new_city
    save_data(users)
    return f"📝 Successfully updated **{candidate}**'s city to **{new_city}**."


# ---------- Routes (unchanged interface) ----------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_email = (request.form.get("email") or "").strip().lower()
        if not user_email:
            return "Please provide an email.", 400
        users = load_data()
        if user_email == ADMIN_EMAIL or any(u["email"] == user_email for u in users):
            return render_template("index.html")
        return "Unauthorized access. Email not recognized in the system.", 401

    return f"""
    <!doctype html>
    <title>Admin Chatbot Login</title>
    <style>
        body {{ font-family: sans-serif; display:flex; align-items:center; justify-content:center; height:100vh; background:#f4f4f4; }}
        .box {{ background:white; padding:30px; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.1); text-align:center; }}
        input[type=email]{{padding:8px 10px; width:260px;}}
        input[type=submit]{{padding:8px 12px; background:#007bff;color:white;border:none;border-radius:4px;}}
    </style>
    <div class="box">
        <h2>Admin Chatbot Login</h2>
        <p>Use admin email <strong>{ADMIN_EMAIL}</strong> or any email present in the system.</p>
        <form method="post">
            <input type="email" name="email" placeholder="Enter your email" required />
            <br/><br/>
            <input type="submit" value="Log In" />
        </form>
    </div>
    """


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(force=True, silent=True) or {}
    cmd = (payload.get("command") or "").strip()
    if not cmd:
        return jsonify({"response": "Please enter a command."})

    intent = classify_intent(cmd)
    if intent == "add_user":
        res = handle_add_user(cmd)
    elif intent == "delete_user":
        res = handle_delete_user(cmd)
    elif intent == "update_user":
        res = handle_update_user(cmd)
    else:
        res = "I'm sorry, I don't understand that command. Try: add, remove, or update."

    return jsonify({"response": res})


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(load_data())


if __name__ == "__main__":
    load_data()  # ensure file exists
    app.run(debug=True, host="0.0.0.0", port=5000)

