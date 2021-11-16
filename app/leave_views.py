from app import app          
from app.database import Database
from app import email      

from flask import render_template, request, url_for, redirect, session


@app.route('/login/dashboard/',methods=['POST','GET'])
def leave_days():
    msg = ''
    ec_number = session['ec_number']
    email = session['email']
    # Fetch for updated available leave days
    user = Database.find_one("available_days",{'ec_number':ec_number})
    # Convert available leave days to interger
    available_days = int(user['days'])
    # Get form data
    dept = request.form['dept']
    position = request.form['position']
    requested_days = int(request.form['days'])
    # Calculate remaining days after user apply for leave
    remaining_days = available_days - requested_days
    
    # Insert leave details into leave collection
    leave = {"ec_number": ec_number, "dept": dept,"position": position,"days":requested_days}
    Database.insert("leave",leave)
    # Update available days with new value after user applies for leave
    query = {"ec_number": ec_number}
    new_value = {"$set":{"days":remaining_days}}
    Database.update_one("available_days",query,new_value)
    msg = 'Successfully Applied For Leave. We Will Give You Feedback Soon!'

    # Send email with provided details
    content = f"""
          Dear Sir/Ma'am \n

          I hereby apply for leave, with the details attached below \n
          Email: {email} \n
          Department: {dept} \n
          Position: {position} \n
          Leave Days: {requested_days}
    """
    email.sendEmail('Leave Application',content)

    return render_template('dashboard.html', msg=msg,available_days=remaining_days)