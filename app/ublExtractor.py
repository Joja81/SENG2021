import defusedxml.ElementTree as xmltree

NAMESPACE = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
    'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}

def customerContact(xml):
    """
    Extracts customer emails.

    Searches through and extracts contact email of the first ``cac:AccountingCustomerParty`` entry 
    in a given UBL.

    Parameters
    ----------
    xml : string
        an `XML` formatted with ``PEPPOL BIS Billing 3.0 standard``

    Returns
    -------
    ``{'name' : '<Customer Name>', 'email': '<Customer@email>'}``
        Customer Email contained in the UBL
    """
    
    invoice = xmltree.fromstring(xml)
    
    cusParty = invoice.find('cac:AccountingCustomerParty',NAMESPACE)        #finds the customer
    customer = cusParty.find('cac:Party',NAMESPACE)                         #enters the customer party info
    continfo = customer.find('cac:Contact',NAMESPACE)                       #finds the child element cac:Contact

    contact = {"name": continfo.find('cbc:Name',NAMESPACE).text,            #puts the info from cac:Contact into a dict
    "email": continfo.find('cbc:ElectronicMail',NAMESPACE).text}

    return contact