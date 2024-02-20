from dotenv import load_dotenv
import json
import shutil
import datetime

import office365sdk
from office365sdk import *

load_dotenv()
site_url = os.getenv('SHAREPOINT_SITE_URL')
tenant_id = os.getenv('SHAREPOINT_TENANT_ID')
client_id = os.getenv('SHAREPOINT_CLIENT_ID')
cert_thumbprint = os.getenv('SHAREPOINT_CERT_THUMBPRINT')
cert_pem = os.getenv('SHAREPOINT_CERT_PEM')

# temporary file to run tests, before adding to examples/ tests/

def test_get_folder_summary_success(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    assert site.check_connection_valid(site_url) == True

    folder_path = "Documents/sharepoint-test-folder1"
 
    folder_summary = site.get_folder(folder_path)
    print(json.dumps(folder_summary, indent=4))

    folder_files_summary = site.get_files_in_folder(folder_path)
    print(json.dumps(folder_files_summary, indent=4))


def test_flow_rag_inference_acl_success(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    assert site.check_connection_valid(site_url) == True

    # ACL check
    user_email = "sushamashroff@ciscosystems335.onmicrosoft.com"
    file_path = "/sites/test-site-1/Shared Documents/sharepoint-test-site-1-test-doc.docx"
 
    assert site.check_user_access_for_file(user_email, file_path, "OPEN_ITEMS") == True

def test_flow_site_connection(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    assert site.check_connection_valid(site_url) == True

def test_flow_site_reconnection(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    if site.check_connection_valid("invalid") == False: # simulating a failed connection (this would actually be site_url instead of "invalid")
        assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True

def test_flow_download_file():  

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    assert site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem) == True
    assert site.check_connection_valid(site_url) == True

    # local storage handling for downloaded files
    # download path should map to appropriate Volume mount when running on K8s cluster
    download_path = "/Users/sushroff/Desktop/sharepoint_download_temp"
    shutil.rmtree(download_path, ignore_errors=True)
    os.mkdir(download_path) 
    print("Directory created", download_path) 

    file_path = "/sites/test-site-1/Shared Documents/sharepoint-test-folder1/nested-in-folder1/nested-file-with-custom-metadata.docx"
    #file_path = "/sites/test-site-1/Shared Documents/200MB-TESTFILE.pdf" # 20sec
    file_size = "19392"
    
    file_download_summary, isOk = site.download_file(file_path, file_size, download_path)
    if not isOk:
        print("Download file errored")
    else:
        print(json.dumps(file_download_summary, indent=4))

def test_flow_rag_inference_acl_success(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem)
    assert site.check_connection_valid(site_url) == True
    
    # ACL check
    user_email = "sushamashroff@ciscosystems335.onmicrosoft.com"
    file_path = "/sites/test-site-1/Shared Documents/sharepoint-test-site-1-test-doc.docx"
 
    #file = site.get_file_by_path(file_path)
    #if file is None:
    #    print("File not found")
    
    # above file check also done as part of this fn below for permission
    assert site.check_user_access_for_file(user_email, file_path, "OPEN_ITEMS") == True

def test_get_folder_files(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem)
    assert site.check_connection_valid(site_url) == True

    folder_path = "Documents/sharepoint-test-folder1"
    
    # list all files in folder with tag (tag_column_name from Sharepoint to be provided)
    tag_column_name = "custom-metadata"
    folder_files_summary = site.get_files_in_folder(folder_path, tag_column_name)
    print(json.dumps(folder_files_summary, indent=4))

def test_get_folder_files_modified_after(): 

    # connection setup
    site = office365sdk.SharePointSite(site_url)
    site.connect_with_client_certificate(tenant_id, client_id, cert_thumbprint, cert_pem)
    assert site.check_connection_valid(site_url) == True

    folder_path = "Documents/sharepoint-test-folder1"
    
    # list all files in folder with tag (tag_column_name from Sharepoint to be provided)
    tag_column_name = "custom-metadata"
    from_datetime = datetime.datetime(2024, 2, 14, 0, 0)
    folder_files_summary = site.get_files_in_folder(folder_path, tag_column_name, from_datetime)
    print(json.dumps(folder_files_summary, indent=4))


#def test_func(): 

    # connection setup
    #ctx = office365sdk.connect_with_client_certificate(site_url, tenant_id, client_id, cert_thumbprint, cert_pem)
    #assert office365sdk.check_context_valid(ctx) == True
 
    #folder_stats = office365sdk.get_folder(ctx, "Documents/sharepoint-test-folder1/nested-in-folder1")
    #folder_stats = office365sdk.get_folder(ctx, "my doc lib with spaces/folder with spaces")
    #print(folder_stats)

    #folder_stats = office365sdk.get_folder(ctx, "Documents")
    #doc_lib_stats = office365sdk.get_folder(ctx, "my doc lib with spaces")
    #doc_lib_stats = office365sdk.get_folder(ctx, "my-test-doc-lib")
    #print(doc_lib_stats)

    #file_stats = office365sdk.get_files_in_folder(ctx, "Documents")
    #file_stats = office365sdk.get_files_in_folder(ctx, "Documents/sharepoint-test-folder1")
    #file_stats = office365sdk.get_files_in_folder(ctx, "Documents/sharepoint-test-folder1/nested-in-folder1")
    #file_stats = office365sdk.get_files_in_folder(ctx, "my-test-doc-lib")
    #file_stats = office365sdk.get_files_in_folder(ctx, "my-test-doc-lib/")
    #file_stats = office365sdk.get_files_in_folder(ctx, "my doc lib with spaces")
    #print(json.dumps(file_stats, indent=4))

if __name__ == '__main__':
    #test_func()
    #test_flow_rag_inference_acl_success()
    #test_get_folder_summary_success()
    #test_flow_site_connection()
    #test_flow_site_reconnection()
    #test_flow_rag_inference_acl_success()
    #test_flow_download_file()
    #test_get_folder_files()
    test_get_folder_files_modified_after()
