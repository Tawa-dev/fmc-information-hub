from app import app          
from app.database import Database      
from app import email

from flask import render_template, request, url_for, redirect, session

@app.route('/login/dashboard/travel',methods=['POST','GET'])
def travel():
    msg = ''
    if request.method == 'POST':
        ec_number = session['ec_number']
        userEmail = session['userEmail']
        # Get form data
        dept = request.form['dept']
        position = request.form['position']
        destination = request.form['destination']
        description = request.form['description']
        budget = request.form['budget']
        
        # Insert travel allowance in travel collection
        travel = {"ec_number": ec_number,"dept":dept,"position": position,"destination":destination,"description":description,"budget":budget}
        Database.insert("travel",travel)
        msg = 'Successfully Applied For Travel Allowance. We Will Give You Feedback Soon!'

        # Send email with provided details
        content = f"""
          Dear Sir/Ma'am \n

          I hereby apply for a Travel Allowance, with the details attached below \n
          Email: {userEmail} \n
          Department: {dept} \n
          Position: {position} \n
          Destination: {destination} \n
          Description: {description} \n
          Budget: {budget}
         """
        email.sendEmail('Travel Allowance Application',content)

    return render_template('travel.html', msg=msg)
