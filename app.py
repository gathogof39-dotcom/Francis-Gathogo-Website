from flask import Flask, abort, request, send_from_directory, jsonify
import json
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(app.root_path, "index.html")


@app.route("/<path:filename>")
def site_asset(filename):
    if filename not in {
        "style.css",
        "script.js",
        "francis-profile.png"
         "googlea35038a42fae92d3.html"
    }:
        abort(404)
    return send_from_directory(app.root_path, filename)


def send_email_notification(name, email, subject, message):
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASS")

    if not sender or not password:
        print("Email not configured, skipping notification.")
        return

    msg = EmailMessage()
    msg["Subject"] = f"New website message: {subject or 'No subject'}"
    msg["From"] = sender
    msg["To"] = sender
    msg["Reply-To"] = email
    msg.set_content(f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


@app.route("/contact", methods=["POST"])
def contact():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    subject = (request.form.get("subject") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(success=False, error="Please fill in name, email and message."), 400

    if "@" not in email or "." not in email:
        return jsonify(success=False, error="Please enter a valid email address."), 400

    entry = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    }

    with open("messages.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"New message from {name} <{email}>")

    try:
        send_email_notification(name, email, subject, message)
    except Exception as e:
        print("Email failed:", e)

    return jsonify(success=True, message="Thank you! Your message has been sent.")


if __name__ == "__main__":
    app.run(debug=False)