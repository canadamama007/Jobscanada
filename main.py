from flask import Flask, request, send_file
import requests, pandas as pd
from bs4 import BeautifulSoup
import smtplib, os
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/')
def home():
    return '''<form action="/search" method="post">
                Location (Province): <input name="location"><br>
                Email: <input name="email"><br>
                <input type="submit" value="Submit">
              </form>'''

@app.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    email = request.form['email']
    
    # Dummy scraping result
    data = [{'Job': 'Part-time', 'Location': location}]
    df = pd.DataFrame(data)
    filename = f'results_{location}.xlsx'
    df.to_excel(filename, index=False)

    send_email(email, filename)
    return f"Email sent to {email} with job data for {location}"

def send_email(to_email, file):
    msg = EmailMessage()
    msg['Subject'] = 'Job Report'
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = to_email
    msg.set_content("Attached is your job report.")

    with open(file, 'rb') as f:
        msg.add_attachment(f.read(), filename=file, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)
