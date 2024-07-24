from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random
import boto3

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.secret_key = 'whatever'

random_int = random.randint(1, 100)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1233281019776340049/ogLfkroHdPaDE9rLiEfspn2VBcmh-Ox1Tn1UKyFbEiYkoxFlap8M2A-RzKecHtLtU_mv'

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('WebStackDynamodbStack9E738F00-UsersTable9725E9C8-MBN9SKXT0ZW0')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        table.put_item(
            Item={
                'userId': username,
                'email': email,
                'password': hashed_password
            }
        )
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        
        response = table.get_item(
            Key={
                'email': request.form['email']
            }
        )
        user = response.get('Item')
        
        if user and check_password_hash(user['password'], password):
            session['username'] = user['userId']
            return redirect(url_for('profile'))
        else:
            return 'Login failed'
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/random')
def random_number():
    return {'randomNumber': random_int}


@app.route('/discord', methods=['GET', 'POST'])
def discord():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            send_to_discord(message)
            return redirect(url_for('discord'))
    return render_template('discord.html')

@app.route('/')
def hello_world():
    return render_template('page.html')

def send_to_discord(message):
    data = {
        'content': message
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
