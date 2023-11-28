from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from robot.api import logger
from robot.api.deco import library, keyword


@library
class azure_data_lake_storage_library:
    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.client = None
        self.credential = None

    @keyword
    def connect_to_ADLS(self, storage_account_name):
        self.credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
        self.client = DataLakeServiceClient('https://{}.dfs.core.windows.net/'.format(storage_account_name),
                                            credential=self.credential)

    @keyword
    def get_content_of_directory(self, file_system, path):
        """
        Keyword that returns the files, directories and subdirectories of a directory as a list.

        ``file_system`` Name of the Blob Container

        ``path`` Returns every file, directory and subdirectory located in this path. If left empty, it returns
        everything from the root level of the file system
        """
        try:
            file_system_client = self.client.get_file_system_client(file_system=file_system)
            directory_content = file_system_client.get_paths(path=path)
            list_of_content = []
            for c in directory_content:
                list_of_content.append(c.name)
            return list_of_content
        except Exception as e:
            logger.error("something went wrong, exception: {}".format(e))

    @keyword
    def delete_directory_in_ADLS(self, file_system, directory):
        """
        Keyword that deletes the given directory and everything in it.

        ``file_system`` Name of the Blob Container

        ``directory`` path of the directory that you would like to delete
        """
        try:
            file_system_client = self.client.get_file_system_client(file_system=file_system)
            file_system_client.delete_directory(directory)
        except Exception as e:
            print(e)

    @keyword
    def delete_file_in_ADLS(self, file_system, file):
        """
        Keyword that deletes the file.

        ``file_system`` Name of the Blob Container

        ``file`` Complete path of the file that you would like to delete
        """
        try:
            file_system_client = self.client.get_file_system_client(file_system)
            file_system_client.delete_file(file)
        except Exception as e:
            print(e)

    @keyword
    def rename_directory_in_ADLS(self, file_system, old_directory, new_directory):
        """
        Keyword that renames a directory.

        ``file_system`` Name of the Blob Container

        ``old_directory`` Name of the directory to be renamed. This needs to include the whole path except the filesystem

        ``new_directory`` Desired name of the directory. This needs to include the whole path except the filesystem
        """
        try:
            file_system_client = self.client.get_file_system_client(file_system)
            directory_client = file_system_client.get_directory_client(old_directory)

            directory_client.rename_directory(directory_client.file_system_name + '/' + new_directory)
        except Exception as e:
            print(e)

    @keyword
    def rename_file_in_ADLS(self, file_system, old_file, new_file):
        """
        Keyword that renames a directory.

        ``file_system`` Name of the Blob Container

        ``old_file`` Name of the file to be renamed. This needs to include the whole path except the filesystem

        ``new_file`` Desired name of the file. This needs to include the whole path except the filesystem
        """
        try:
            file_system_client = self.client.get_file_system_client(file_system)
            file_client = file_system_client.get_file_client(old_file)
            file_client.rename_file(file_client.file_system_name + '/' + new_file)
        except Exception as e:
            print(e)
