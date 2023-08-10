from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('subscribers.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                email TEXT NOT NULL,
                page_tag TEXT
            )
        ''')
        conn.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    return "Welcome to the Subscription Service!"

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    page_tag = request.args.get('page', 'unknown')
    if email:
        with sqlite3.connect('subscribers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO subscribers (email, page_tag) VALUES (?, ?)", (email, page_tag))
            conn.commit()
        return render_template('success.html')
    return "Email not provided!", 400

@app.route('/get-subscribers')
def get_subscribers():
    # Connect to the database
    conn = sqlite3.connect('subscribers.db')
    cursor = conn.cursor()

    # Fetch all subscribers and their page tags
    cursor.execute("SELECT email, page_tag FROM subscribers")
    subscribers = cursor.fetchall()

    # Close the database connection
    conn.close()

    # If there are no subscribers
    if not subscribers:
        return "No subscribers --- yet!"

    # Return the list of subscribers with their page tags
    return '<br>'.join([f"Email: {email} - Page: {page}" for email, page in subscribers])

# Commenting out this section as it's not needed on PythonAnywhere
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
