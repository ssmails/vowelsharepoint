from dotenv import load_dotenv
import json

import vowelsharepoint
from vowelsharepoint.office365sdk import *

load_dotenv()
site_url = os.getenv('SHAREPOINT_SITE_URL')
tenant_id = os.getenv('SHAREPOINT_TENANT_ID')
client_id = os.getenv('SHAREPOINT_CLIENT_ID')
cert_thumbprint = os.getenv('SHAREPOINT_CERT_THUMBPRINT')
cert_pem = os.getenv('SHAREPOINT_CERT_PEM')

def test_get_folder_files_with_tags(): 

    # connection setup
    site = vowelsharepoint.office365sdk.SharePointSite(site_url)
    site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem)
    assert site.check_connection_valid(site_url) == True

    folder_path = "Documents/sharepoint-test-folder1"
    
    # list all files in folder with tag (tag_column_name from Sharepoint to be provided)
    tag_column_name = "custom-metadata"
    folder_files_summary = site.get_files_in_folder(folder_path, tag_column_name)
    print(json.dumps(folder_files_summary, indent=4))


def test_get_folder_files(): 

    # connection setup
    site = vowelsharepoint.office365sdk.SharePointSite(site_url)
    site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem)
    assert site.check_connection_valid(site_url) == True

    folder_path = "Documents/sharepoint-test-folder1"
 
    folder_files_summary = site.get_files_in_folder(folder_path)
    print(json.dumps(folder_files_summary, indent=4))

if __name__ == '__main__':
    test_get_folder_files()
    test_get_folder_files_with_tags()
