from app import app          
from app.database import Database  
from app import email    

from flask import render_template, request, url_for, redirect, session
from datetime import datetime


@app.route('/login/dashboard/asset_transfer',methods=['POST','GET'])
def asset_transfer():
    msg = ''
    if request.method == 'POST':
        ec_number = session['ec_number']
        email = session['email']
        # Get form data
        dept = request.form['dept']
        position = request.form['position']
        asset_name = request.form['asset_name']
        serial_num = request.form['serial_num']
        asset_num = request.form['asset_num']
        from_branch = request.form['from_branch']
        from_dept = request.form['from_dept']
        to_branch = request.form['to_branch']
        to_dept = request.form['to_dept']
        reason = request.form['reason']
        dateOfTransfer = request.form['dateOfTransfer']

        # If date of transfer is not given use that day's date
        #if dateOfTransfer == "":
           # dateOfTransfer = datetime.today().date()
        
        # Insert travel allowance in travel collection
        asset = {"ec_number": ec_number,"position": position,"asset_name":asset_name,"serial_num":serial_num,"asset_num":asset_num,"from_branch":from_branch,"from_dept":from_dept,"to_branch":to_branch,"to_dept":to_dept,"reason":reason,"dateOfTransfer":dateOfTransfer}
        Database.insert("asset_transfer",asset)
        msg = 'Successfully Registered Asset!'

        # Send email with provided details
        content = f"""
          Dear Sir/Ma'am \n

          I hereby register the Asset with details below \n
          Email: {email} \n
          Department: {dept} \n
          Position: {position} \n
          Asset Name: {asset_name} \n
          Serial Number: {serial_num} \n
          Asset Number: {asset_num} \n
          From Branch: {from_branch} \n
          From Department: {from_dept} \n
          To Branch: {to_branch} \n
          To Department: {to_dept} \n
          Reason For Transfer: {reason} \n
          Date Of Transfer: {dateOfTransfer}
         """
        email.sendEmail('Asset Registration',content)

    return render_template('asset.html', msg=msg)