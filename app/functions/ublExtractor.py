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
    ``{'custS_name' : '<Customer Name>', 'cust_email': '<Customer@email>' 
        'Bill_name : '<Biller Name>, 'Bill_email': '<Biller@email>'}``
        Customer Email contained in the UBL
    """
    
    invoice = xmltree.fromstring(xml)
    
    cusParty = invoice.find('cac:AccountingCustomerParty',NAMESPACE)        #finds the customer
    customer = cusParty.find('cac:Party',NAMESPACE)                         #enters the customer party info
    continfo = customer.find('cac:Contact',NAMESPACE)                       #finds the child element cac:Contact

    supplier = invoice.find('cac:AccountingSupplierParty', NAMESPACE)
    seller = supplier.find('cac:Party',NAMESPACE)
    contseller = seller.find('cac:Contact',NAMESPACE)    

    contact = {"cust_name": continfo.find('cbc:Name',NAMESPACE).text,            #puts the info from cac:Contact into a dict
    "cust_email": continfo.find('cbc:ElectronicMail',NAMESPACE).text,
    "bill_name": contseller.find('cbc:Name',NAMESPACE).text, 
    "bill_email": contseller.find('cbc:ElectronicMail',NAMESPACE).text}

    return contact


def invoice_contents(xml):
    """
    Extracts all relevant data to render a neat email with xml contents

    Searches through and extracts
    Parameters
    ----------
    xml : string
        an `XML` formatted with ``PEPPOL BIS Billing 3.0 standard``

    Returns
    -------
    ``{'compay' : '<company name>', 'issue': '<dd/mm/yyyy>' 
        'due' : '<dd/mm/yyyy>', 'currency': '<CurCode>', 
        'payable': '<payable amount>'}``
    """

    invoice = xmltree.fromstring(xml)

    # total amount
    LMtotal = invoice.find('cac:LegalMonetaryTotal',NAMESPACE)
    totalpayable = LMtotal.find('cbc:PayableAmount',NAMESPACE).text
    # currency code
    currency = invoice.find('cbc:DocumentCurrencyCode',NAMESPACE).text

    # due date
    due = invoice.find('cbc:DueDate',NAMESPACE).text
    # issue date
    issue = invoice.find('cbc:IssueDate',NAMESPACE).text

    # sender
    supplier = invoice.find('cac:AccountingSupplierParty', NAMESPACE)
    party = supplier.find('cac:Party',NAMESPACE)
    seller = party.find('cac:PartyName',NAMESPACE)
    sender = seller.find('cbc:Name',NAMESPACE).text

    print({'company' : sender, 'issue': issue, 
        'due' : due, 'currency': currency, 
        'payable': totalpayable})

    return {'company' : sender, 'issue': issue, 
        'due' : due, 'currency': currency, 
        'payable': totalpayable}


