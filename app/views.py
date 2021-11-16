from app import app          
from app.database import Database      

from flask import render_template, request, url_for, redirect, session
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app.secret_key = "testing"




# this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    
    # Check if "ec number" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'ec_number' in request.form and 'password' in request.form:
        # Create variables for easy access
        ec_number = request.form['ec_number']
        password = request.form['password']
        # Fetch one record and return result
        temporary_user = Database.find_one("users",{'ec_number':ec_number})
        # Check if a user was found with specified ec_number
        if temporary_user:
            # Compare user's password with hashed password from database
            correct_password = check_password_hash(temporary_user['password'],password)
        
            # If password is correct assign temporary user to be user
            if correct_password:
                user = temporary_user
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                #session['_id'] = user['_id']
                session['ec_number'] = user['ec_number']
                session['email'] = user['email']
                # Redirect to dashboard page
                return redirect(url_for('dashboard'))
            else:
                # Password is wrong
                msg = 'Password is wrong!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'EC Number does not exist!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

# this will be the logout page
@app.route('/login/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   #session.pop('_id', None)
   session.pop('ec_number', None)
   # Redirect to login page
   return redirect(url_for('login'))

# this will be the registration page, we need to use both GET and POST requests
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "ec_number", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'ec_number' in request.form:
        # Create variables for easy access
        ec_number = request.form['ec_number']
        password = request.form['password']
        # Change user's password to hashed password
        hash_password = generate_password_hash(password)
        email = request.form['email']
        # Check if account exists 
        user = Database.find_one("users",{'ec_number':ec_number})
       
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', ec_number):
            msg = 'Username must contain only characters and numbers!'
        elif not ec_number or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users collection
            employee = {"ec_number": ec_number, "email": email,"password": hash_password}
            # inititalize available leave days to 3
            availableDays = {"ec_number": ec_number,"days":3}
            Database.insert("users",employee)
            Database.insert("available_days",availableDays)
            msg = 'You have successfully registered! You can Login'
    
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


#  this will be the home page, only accessible for loggedin users
@app.route('/login/dashboard')
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page 
        ec_number = session['ec_number']
        # Fetch for the available leave days for the loggedin user
        user = Database.find_one("available_days",{'ec_number':ec_number})
        # Convert available days to integer
        available_days = int(user['days'])
        # set todays's day
        #toDay = datetime.today()
        # Add a flag variable to determine if we have already incremented
        

        # Check if its first day of a month, if it is increment leave days by 3
        #if toDay == '2021-11-02 20:26:39.834847':
            # Add a flag variable to determine if we have already incremented
            # Update available days by adding 3, since the user gets 3 days each month
            #incrementedDays = available_days + 3
            #available_days = incrementedDays
            #query = {"ec_number": ec_number} 
            #new_value = {"$set":{"days":incrementedDays}}
            #Database.update_one("available_days",query,new_value)
            
                

        return render_template('dashboard.html', ec_number=ec_number,available_days=available_days)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    

   