'''
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('job_portal.db')  # SQLite database (file-based)
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # Your email address from environment variables
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Your email password from environment variables

# Function to send email
def send_email(to_email, job_id, organization, user_email):
    subject = f'Job Application for {job_id} at {organization}'
    body = f'User with email {user_email} has applied for the job ID: {job_id}.'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs', methods=['POST'])
def jobs():
    skill1 = request.form['skill1'].lower()
    skill2 = request.form.get('skill2', '').lower()
    skill3 = request.form.get('skill3', '').lower()

    conn = get_db_connection()
    cur = conn.cursor()

    # Prepare a list of skills to search for (non-empty)
    skills = [skill for skill in [skill1, skill2, skill3] if skill]

    grouped_jobs = {}

    # Loop through each skill and fetch jobs from the table named after the skill
    for skill in skills:
        try:
            query = f"SELECT * FROM {skill};"
            cur.execute(query)
            jobs = cur.fetchall()
            # Group jobs by skill
            if skill not in grouped_jobs:
                grouped_jobs[skill] = []
            grouped_jobs[skill].extend(jobs)
        except sqlite3.OperationalError:
            # Handle case where the table does not exist
            print(f"Table for skill '{skill}' does not exist.")

    cur.close()
    conn.close()

    return render_template('jobs.html', grouped_jobs=grouped_jobs)

@app.route('/apply_job', methods=['POST'])
def apply_job():
    job_id = request.form['job_id']
    skill = request.form['skill']  # Get the skill from the form
    user_email = request.form['user_email']

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Query the correct table based on the skill and job_id
        query = f"SELECT name_of_organization, emailid FROM {skill} WHERE job_id = ?"
        cur.execute(query, (job_id,))
        job = cur.fetchone()

        if job:
            organization = job['name_of_organization']
            job_provider_email = job['emailid']  # Assuming you have an 'emailid' column

            # Send email notification
            send_email(job_provider_email, job_id, organization, user_email)
        else:
            print(f"Job with ID {job_id} not found.")
    except sqlite3.OperationalError as e:
        print(f"Error querying the table '{skill}': {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('jobs'))



if __name__ == '__main__':
    app.run(debug=True, port=8080)'''





from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('job_portal2.db')  # SQLite database (file-based)
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # Your email address from environment variables
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Your email password from environment variables

# Function to send email
def send_email(to_email, job_id, organization, user_info):
    subject = f'Job Application for {job_id} at {organization}'
    body = f"""User Information:
    Name: {user_info['name']}
    Email: {user_info['emailid']}
    Skills: {user_info['skill1']}, {user_info['skill2']}, {user_info['skill3']}
    The user has applied for the job ID: {job_id}."""
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs', methods=['POST'])
def jobs():
    skill1 = request.form['skill1'].lower()
    skill2 = request.form.get('skill2', '').lower()
    skill3 = request.form.get('skill3', '').lower()

    conn = get_db_connection()
    cur = conn.cursor()

    # Prepare a list of skills to search for (non-empty)
    skills = [skill for skill in [skill1, skill2, skill3] if skill]

    grouped_jobs = {}

    # Loop through each skill and fetch jobs from the table named after the skill
    for skill in skills:
        try:
            query = f"SELECT * FROM {skill};"
            cur.execute(query)
            jobs = cur.fetchall()
            # Group jobs by skill
            if skill not in grouped_jobs:
                grouped_jobs[skill] = []
            grouped_jobs[skill].extend(jobs)
        except sqlite3.OperationalError:
            # Handle case where the table does not exist
            print(f"Table for skill '{skill}' does not exist.")

    cur.close()
    conn.close()

    return render_template('jobs.html', grouped_jobs=grouped_jobs)

@app.route('/apply_job', methods=['POST'])
def apply_job():
    job_id = request.form['job_id']
    skill = request.form['skill']  # Get the skill from the form
    user_email = request.form['user_email']  # Assuming the email belongs to the logged-in user

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Query the correct table based on the skill and job_id
        query = f"SELECT name_of_organization, emailid FROM {skill} WHERE job_id = ?"
        cur.execute(query, (job_id,))
        job = cur.fetchone()

        if job:
            organization = job['name_of_organization']
            job_provider_email = job['emailid']  # Assuming you have an 'emailid' column

            # Fetch user details from the 'user' table
            user_query = "SELECT * FROM user WHERE emailid = ?"
            cur.execute(user_query, (user_email,))
            user_info = cur.fetchone()

            if user_info:
                # Send email notification to the job provider
                send_email(job_provider_email, job_id, organization, user_info)
            else:
                print(f"User with email {user_email} not found.")
        else:
            print(f"Job with ID {job_id} not found.")
    except sqlite3.OperationalError as e:
        print(f"Error querying the table '{skill}': {e}")
    finally:
        cur.close()
        conn.close()

    # After applying, redirect to a confirmation page
    return redirect(url_for('email_sent'))

# Confirmation page route
@app.route('/email_sent')
def email_sent():
    return render_template('email_sent.html')  # A simple page to confirm email sending

if __name__ == '__main__':
    app.run(debug=True, port=8080)
