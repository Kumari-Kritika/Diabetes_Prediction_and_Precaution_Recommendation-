#connection
'''from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')

    resp = MessagingResponse()
    msg = resp.message()

    # Simple reply
    msg.body("Hi")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)'''























#///////////////////////////////////////////////////////workable code/////////////////////
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Temporary memory (simple version)
user_data = {}

def show_menu():
    return """📋 *Main Menu*

1️⃣ Check Diabetes Risk  
2️⃣ Diet Plan  
3️⃣ Exercise Routine  
4️⃣ Precautions  
5️⃣ Exit  

Reply with number (1/2/3/4/5) 😊"""


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body').strip().lower()
    sender = request.form.get('From')

    resp = MessagingResponse()
    msg = resp.message()

    # Initialize user state
    if sender not in user_data:
        user_data[sender] = {"step": None}

    state = user_data[sender]

    # Greeting
    if incoming_msg in ["hi", "hello"]:
        state["step"] = None
        msg.body("""👋 *Welcome to KritikaMedi AI*

Hello! I’m your Diabetes Risk Assessment Assistant.

I’ll ask you a few quick questions about your health to estimate your diabetes risk.

This is based on medically validated factors used in research (WHO / ADA).

👉 Type *menu* to begin 😊""")

    # Menu
    elif incoming_msg == "menu":
        state["step"] = None
        msg.body(show_menu())

    # Option 1: Start questions
    elif incoming_msg == "1":
        state["step"] = "age"
        msg.body("🔢 What is your age? (e.g., 30)")

    # Collect Age
    elif state["step"] == "age":
        state["age"] = float(incoming_msg)
        state["step"] = "glucose"
        msg.body("🩸 Enter your Glucose level (e.g., 120)")

    # Collect Glucose
    elif state["step"] == "glucose":
        state["glucose"] = float(incoming_msg)
        state["step"] = "bmi"
        msg.body("⚖️ What is your BMI? (e.g., 28)")

    # Collect BMI + Calculate
    elif state["step"] == "bmi":
        state["bmi"] = float(incoming_msg)

        age = state["age"]
        glucose = state["glucose"]
        bmi = state["bmi"]

        # Hidden formula (not shown unless needed)
        score = (glucose * 0.03) + (bmi * 0.02) + (age * 0.01)

        if score > 5:
            result = "high"
        else:
            result = "low"

        response = f"Your Score = {round(score,2)}\n\n"

        if result == "high":
            response += "⚠️ High score → Diabetes"
        else:
            response += "✅ Low score → No Diabetes"

        response += "\n\nType *menu* to continue 😊"

        state["step"] = None
        msg.body(response)

    # Option 2
    elif incoming_msg == "2":
        msg.body("""🥗 *Diet Plan*

✔️ Eat green vegetables  
✔️ Avoid sugar & junk food  
✔️ Include whole grains  
✔️ Drink plenty of water  

Type *menu* to go back""")

    # Option 3
    elif incoming_msg == "3":
        msg.body("""🏃 *Exercise Routine*

✔️ 30 min walking  
✔️ Yoga or stretching  
✔️ Light exercise  

Type *menu* to go back""")

    # Option 4
    elif incoming_msg == "4":
        msg.body("""🩺 *Precautions*

✔️ Monitor blood sugar  
✔️ Maintain healthy weight  
✔️ Regular checkups  
✔️ Stay hydrated  

Type *menu* to go back""")

    # Exit
    elif incoming_msg == "5" or "exit" in incoming_msg:
        msg.body("""🙏 Thank You for using KritikaMedi AI

Stay healthy 😊""")

    # Default fallback
    else:
        msg.body("❗ Please type *menu* to continue 😊")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)













































































