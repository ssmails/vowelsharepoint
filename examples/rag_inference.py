from dotenv import load_dotenv

import vowelsharepoint
from vowelsharepoint.office365sdk import *

load_dotenv()
site_url = os.getenv('SHAREPOINT_SITE_URL')
tenant_id = os.getenv('SHAREPOINT_TENANT_ID')
client_id = os.getenv('SHAREPOINT_CLIENT_ID')
cert_thumbprint = os.getenv('SHAREPOINT_CERT_THUMBPRINT')
cert_pem = os.getenv('SHAREPOINT_CERT_PEM')


def test_flow_rag_inference_acl_success(): 

    # connection setup
    site = vowelsharepoint.office365sdk.SharePointSite(site_url)
    site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem)
    assert site.check_connection_valid(site_url) == True

    # ACL check
    user_email = "sushamashroff@ciscosystems335.onmicrosoft.com"
    file_path = "/sites/test-site-1/Shared Documents/sharepoint-test-site-12-test-doc.docx"
 
    #file = site.get_file_by_path(file_path)
    #if file is None:
    #    print("File not found")
    
    # file and user exists check - also done as part of this fn.
    assert site.check_user_access_for_file(user_email, file_path, "OPEN_ITEMS") == True

if __name__ == '__main__':
    test_flow_rag_inference_acl_success()
