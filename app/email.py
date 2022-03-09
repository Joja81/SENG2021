from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from pydoc import plain
import re
from app.error import InputError
import smtplib
from app import ublExtractor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


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
    msg['Subject'] = (f'URGENT: Invoice from {contacts["bill_name"]}')
    msg['From'] = (f'{contacts["bill_email"]}')
    msg['To'] = (f'{contacts["cust_email"]}')
    body = MIMEText(f'{contacts["cust_name"]}, \nYou have a new invoice! \nKind regards, \n{contacts["bill_name"]} \n{contacts["bill_email"]}.\n\n', 'plain')
    msg.attach(body)
    msg.attach(MIMEApplication(xml, Name='invoice.xml'))
    
    
    mail = smtplib.SMTP(host= os.environ.get('SMTP_HOST'), port=os.environ.get('SMTP_PORT'))
    mail.starttls()
    mail.login(os.environ.get('SMTP_USERNAME'), os.environ.get('SMTP_PASSWORD'))

    mail.sendmail(msg['From'], msg['To'], msg.as_string())

    mail.quit()
