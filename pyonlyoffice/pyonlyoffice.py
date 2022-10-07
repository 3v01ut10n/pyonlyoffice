import time
import json

import requests


class PyOnlyOffice:
    username = ""
    password = ""
    baseurl = ""
    token = ""
    auth = ""

    def __init__(self, baseurl: str, username: str, password: str):
        self.username = username
        self.password = password
        self.baseurl = baseurl
        self.authenticate(username, password, baseurl)

    def authenticate(self, username: str, password: str, baseurl: str):
        """
        :param username: User name or email.
        :param password: Password.
        :param baseurl: Own OnlyOffice link (https://example.com/).

        https://api.onlyoffice.com/portals/method/authentication/post/api/2.0/authentication
        """
        self.username = username
        self.password = password
        self.baseurl = baseurl
        r = requests.post(
            f"{baseurl}/api/2.0/authentication",
            data={"username": username, "password": password}
        )
        j = json.loads(r.text)
        self.token = j["response"]["token"]
        self.auth = {"Authorization": self.token}

    def get_fileops(self):
        """
        :return: A list of all the active operations.

        https://api.onlyoffice.com/portals/method/files/get/api/2.0/files/fileops
        """
        finished = True
        r = requests.get(
            f"{self.baseurl}/api/2.0/files/fileops",
            headers=self.auth
        )
        j = json.loads(r.text)
        for item in j["response"]:
            if not (item["finished"]):
                finished = False

        return finished, j

    def download(self, file_ids: list, filename: str):
        """
        Starts the download process of files and folders with the IDs specified in the request.

        :param file_ids: List of file IDs.
        :param filename:
        :return:

        https://api.onlyoffice.com/portals/method/files/put/api/2.0/files/fileops/bulkdownload
        """
        r1 = requests.put(
            f"{self.baseurl}/api/2.0/files/fileops/bulkdownload",
            data={"fileIds": file_ids},
            headers=self.auth,
        )

        # Wait for operation to finish, up to 120 s.
        i = 0
        while (i < 60) and not (self.get_fileops()[0]):
            time.sleep(2)
            print("Sleep %s" % i)
            i += 1

        if not (self.get_fileops()[0]):
            ok = False
        else:
            r = requests.get(f"{self.baseurl}/Products/Files/HttpHandlers/filehandler.ashx?action=bulk&ext=.zip",
                             headers=self.auth)
            open(filename, "wb").write(r.content)
            ok = True

        return ok

    def download_file(self, file_id: int, filename=None):
        """
        :param file_id: File ID.
        :param filename: Filename to save. By default, the file name is taken from the server.
        """
        r = requests.get(
            f"{self.baseurl}/Products/Files/HttpHandlers/filehandler.ashx?action=download&fileid={file_id}",
            headers=self.auth,
        )

        if filename:
            open(filename, "wb").write(r.content)
        else:
            open(self.get_filename(file_id), "wb").write(r.content)

    def upload(self, folder_id: int, filename: str):
        """
        Uploads a file specified in the request to the selected folder by single file uploading
        or standart multipart/form-data method.

        :param folder_id: Folder ID.
        :param filename:
        :return:

        https://api.onlyoffice.com/portals/method/files/post/api/2.0/files/%7bfolderid%7d/upload
        """
        with open(filename, "rb") as payload:
            # TODO: Support other file types with content-type.
            headers = {
                "content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "Content-Disposition": f"inline; filename={filename}",
                "Authorization": self.token
            }
            r = requests.post(
                f"{self.baseurl}/api/2.0/files/{folder_id}/upload",
                data=payload, verify=False, headers=headers
            )
            j = json.loads(r.text)

            return j

    def get_file_list(self, folder_id: int):
        """
        Returns the detailed list of files and folders located in the folder with the ID specified in the request.

        :param folder_id:
        :return:

        https://api.onlyoffice.com/portals/method/files/get/api/2.0/files/%7bfolderid%7d
        """
        r = requests.get(f"{self.baseurl}/api/2.0/files/{folder_id}", headers=self.auth)
        j = json.loads(r.text)
        files = j["response"]["files"]
        file_list = []
        for f in files:
            file_list.append(f["id"])

        return file_list, j

    def delete_file(self, file_id: int, delete_after: bool, immediately: bool):
        """
        Deletes a file with the ID specified in the request.

        :param file_id:
        :param delete_after:
        :param immediately:
        :return:

        https://api.onlyoffice.com/portals/method/files/delete/api/2.0/files/file/%7bfileid%7d
        """
        headers = {"deleteAfter": delete_after, "immediately": immediately,
                   "Authorization": self.token}
        r = requests.delete(f"{self.baseurl}/api/2.0/files/file/{file_id}", headers=headers)
        j = json.loads(r.text)

        return j

    def terminate(self):
        """
        Finishes all the active operations.

        https://api.onlyoffice.com/portals/method/files/put/api/2.0/files/fileops/terminate
        """
        r = requests.put(f"{self.baseurl}/api/2.0/files/fileops/terminate", headers=self.auth)
        j = json.loads(r.text)

        return j

    def get_the_file_information(self, file_id: int):
        """
        Returns the detailed information about a file with the ID specified in the request.

        :param file_id: File ID.
        :return:

        https://api.onlyoffice.com/portals/method/files/get/api/2.0/files/file/%7bfileid%7d
        """
        r = requests.get(f"{self.baseurl}/api/2.0/files/file/{file_id}", headers=self.auth)
        j = json.loads(r.text)

        return j

    def get_filename(self, file_id: int):
        """
        Return filename.

        :param file_id: File ID.
        """
        return self.get_the_file_information(file_id)["response"]["title"]

    def update_file_content(self, file_id: int, filename):
        """
        Updates the content of a file with the ID specified in the request.

        :param file_id: File ID.
        :param filename: Filename.

        https://api.onlyoffice.com/portals/method/files/put/api/2.0/files/%7bfileid%7d/update
        """
        r = requests.put(
            f"{self.baseurl}/api/2.0/files/{file_id}/update",
            headers=self.auth,
            files={"file": open(filename, "rb")},
        )
        j = json.loads(r.text)

        return j
