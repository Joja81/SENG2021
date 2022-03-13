from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import re
from app.functions.error import InputError
import smtplib
from app.functions import ublExtractor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

mail = smtplib.SMTP(host= os.environ.get('SMTP_HOST'), port=os.environ.get('SMTP_PORT'))
mail.starttls()
mail.login(os.environ.get('SMTP_USERNAME'), os.environ.get('SMTP_PASSWORD'))

def validate_email(email):
    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if not (re.fullmatch(email_regex,email)):
        raise InputError(description='email is not of valid format')

def send_email(xml):
    """
    Sends UBL invoice to the first ``cac:AccountingCustomerParty`` entry 
    in said UBL.

    Parameters
    ----------
    xml : string
        an `XML` formatted with ``PEPPOL BIS Billing 3.0 standard``

    Returns
    -------
    """
    
    contacts = ublExtractor.customerContact(xml)
    
    validate_email(contacts["cust_email"])

    #create email
    msg = MIMEMultipart()
    msg['Subject'] = (f'Invoice from {contacts["bill_name"]}')
    msg['From'] = (f'{contacts["bill_email"]}')
    msg['To'] = (f'{contacts["cust_email"]}')
    message = f"""
        <html>
            <head></head>
            <body>
                <p>Hello {contacts["cust_name"]},<br>
                    Attached is your invoice.<br>
                    Kind regards,<br>
                    {contacts["bill_name"]} <br>
                    {contacts["bill_email"]}.
                </p>
            </body>
        </html>
    """

    body = MIMEText(message,'HTML')
    msg.attach(body)
    msg.attach(MIMEApplication(xml, Name='invoice.xml'))
    mail.sendmail(msg['From'], msg['To'], msg.as_string())

def exit():
    mail.quit()
    
