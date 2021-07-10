import os
import uuid
import time
from shutil import copyfile

class LocalProvider:

    def __init__(self, parameters, saved_files):
        self.parameters = parameters
        self.saved_files = saved_files

    def backup_files(self, new_files, current_timestamp):
        """
        Backups the new files.
        """
        copy_path = self._get_parameter('output_path')
        if not os.path.exists(copy_path):
            os.makedirs(copy_path)
        saved_files = []
        for file_in_index, file_in in enumerate(new_files):
            if os.path.isdir(file_in): 
                saved_files.append({'name': file_in, 'type': 'directory', 'date': current_timestamp})
                continue
            else:
                file_out = self._generate_output_path(copy_path)
                self._copy_file(file_in, file_out)
                saved_files.append({'name': file_in, 'path': file_out, 'type': 'file', 'date': current_timestamp})
        return saved_files

    def _generate_output_path(self, copy_path):
        new_file_name = str(uuid.uuid4())
        file_out = os.path.join(copy_path, new_file_name)
        return file_out

    def _copy_file(self, file_in, file_out):
        copyfile(file_in, file_out)

    def _get_parameter(self, key):
        return self.parameters[key]

