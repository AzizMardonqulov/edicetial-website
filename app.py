from flask import Flask , render_template , redirect ,jsonify , request , session , flash 
import os
import sqlite3
app = Flask(__name__)
app.secret_key = "this_is_secret_key"
def get_db_connection():
    conn = sqlite3.connect("test.db")
    conn.row_factory = sqlite3.Row  
    return conn
conn = sqlite3.connect("test.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS test (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quasion TEXT NOT NULL,
    obsion  text ,
    addvers text
)
''')
sample_data = [
    ("What is the capital of France?", "A. London , B. Paris , C. Rome , D. Madrid", "B. Paris"),
    ("Choose the correct sentence:", "A. He go to school , B. He goes to school , C. He going to school , D. He gone to school.", "B. He goes to school"),
    ("Which word is a synonym of (happy)?", "A. Sad , B. Angry , C. Joyful , D. Tired.", "C. Joyful"),
    ("What is the past tense of (eat)?", "A. Eated , B. Ate, C. Eats, D. Eating,", "B. Ate"),
    ("What is the correct form of the sentence?", "A. I have never saw this movie , B. I have never seen this movie., C. I has never seen this movie. , D. I never seen this movie.", "B. I have never seen this movie"),
    ("What does (It's a piece of cake) mean?", "A. It is delicious , B. It is very easy , C. It is expensive , D. It is confusing.", "B. It is very easy"),
    (" Which sentence is grammatically correct?", "A. She don’t like coffee , B. She doesn’t like coffee , C. She not like coffee , D. She didn’t likes coffee.", "B. She doesn’t like coffee"),
    ("What is the opposite of (increase)?", "A. Grow , B. Expand , C. Decrease , D. Improve.", "C. Decrease"),
    ("Which sentence is in the passive voice?", "A. She wrote a letterv , B. A letter was written by her , C. She is writing a letter , D. She writes a letter.", "B. A letter was written by her"),
    ("What is the correct conditional sentence?", "A. If I will have time, I call you , B. If I had time, I would call you , C. If I has time, I will call you , D. If I had time, I call you.", "B. If I had time, I would call you"),
    ("Choose the correct reported speech form:", "A. She said, (I am tired.) → She said that she was tired , B. She said, (I am tired.) → She said that she is tired , C. She said, (I am tired.) → She said that she will be tired , D. She said, (I am tired.) → She said that she be tired.", "A. She said that she was tired"),
    ("Identify the correct phrasal verb:", "A. She looked after her little brother , B. She looked for her little brother , C. She looked in her little brother , D. She looked with her little brother.", " A. She looked after her little brother"),
    ("What does (jump on the bandwagon) mean?", "A. To start doing something because it is popular , B. To travel by train , C. To avoid responsibilities , D. To criticize someone.", "A. To start doing something because it is popular"),
    ("Choose the correct sentence using inversion:", "A. Never I have seen such a beautiful view , B. Never have I seen such a beautiful view , C. Never I seen have such a beautiful view , D. Never I seen have such beautiful a view.", "B. Never have I seen such a beautiful view"),
    ("Which sentence contains a relative clause?", "A. The book that I borrowed was interesting , B. I read the book fast , C. That book is interesting , D. The book was on the table.", "A. The book that I borrowed was interesting"),
    ("What does (give someone the benefit of the doubt) mean?", "A. To doubt someone completely , B. To trust someone even if unsure , C. To punish someone , D. To ignore someone.", "B. To trust someone even if unsure"),
    ("Identify the correct sentence using a cleft structure:", "A. It was my friend who helped me , B. It was helped my friend me , C. My friend was it who helped me , D. It my friend helped was me.", "A. It was my friend who helped me"),
    ("Choose the correct usage of a subjunctive mood:", "A. I wish he were here , B. I wish he was here , C. I wish he is here , D. I wish he be here.", "A. I wish he were here"),
    ("Identify the sentence with correct parallel structure:", "A. She enjoys reading, cooking, and to dance , B. She enjoys reading, cooking, and dancing , C. She enjoys reading, to cook, and dancing , D. She enjoys to read, cooking, and dancing.", "B. She enjoys reading, cooking, and dancing"),
    ("What does (walk on eggshells) mean?", "A. To be extremely careful , B. To be very clumsy , C. To be very confident , D. To be extremely happy.", "A. To be extremely careful"),
    ("What is the capital of France?", "A. London , B. Paris , C. Rome , D. Madrid", "B. Paris"),
]
#cursor.executemany("INSERT INTO test (quasion, obsion, addvers) VALUES (?, ?, ?)", sample_data)

@app.route('/')
def index():
    userr = session.get("user_id", "Log In")
    if "user_id" in session:
        return render_template("index.html", log=userr)
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        flash("Siz allaqachon logindan o'tgansiz")
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")

    foydalanuvchilar = request.form.get("email")
    password = request.form.get("password")

    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM foydalanuvchilar WHERE foydalanuvchi_nomi = ? AND parol = ?",
        (foydalanuvchilar, password),
    )
    row = cursor.fetchone()
    con.close()

    if row:
        session["user_id"] = foydalanuvchilar
        return redirect("/")
    else:
        flash("No'to'gri foydalanuvchi nomi yoki parol")
        return render_template("unfound.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    foydalanuvchi_nomi = request.form.get("email")
    parol = request.form.get("password")

    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO foydalanuvchilar (foydalanuvchi_nomi, parol) VALUES (?, ?)",
        (foydalanuvchi_nomi, parol),
    )
    con.commit()
    con.close()

    return redirect("/")


@app.route("/log-out")
def logout():
    session.pop("user_id", None)
    flash("Siz tizimdan chiqdingiz")
    return redirect("/")



@app.route("/test")
def test():
   return render_template("test.html" )

@app.route("/test/eilts", methods=["GET", "POST"])
def eilts():
    conn = get_db_connection() 
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM test")
    # quasion = cursor.fetchall()
    # conn.close()  
    # Ma'lumotlarni faqat bir marta qo‘shish uchun tekshiramiz
    cursor.execute("SELECT * FROM test")
    quasion = cursor.fetchall()

    if quasion == 0:  # Agar bo‘sh bo‘lsa, qo‘shamiz
        cursor.executemany("INSERT INTO test (quasion, obsion, addvers) VALUES (?, ?, ?)", sample_data)
        conn.commit()

    conn.close()  # Ulanishni yopamiz
    return render_template("eilts.html", quasion=quasion)

@app.route("/test/result/page" , methods=["GET", "POST"])
def get_result():
    scrore = request.form.get("Result")
    if scrore is None:
        return "Error: No result provided", 400  
    resultNum = int(scrore) * 7

    text =""
    return render_template("result.html" , result = scrore , test = test)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)