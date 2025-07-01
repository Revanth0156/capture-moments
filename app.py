from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret in production
app.permanent_session_lifetime = timedelta(minutes=30)

# Dummy users for login
users = {
    "revanth": "1234",
    "admin": "admin"
}

# Photographer data
photographers = [
    {
        "id": "p1",
        "name": "Amit Lensman",
        "skills": ["Wedding", "Portrait"],
        "image": "amit.jpg",
        "cost": "₹15,000 per event"
    },
    {
        "id": "p2",
        "name": "Sana Clickz",
        "skills": ["Fashion", "Event"],
        "image": "sana.jpg",
        "cost": "₹12,000 per event"
    },
    {
        "id": "p3",
        "name": "Rahul Snapz",
        "skills": ["Travel", "Nature"],
        "image": "rahul.jpg",
        "cost": "₹10,000 per event"
    },
    {
        "id": "p4",
        "name": "Neha Frames",
        "skills": ["Pre Wedding", "College Events"],
        "image": "neha.jpg",
        "cost": "₹11,500 per event"
    }
]

# Route: Home → redirect to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session.permanent = True
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Route: Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

# Route: Show photographers
@app.route('/show-photographers')
def show_photographers():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('photographers.html', photographers=photographers)

# Route: Book photographer
@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        category = request.form.get('category')
        date = request.form.get('date')
        return render_template('confirmed.html',
                               photographer_id=photographer_id,
                               category=category,
                               date=date)

    selected_id = request.args.get('photographer_id')
    return render_template('book.html',
                           photographers=photographers,
                           selected_id=selected_id)

# Route: Portfolio
@app.route('/portfolio')
def portfolio():
    if 'user' not in session:
        return redirect(url_for('login'))

    photos = [
        {
            "src": "portfolio/wedding1.jpg",
            "title": "Amit Lensman",
            "skills": ["Wedding", "Portrait"],
            "famous_for": "Famous for capturing timeless Wedding & Portrait moments"
        },
        {
            "src": "portfolio/fashion1.jpg",
            "title": "Sana Clickz",
            "skills": ["Fashion", "Event"],
            "famous_for": "Known for stylish Fashion & vibrant Event photography"
        },
        {
            "src": "portfolio/travel1.jpg",
            "title": "Rahul Snapz",
            "skills": ["Travel", "Nature"],
            "famous_for": "Specializes in scenic Travel & Nature photography"
        },
        {
            "src": "portfolio/prewedding1.jpg",
            "title": "Neha Frames",
            "skills": ["Pre Wedding", "College Events"],
            "famous_for": "Expert in romantic Pre Wedding & College event shoots"
        }
    ]
    return render_template('portfolio.html', photos=photos)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
