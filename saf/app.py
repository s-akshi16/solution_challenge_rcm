from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'super_secret_hackathon_key' # Needed for user sessions

# --- EMAIL CONFIGURATION ---
# For a hackathon, hardcode the sender info here. 
SENDER_EMAIL = "enteremail@gmail.com"
SENDER_APP_PASSWORD = "password"
RECEIVER_EMAIL = "enteremail@gmail.com"

@app.route('/', methods=['GET', 'POST'])
def login():
    # If the user submits the form, save their name in the session
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Protect the dashboard so only logged-in users can see it
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/trigger_alert', methods=['POST'])
def trigger_alert():
    # This endpoint is called by JavaScript when decibels cross the threshold
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    username = session['username']
    
    try:
        # Construct the email
        msg = MIMEText(f"EMERGENCY ALERT! {username} is in danger and requires immediate assistance.")
        msg['Subject'] = f"EMERGENCY: {username}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        # Send the email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
            
        return jsonify({'status': 'success', 'message': 'Alert email sent!'})
    except Exception as e:
        print(f"Failed to send email: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)