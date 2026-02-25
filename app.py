from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ujjawal@@",
        database="portfolio_db"
    )
    cursor = db.cursor(buffered=True)
    print("Database connected successfully!")
except Error as e:
    print(f"Error connecting to MySQL: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        # validation
        if not name or not email or not message:
            return jsonify({
                "status": "error",
                "message": "All fields are required!"
            })

        # insert into database
        sql = "INSERT INTO contacts(name,email,message) VALUES(%s,%s,%s)"
        cursor.execute(sql, (name, email, message))
        db.commit()

        return jsonify({
            "status": "success",
            "message": "Message sent successfully!"
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "status": "error",
            "message": "Server error occurred"
        })

if __name__ == "__main__":
    app.run(debug=True)