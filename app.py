from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()

    conn.close()
    return render_template("index.html", users=users)

@app.route("/user/<int:user_id>")
def user_detail(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return render_template("user_detail.html", user=user)

@app.route("/api/users", methods=["GET"])  # Add this route decorator
def api_get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()

    conn.close()
    return jsonify(users)

@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        website = request.form["website"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (name, username, email, phone, website)
            VALUES (?, ?, ?, ?, ?)
        """, (name, username, email, phone, website))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("create_user.html")

@app.route("/update/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        website = request.form["website"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users 
            SET name=?, username=?, email=?, phone=?, website=?
            WHERE id=?
        """, (name, username, email, phone, website, user_id))

        conn.commit()
        conn.close()

        return redirect(url_for("user_detail", user_id=user_id))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()
    return render_template("update_user.html", user=user)

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
