from dotenv import load_dotenv

import vowelsharepoint
from vowelsharepoint.office365sdk import *

load_dotenv()
site_url = os.getenv('SHAREPOINT_SITE_URL')
tenant_id = os.getenv('SHAREPOINT_TENANT_ID')
client_id = os.getenv('SHAREPOINT_CLIENT_ID')
cert_thumbprint = os.getenv('SHAREPOINT_CERT_THUMBPRINT')
cert_pem = os.getenv('SHAREPOINT_CERT_PEM')

def test_flow_site_connection(): 

    # connection setup
    site = vowelsharepoint.office365sdk.SharePointSite(site_url)
    assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    assert site.check_connection_valid(site_url) == True

def test_flow_site_reconnection(): 

    site = vowelsharepoint.office365sdk.SharePointSite(site_url)
    # check existing connection ok, else reconnect
    if site.check_connection_valid("invalid") == False: # simulating a failed connection (this would actually be site_url instead of "invalid")
        assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    
if __name__ == '__main__':
    test_flow_site_connection()
    test_flow_site_reconnection()
