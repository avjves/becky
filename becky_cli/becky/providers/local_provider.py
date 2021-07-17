import os
import uuid
import time
from shutil import copyfile
from natsort import natsorted
from becky_cli.becky.utils.utils import join_file_path

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
            directory_path = file_in.rsplit("/", 1)[0]
            if not directory_path: directory_path = '/'
            file_out = self._generate_output_path(copy_path)
            if os.path.isdir(file_in): 
                saved_files.append({'name': file_in, 'directory': directory_path, 'path': file_out, 'type': 'directory', 'date': current_timestamp})
                continue
            else:
                self._copy_file(file_in, file_out)
                saved_files.append({'name': file_in, 'directory': directory_path, 'path': file_out, 'type': 'file', 'date': current_timestamp})
        return saved_files


    def restore_files(self, files_to_restore, restore_path):
        if not os.path.exists(restore_path): os.makedirs(restore_path)
        files_to_restore = natsorted(files_to_restore, key=lambda x: x['name'])
        files_restored = []
        files_skipped = []
        for f in files_to_restore:
            try:
                file_out = join_file_path(restore_path, f['name'])
                if f['type'] == 'directory':
                    os.mkdir(file_out)
                else:
                    file_in = f['path']
                    if os.path.exists(file_out): 
                        files_skipped.append(f)
                        continue
                    self._copy_file(file_in, file_out)
                files_restored.append(f)
            except:
                files_skipped.append(f)
        return files_restored, files_skipped


    def _generate_output_path(self, copy_path):
        new_file_name = str(uuid.uuid4())
        file_out = os.path.join(copy_path, new_file_name)
        return file_out

    def _copy_file(self, file_in, file_out):
        copyfile(file_in, file_out)

    def _get_parameter(self, key):
        return self.parameters[key]


