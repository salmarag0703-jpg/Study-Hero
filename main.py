import random
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "study-hero-final-pro"

# =========================
# LARGE QUESTION BANK
# =========================
bank = {
    "Easy": [
        ("What is HTML used for?", "structure"),
        ("What is CSS used for?", "style"),
        ("Python is a?", "programming language"),
        ("What does print do?", "display output"),
        ("What symbol for comments in Python?", "#"),
        ("What tag for image?", "img"),
        ("What tag for link?", "a"),
        ("Input is used for?", "taking input"),
        ("Variable stores?", "data"),
        ("True or False: Python is a language", "true"),
    ] * 2,
    "Medium": [
        ("What keyword for loop?", "for"),
        ("What keyword for condition?", "if"),
        ("== means?", "equal"),
        ("!= means?", "not equal"),
        ("What does break do?", "stop loop"),
        ("What does continue do?", "skip iteration"),
        ("List is?", "collection"),
        ("Dictionary stores?", "key value"),
        ("Tuple is?", "immutable list"),
        ("len() returns?", "length"),
    ] * 2,
    "Hard": [
        ("What is OOP?", "object oriented programming"),
        ("What is class?", "blueprint"),
        ("What is object?", "instance"),
        ("What is inheritance?", "reuse of code"),
        ("What is recursion?", "function calling itself"),
        ("What is debugging?", "fix errors"),
        ("What is algorithm?", "steps to solve problem"),
        ("What is function?", "block of code"),
        ("What is API?", "application interface"),
        ("What is loop?", "repetition"),
    ] * 2
}

good_msgs = ["🔥 Awesome!", "🚀 Great Job!", "💪 Perfect!", "🌟 Excellent!", "🏆 Genius!"]
bad_msgs = ["😅 Try again!", "📚 Not yet!", "💪 Keep going!", "🔥 Don't give up!"]

# =========================
# HOME
# =========================
@app.route("/", methods=["GET", "POST"])
def home():
    if "exam" not in session:
        if request.method == "POST":
            level = request.form["level"]
            if level == "1":
                levels = ["Easy"]
            elif level == "2":
                levels = ["Medium"]
            elif level == "3":
                levels = ["Hard"]
            else:
                levels = ["Easy", "Medium", "Hard"]
            
            exam = []
            for l in levels:
                for q, a in bank[l]:
                    exam.append({"q": q, "a": a})
            random.shuffle(exam)
            session["exam"] = exam
            session["i"] = 0
            session["score"] = 0
            session["lives"] = 3
            session["wrong"] = []
            session["msg"] = ""
            session["correct"] = ""
        else:
            return render_template_string("""
                <h1>🎮 STUDY HERO FINAL</h1>
                <h3>Choose Level</h3>
                <form method="POST">
                    <button name="level" value="1">Easy</button>
                    <button name="level" value="2">Medium</button>
                    <button name="level" value="3">Hard</button>
                    <button name="level" value="4">Mixed</button>
                </form>
            """)

    exam = session["exam"]
    i = session["i"]
    
    if session["lives"] <= 0 or i >= len(exam):
        return render_template_string("""
            <h1>🏆 GAME OVER</h1>
            <p>⭐ Score: {{score}}</p>
            <h3>📚 Mistakes Review</h3>
            {% for m in wrong %}
                <p>❌ {{m[0]}} <br> ✔ {{m[1]}}</p>
            {% endfor %}
            <a href="/reset">🔄 Play Again</a>
        """, score=session["score"], wrong=session["wrong"])

    q = exam[i]
    hearts = "❤️" * session["lives"] + "🖤" * (3 - session["lives"])
    return render_template_string("""
        <h2>🎮 STUDY HERO FINAL</h2>
        <p>Lives: {{hearts}} | Score: {{score}}</p>
        <h3>Q{{i+1}}: {{q['q']}}</h3>
        {% if msg %}
            <p><b>{{msg}}</b></p>
        {% endif %}
        {% if correct %}
            <p style="color:green;"><b>✔ Correct Answer: {{correct}}</b></p>
        {% endif %}
        <form method="POST" action="/answer">
            <input name="answer" placeholder="Type answer..." required>
            <button>Submit</button>
        </form>
    """, q=q, i=i, hearts=hearts, score=session["score"], msg=session["msg"], correct=session["correct"])

# =========================
# ANSWER CHECK
# =========================
@app.route("/answer", methods=["POST"])
def answer():
    user = request.form["answer"].lower()
    exam = session["exam"]
    i = session["i"]
    correct = exam[i]["a"]
    if user in correct.lower() or correct.lower() in user:
        session["score"] += 10
        session["msg"] = random.choice(good_msgs)
        session["correct"] = ""
    else:
        session["lives"] -= 1
        session["msg"] = random.choice(bad_msgs)
        session["correct"] = correct
        session["wrong"].append((exam[i]["q"], correct))
    session["i"] += 1
    return redirect(url_for("home"))

# =========================
# RESET
# =========================
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
