from dotenv import load_dotenv
import json
import shutil

import vowelsharepoint
from vowelsharepoint.office365sdk import *

load_dotenv()
site_url = os.getenv('SHAREPOINT_SITE_URL')
tenant_id = os.getenv('SHAREPOINT_TENANT_ID')
client_id = os.getenv('SHAREPOINT_CLIENT_ID')
cert_thumbprint = os.getenv('SHAREPOINT_CERT_THUMBPRINT')
cert_pem = os.getenv('SHAREPOINT_CERT_PEM')


def test_flow_download_file():  

    # connection setup
    site = vowelsharepoint.office365sdk.SharePointSite(site_url)
    assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    assert site.check_connection_valid(site_url) == True

    # local storage handling for downloaded files
    # download path should map to appropriate Volume mount when running on K8s cluster
    download_path = "/Users/sushroff/Desktop/sharepoint_download_temp"
    shutil.rmtree(download_path, ignore_errors=True)
    os.mkdir(download_path) 
    print("Directory created", download_path) 

    # file_path, file_size -> as returned by site.get_files_in_folder(...))
    file_path = "/sites/test-site-1/Shared Documents/sharepoint-test-folder1/nested-in-folder1/nested-file-with-custom-metadata.docx"
    file_size = "19392"
    
    file_download_summary, isOk = site.download_file(file_path, file_size, download_path)
    if not isOk:
        print("Download file errored")
    else:
        print(json.dumps(file_download_summary, indent=4))
    
if __name__ == '__main__':
    test_flow_download_file()
