from app import app          
from app.database import Database
from app import email      

from flask import render_template, request, url_for, redirect, session


@app.route('/login/dashboard/',methods=['POST','GET'])
def leave_days():
    msg = ''
    ec_number = session['ec_number']
    userEmail = session['userEmail']
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
    # If remaining_days is less than zero then calculate how much was exceeded with and also set remaining_days to zero
    if remaining_days < 0:
        exceed = abs(remaining_days)
        remaining_days = available_days
        # If available days is zero then, there are no leave days available
        if available_days == 0:
            msg = 'There Are No Leave Days Available'
        else:
            # If remaining_days is negative and available days is not zero, then there are leave days availble but user applied for too much
            msg = f'The Days You Requested Exceed Available Days By {exceed}'
    elif requested_days == 0:
          msg = 'You Can Not Apply For Zero Leave Days!'
    else:
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
              Email: {userEmail} \n
              Department: {dept} \n
              Position: {position} \n
              Leave Days: {requested_days}
        """
        email.sendEmail('Leave Application',content)

    return render_template('dashboard.html', msg=msg,available_days=remaining_days)
