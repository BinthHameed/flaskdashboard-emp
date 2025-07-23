import os
from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import dotenv
from dotenv import load_dotenv
from flask_session import Session

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load environment variables from .env file
load_dotenv()

# Set up Flask for production
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Get the admin password from environment variables
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\HP\\Documents\\skyapp\\firebase_adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://info-sync-official-default-rtdb.firebaseio.com'
})

# Configure session
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'SkynetsolutionsQatar')  # Replace with a strong secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def filter_data(data, filter_type, specific_date=None, specific_month=None):
    filtered_data = []
    now = datetime.now()

    if isinstance(data, dict):
        data = list(data.values())

    for item in data:
        item_date_str = item.get('support_date', '')
        try:
            item_date = datetime.strptime(item_date_str, '%Y-%m-%d')
        except ValueError:
            continue

        if filter_type == 'today' and item_date.date() == now.date():
            filtered_data.append(item)
        elif filter_type == 'week':
            start_of_week = now - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            if start_of_week.date() <= item_date.date() <= end_of_week.date():
                filtered_data.append(item)
        elif filter_type == 'month' and item_date.month == now.month and item_date.year == now.year:
            filtered_data.append(item)
        elif filter_type == 'specific_date' and specific_date:
            if isinstance(specific_date, str):
                specific_date = datetime.strptime(specific_date, '%Y-%m-%d').date()
            if item_date.date() == specific_date:
                filtered_data.append(item)
        elif filter_type == 'specific_month' and specific_month:
            if isinstance(specific_month, str):
                try:
                    specific_month_date = datetime.strptime(specific_month, '%Y-%m')
                except ValueError:
                    continue
            else:
                specific_month_date = specific_month
            if item_date.month == specific_month_date.month and item_date.year == specific_month_date.year:
                filtered_data.append(item)
        elif filter_type == 'all':
            filtered_data.append(item)
    
    return filtered_data

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/index')
        else:
            error = 'Incorrect password. Please try again.'
    if session.get('logged_in'):
        return redirect('/index')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect('/')

    filter_type = request.args.get('filter', 'today')
    specific_date = request.args.get('specific_date')
    specific_month = request.args.get('specific_month')
    employee_name = request.args.get('employee_name')

    ref = db.reference("service")
    data = ref.get()

    if isinstance(data, dict):
        data = list(data.values())

    filtered_data = filter_data(data, filter_type, specific_date, specific_month)

    all_employee_names = sorted(set(item.get('employee') for item in filtered_data))

    if employee_name:
        employee_name = employee_name.lower()
        table_data = [item for item in filtered_data if item.get('employee', '').lower() == employee_name]
    else:
        table_data = filtered_data

    closed_issues = sum(1 for item in table_data if item.get('status_name') == 'Close')
    open_issues = sum(1 for item in table_data if item.get('status_name') == 'Open')

    employee_performance = {}
    for item in filtered_data:
        employee = item.get('employee')
        if employee not in employee_performance:
            employee_performance[employee] = 0
        employee_performance[employee] += 1

    return render_template('index.html', 
                           data=table_data, 
                           closed_issues=closed_issues, 
                           open_issues=open_issues,
                           employee_performance=employee_performance,
                           employee_names=all_employee_names)

if __name__ == '__main__':
    app.run()
