#import pytest
#from app import ublExtractor
#
#def test_AU_Example():
#    correct = {'name': 'Lisa Johnson', 'email':'lj@buyer.com.au'}
#    xml = open('./tests/files/AUInvoice.xml', 'rb')
#    contacts = ublExtractor.customerContact(xml.read())
#    assert(contacts == correct)