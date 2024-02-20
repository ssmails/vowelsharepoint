import os

from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.permissions.kind import PermissionKind
from office365.sharepoint.listitems.caml.query import CamlQuery

from typing import Any

Documents_DocLibName = "Documents"
Documents_SitePathName = "Shared Documents"

List = "List"
Folder = "Folder"
File = "File"

# uses the office365 SDK to provide relevant functionality 
# https://github.com/vgrem/Office365-REST-Python-Client

# todo error handling
# todo logging

class SharePointSite:

    """
    creates a SharePointSite object associated with a provided SharePoint Site
    """

    def connect_with_client_certificate(self, tenant_id=None, client_id=None, cert_thumbprint=None, cert_pem=None) -> bool:

        """
        create new context/connection to this Sharepoint site using certificate credentials.
        
        https://github.com/vgrem/Office365-REST-Python-Client/wiki/How-to-connect-to-SharePoint-Online-with-certificate-credentials
        https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread

        tenant_id: Azure AD tenant id 
        client_id: Azure AD Application name
        cert_thumbprint: Azure AD App certificate thumbprint once uploaded
        cert_pem: certificate pem contents

        Return: True on success
        """
    
        if not tenant_id:
            print("invalid input:missing tenant_id")
            return False
        
        if not client_id:
            print("invalid input:missing client_id")
            return False
        
        if not cert_thumbprint:
            print("invalid input:missing cert_thumbprint")
            return False
        
        if not cert_pem:
            print("invalid input:missing cert_pem")
            return False

        cert_credentials = {
            "tenant": tenant_id,
            "client_id": client_id,
            "thumbprint": cert_thumbprint,
            "private_key": cert_pem,
        }
        ctx = ClientContext(self.site_url).with_client_certificate(**cert_credentials)
        if not ctx:
            print('error getting context for sharepoint site')
            return False

        self.ctx = ctx

        return True

    def check_connection_valid(self, siteurl) -> bool:     
        """
        checks if the existing context/connection is valid for provided site_url

        Return: True on success
        """

        if self.ctx is None:
            print('invalid context')
            return False

        current_web = self.ctx.web.get().execute_query_retry()
        site = current_web.url
        print("site:", site)
        if not site or site.lower() != siteurl.lower():
            print('invalid context for site')
            return False
            
        return True
    
    def get_file_by_path(self, file_path):
        """
        gets file at file_path, if exists

        Return : file on success, None on error
        """
        try:
            return self.ctx.web.get_file_by_server_relative_path(file_path).get().execute_query()
        except ClientRequestException as e:
            if e.response.status_code == 404:
                print(f'file:{file_path} does not belong to site')
                return None
            else:
                print(f'file:{file_path} does not belong to site:', e.response.text)
                raise ValueError(e.response.text)
    
    def get_user_by_email(self, user_email):
        """
        gets file at file_path, if exists

        Return : file on success, None on error
        """
        try:
            return self.ctx.web.site_users.get_by_email(user_email).get().execute_query()
        except ClientRequestException as e:
            if e.response.status_code == 404:
                print(f'user:{user_email} does not belong to site')
                return None
            else:
                print(f'user:{user_email} does not belong to site:', e.response.text)
                raise ValueError(e.response.text)


    def check_user_access_for_file(self, user_email, file_path, access) -> bool:
        """
        checks if user has provided access to the file
        user_email: Azure AD principal for user
        file_path: file path relative to sharepoint site Eg./sites/test-site-1/Shared Documents/sharepoint-doc.docx
        access: OPEN_ITEMS

        Return: True on success
        """

        if not user_email:
            print("invalid input:missing user_email")
            return False

        if not file_path:
            print("invalid input:missing file_path")
            return False

        if access != "OPEN_ITEMS": access = "OPEN_ITEMS" #only supported type for now
        if access == "OPEN_ITEMS":
            permission_kind = PermissionKind.OpenItems

        user_login_name = self.get_user_by_email(user_email)
        if user_login_name is None or user_login_name == "":
            return False
        
        target_file = self.get_file_by_path(file_path)
        if target_file is None:
            return False
        
        try:
            result = target_file.listItemAllFields.get_user_effective_permissions(user_login_name).execute_query_retry()
            if result.value.has(permission_kind):
                print(f'user:{user_email} has access to file:"{file_path}')
                return True
            else:
                print(f'user:{user_email} does not have access to file:"{file_path}')
                return False
        except ClientRequestException as e:
            print("error : User, file, error ",user_login_name, file_path, e.message)
            return False

    def get_doc_lib(self, list_title) -> Any:
        """
        get list summary.
        list_title: List Title for the Document Library (as recognized by Sharepoint)
        
        Returns: dict on success
        """

        lib = (
            self.ctx.web.lists.get_by_title(list_title)
            .root_folder.expand(["StorageMetrics"])
            .get()
            .execute_query()
        )
        return _get_system_object_summary(List, lib)

    def get_folder(self, input_path) -> Any:
        """
        get folder summary.
        input_path: Folder path, starting at Document Library for Eg. Documents/sharepoint-test-folder1
        
        Returns: dict on success
        """

        if not input_path:
            print("invalid input:missing input_path")
            return None
        
        doc_lib = self._get_doclib_from_inputpath(input_path) 
        folder_path = self._get_folderpath_from_inputpath(input_path) 

        print("doc_lib:", doc_lib)
        print("folder_path:", folder_path)

        # Eg input_path=Documents (doclib only usecase)
        if not folder_path:
            return self.get_doc_lib(self.ctx, doc_lib)

        lib = self.ctx.web.lists.get_by_title(doc_lib)
        items = (
            lib.items.select(["FileSystemObjectType"])
            .expand(["Folder"]) #office365/sharepoint/files/system_object_type.py
            .get_all()
            .execute_query_retry()
        )
        
        for idx, item in enumerate(items):  # type: int, ListItem
            if folder_path in item.folder.serverRelativeUrl: 
                return self._get_system_object_summary(Folder, item.folder)
    
        return None

    def get_files_in_folder(self, input_path, tag_column_name=None, modified_after=None) -> Any:
        """
        Note: use with caution
        get all files under given folder (including files under sub folders).
        input_path: Folder path, starting at Document Library for Eg. Documents/sharepoint-test-folder1
        tag_column_name: optional, column name from sharepoint to get tags
        modified_after: optional, get only files modified after datetime
        
        Returns []dict on success
        """
    
        if not input_path:
            print("invalid input:missing input_path")
            return None
        
        doc_lib = self._get_doclib_from_inputpath(input_path) 
        folder_path = self._get_folderpath_from_inputpath(input_path) 
 
        lib = self.ctx.web.lists.get_by_title(doc_lib)

        tag_column_name_internal = ""
        if tag_column_name:
            tag_column_name_internal = self._get_lib_field_internal(lib, tag_column_name)
        
        if modified_after:
            filter_text = "Modified gt datetime'{0}'".format(modified_after.isoformat())
            items = (
                lib.items.select(["FileSystemObjectType"])
                .filter(filter_text)
                .expand(["File", "Folder"]) #office365/sharepoint/files/system_object_type.py
                .get_all()
                .execute_query_retry()
            )
        else:
            items = (
                lib.items.select(["FileSystemObjectType"])
                .expand(["File", "Folder"]) #office365/sharepoint/files/system_object_type.py
                .get_all()
                .execute_query_retry()
            )

        file_list = []

        if folder_path == "": 
            # return all files from doc_lib as folder_path is empty. Eg.input_path = Documents
            for idx, item in enumerate(items):  # type: int, ListItem       
                if item.file_system_object_type == FileSystemObjectType.File:
                    summary = self._get_system_object_summary(File, item.file, tag_column_name_internal)
                    file_list.append(summary)
        else:
            # return files under input_path. Eg.Files under input_path = Documents/sharepoint-test-folder1
            folder = self.get_folder(input_path)
            for idx, item in enumerate(items):  # type: int, ListItem       
                if item.file_system_object_type == FileSystemObjectType.File:
                    #if folder_path in item.file.serverRelativeUrl:
                    if folder['server_relative_url'] in item.file.serverRelativeUrl:
                        summary = self._get_system_object_summary(File, item.file, tag_column_name_internal)
                        file_list.append(summary)
        
        return file_list

    def download_file(self, input_path, input_size_bytes, download_path) -> (dict, bool):
        """
        download file provided at input_path to download_path. 
        (open or checked out files will also be downloaded)

        input_path: File path (as returned by get_files_in_folder(...)), 
                    starting at Document Library for Eg. /sites/test-site-1/Shared Documents/{file_name}
                    todo support automatic path conversion here ?            
        download_path : local path to download file. local path must be pre-existing.

        Returns: Dict of downloaded file details, bool
                 Caller to check bool for success/failure detection
        """

        file_download_summary = {}
        
        # todo any other checks w+, r+ permissions (volume mounts ok?)
        if not os.path.isdir(download_path):
            print("Provided download_path does not exist")
            return file_download_summary, False

        #source_file = self.ctx.web.get_file_by_server_relative_path(input_path)
        source_file = self.get_file_by_path(input_path)
        if source_file is None:
            return file_download_summary, False

        local_file_name = os.path.join(download_path, os.path.basename(input_path))

        with open(local_file_name, "wb") as local_file:
            # todo add large file checks ?
            #source_file.download_session(local_file, print_download_progress).execute_query() #-> large files download
            source_file.download(local_file).execute_query()
            file_stats = os.stat(local_file_name)
            print("[Ok] file has been downloaded: {0},size:{1} bytes".format(local_file_name, file_stats.st_size))
            file_download_summary = {
                "file_name": local_file_name,
                "file_size_bytes": file_stats.st_size,
            }
            return file_download_summary, True

        return file_download_summary, False

    
    ################################### Internal functions #################################

    def _get_lib_field_internal(self, lib, field_ext_name) -> str:
        """
        gets field_internal_name from input field_ext_name

        Returns: field_internal_name if found, 
                 "" on error
        """
        fields = lib.fields.get().execute_query()
        for field in fields:
            #print("Field name Internal {0}".format(field.internal_name))
            #print("Field name Internal {0}".format(field.title))
            #print(field._properties)
            if field.title == field_ext_name:
                return field.internal_name

    
        print("invalid input:column not found in Sharepoint:", field_ext_name)

        return ""

    def _get_system_object_summary(self, input_type, item, tag_column_name_internal="") -> dict:

        # todo include new field with all properties for caller to pick ?

        if input_type == List:
            summary = {
                "site_url": self.site_url,
                "server_relative_url": item.properties['ServerRelativeUrl'],
                "time_last_modified": item.properties['TimeLastModified'].ctime(),
                "size_bytes": item.storage_metrics.total_size
            }

        if input_type == Folder:
            sm = item.expand(["StorageMetrics"]).get().execute_query()
            summary = {
                "site_url": self.site_url,
                "server_relative_url": item.serverRelativeUrl,
                "time_last_modified": item.properties['TimeLastModified'].ctime(),
                "size_bytes": sm.storage_metrics.total_file_stream_size
            }

        if input_type == File:
        
            sm = item.expand(["StorageMetrics"]).get().execute_query()

            summary = {
                "site_url": self.site_url,
                "server_relative_url": item.serverRelativeUrl,
                "time_last_modified": item.properties['TimeLastModified'].ctime(),
                "size_bytes": item.properties['Length']
            }
            # add tag if tag-column present
            if tag_column_name_internal:
                file_item = (
                    item.listItemAllFields.get().execute_query()
                )
                tag_value = file_item.properties.get(tag_column_name_internal)   
                if tag_value:    
                    summary["tag"] = tag_value
                else:
                    summary["tag"] = ""

        return summary
    
    # File properties do not provide - file size, server relative url. So use list as above.
    #def get_file_metadata(self, file_path):
    #    file_item = (
    #        self.ctx.web.get_file_by_server_relative_url(file_path)
    #        .listItemAllFields.get()
    #        .execute_query()
    #    )
    #    for k, v in file_item.properties.items():
    #        print("{0}: {1}".format(k, v))

    def _get_doclib_from_inputpath(self, input_path) -> str:
        parts = input_path.split('/', 1)
        return parts[0]

    def _get_folderpath_from_inputpath(self, input_path) -> str:
        parts = input_path.split('/', 1)
        doc_lib = parts[0]

        if len(parts) == 1:
            return ""

        if Documents_DocLibName in doc_lib:
            folder_path = Documents_SitePathName + "/" + parts[1]
            return folder_path # Shared Documents/somefolder
        else:
            return input_path # my-site-lib/somefolder

    def __init__(self, site_url=None, ctx=None) -> Any:

        if not site_url:
            print("invalid input:missing site_url")
        
        # instance variables
        self.site_url = site_url
        self.ctx = None
