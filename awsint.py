from flask import Flask, render_template, request, jsonify
import boto3
import uuid
from datetime import datetime

# Step 1: Create the Flask app instance
app = Flask(__name__)

# Step 2: Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')  # Replace with your region

# Tables
photographers_table = dynamodb.Table('photographers')
bookings_table = dynamodb.Table('booking')

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Booking form route
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        photographer_id = request.form.get('photographer_id')
        user_id = request.form.get('user_id')
        date = request.form.get('date')

        # Create unique booking ID
        booking_id = str(uuid.uuid4())

        # Store booking in DynamoDB Bookings table
        bookings_table.put_item(Item={
            'booking_id': booking_id,
            'photographer_id': photographer_id,
            'user_id': user_id,
            'date': date,
            'timestamp': datetime.now().isoformat()
        })

        return f"<h2 style='color:green;'>Booking Confirmed! For {photographer_id} on {date}.</h2><a href='/'>Back to Home</a>"

    return render_template('book.html')

# Display photographers from DynamoDB
@app.route('/show-photographers')
def show_photographers():
    response = photographers_table.scan()
    photographers = response.get('Items', [])

    # ✅ FIXED: use correct DynamoDB key - 'photographer_id'
    availability_data = {
        p['photographer_id']: p.get('availability', []) for p in photographers
    }

    return render_template('photographers.html',
                           photographers=photographers,
                           availability_data=availability_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


photographers.html
<!DOCTYPE html>
<html>
<head>
  <title>Photographers</title>
  <style>
    body {
      background-color: #f7f7f7;
      font-family: Arial;
      text-align: center;
      padding: 50px;
    }
    .card {
      background: white;
      margin: 20px auto;
      padding: 20px;
      width: 300px;
      border-radius: 8px;
      box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    h3 {
      margin-bottom: 10px;
      color: #2c3e50;
    }
    p {
      color: #555;
    }
    img {
      margin-top: 10px;
      border-radius: 4px;
      width: 200px;
      height: auto;
    }
  </style>
</head>
<body>
  <h2>Available Photographers</h2>

  {% for p in photographers %}
    <div class="card">
      <h3>{{ p['Name'] }}</h3>
      <p><strong>ID:</strong> {{ p['photographer_id'] }}</p>
      <p><strong>Skills:</strong> {{ p['Skills'] }}</p>
      <p><strong>Availability:</strong> {{ p['availability'] | join(', ') }}</p>

      {% if p['Photo'] %}
        <img src="{{ p['Photo'] }}" alt="{{ p['Name'] }}">
      {% else %}
        <p>No image available</p>
      {% endif %}
    </div>
  {% endfor %}

  <a href="/" style="display: inline-block; margin-top: 20px;">← Back to Home</a>
</body>
</html>

  <a href="/" style="display: inline-block; margin-top: 20px;">← Back to Home</a>
</body>
</html>
