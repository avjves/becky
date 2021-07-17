import os
import glob
import shelve
import tempfile
import uuid
from shutil import copyfile
from becky_cli.becky.utils.utils import remove_prefix, join_file_path, path_to_folders

"""
A remote backup provider that can backup files from the local system
to a remote machine.
"""
class RemoteProvider:
    
    def __init__(self, parameters, saved_files):
        self.parameters = parameters
        self.saved_files = saved_files

    def backup_files(self, new_files, current_timestamp):
        """
        Receives a list of files to be backed up. 
        """
        new_files.sort(key=lambda x: x) # Sort, so folders will be created before any files are copied in.
        remote_addr = self._get_parameter('remote_addr')
        remote_copy_path = self._get_parameter('remote_path')
        ssh_identity_path = self._get_parameter('ssh_id_path')
        saved_files = []
        for file_in_index, file_in in enumerate(new_files):
            directory_path = file_in.rsplit("/", 1)[0]
            if not directory_path: directory_path = '/'
            file_out = self._generate_output_path(remote_copy_path)
            if os.path.isdir(file_in): 
                saved_files.append({'name': file_in, 'directory': directory_path, 'path': file_out, 'type': 'directory', 'date': current_timestamp})
            else:
                saved_files.append({'name': file_in, 'directory': directory_path, 'path': file_out, 'type': 'file', 'date': current_timestamp})
        copied_files = self._copy_files(saved_files, remote_addr, remote_copy_path, ssh_identity_path)
        return copied_files

    def restore_files(self, files_to_restore, restore_path):
        """
        Restores selected files from the backups to the restore folder.
        """
        files_to_restore.sort(key=lambda x: x['name']) # Sort, so folders will be created before any files are copied in.
        remote_addr = self._get_parameter('remote_addr')
        remote_copy_path = self._get_parameter('remote_path')
        ssh_identity_path = self._get_parameter('ssh_id_path')
        return self._copy_remote_files(files_to_restore, restore_path, remote_addr, remote_copy_path, ssh_identity_path)

    # def verify_files(self):
        # """
        # Verifies that the the internal state of BackupItems matches the remote files.
        # Returns true if eveything is ok, else returns False.
        # """
        # backup_items = self.backup_model.get_all_backup_items()
        # remote_copy_path = self._get_parameter('remote_path')
        # remote_paths = [join_file_path(remote_copy_path, backup_item.path) for backup_item in backup_items]
        # remote_checksums = self._get_remote_checksums(remote_paths)
        # mismatched_files = set()
        # for backup_item_i, backup_item in enumerate(backup_items):
            # if backup_item.checksum != remote_checksums.get(join_file_path(remote_copy_path, backup_item.path), '0'):
                # mismatched_files.add(backup_item.path)
        # if len(mismatched_files) > 0:
            # raise exceptions.DataVerificationFailedException(fail_count=len(mismatched_files))

    def _get_parameter(self, key):
        """
        Returns the parameter with the given key from the backup parameters.
        """
        return self.parameters[key]

    def _get_remote_checksums(self, remote_paths):
        """
        Runs checksums on the remote server on the given paths.
        Process:
            1. Copies the list of files to run checksum to the server.
            2. Runs md5sum on each file on the remote server and save results to tmp.
            3. Copy back the results.
        TODO: Maybe use an actual SSH client to do this without any file saving.
        """
        remote_addr = self._get_parameter('remote_addr')
        remote_copy_path = self._get_parameter('remote_path')
        ssh_identity_path = self._get_parameter('ssh_id_path')

        remote_paths_file = '/tmp/{}'.format(str(uuid.uuid4()))
        remote_checksums_file = '/tmp/{}'.format(str(uuid.uuid4()))
        open(remote_paths_file, "w").write('\n'.join(remote_paths) + '\n')
        command = 'scp -i {} {} {}:{} > /dev/null'.format(ssh_identity_path, remote_paths_file, remote_addr, remote_paths_file)
        os.system(command)
        command = "ssh -i {} {} 'while read line; do md5sum $line; done < {} > {} 2>/dev/null' > /dev/null".format(ssh_identity_path, remote_addr, remote_paths_file, remote_checksums_file)
        os.system(command)
        command = 'scp -i {} {}:{} {} > /dev/null'.format(ssh_identity_path, remote_addr, remote_checksums_file, remote_checksums_file)
        os.system(command)
        checksum_lines = open(remote_checksums_file, "r").read().split('\n')
        checksums = {}
        checksum_lines = [l.strip() for l in checksum_lines if l.strip()]
        for checksum_i, checksum_line in enumerate(checksum_lines):
            checksum = checksum_line.split(" ")[0].strip()
            file_name = checksum_line.split(" ", 1)[1].strip()
            checksums[file_name] = checksum
        return checksums

    
    def _copy_files(self, files, remote_addr, remote_path, ssh_identity_path):
        """
        Copies a list of files from the current server to the remote server.
        Uses rsync to copy the files efficiently.
        """
        paths = [f['name'] for f in files if f['type'] == 'file']
        for file in files:
            if file['type'] == 'directory': continue
            command = 'rsync -e "ssh -i {}" {} {}:{}'.format(ssh_identity_path, file['name'], remote_addr, file['path'])
            os.system(command)
        # files_file = tempfile.NamedTemporaryFile(mode="w")
        # files_file.write('\n'.join(paths))
        # files_file.flush()
        # print(paths[0])
        # command = 'rsync -e "ssh -i {}" --files-from {} / {}:{}'.format(ssh_identity_path, files_file.name, remote_addr, remote_path)
        # os.system(command)
        # files_file.close()
        return files

    def _copy_remote_files(self, files, restore_path, remote_addr, remote_path, ssh_identity_path):
        """
        Copies a list of files from the remote server to the current server in the specified restore folder.
        Uses rsync to copy the files efficiently.
        """
        files_restored = []
        files_skipped = []
        for file in files:
            if file['type'] == 'directory':
                os.makedirs(join_file_path(restore_path, file['name']))
                files_restored.append(file)
            else:
                command = 'scp -i {} {}:{} {}'.format(ssh_identity_path, remote_addr, file['path'], join_file_path(restore_path, file['name']))
                files_restored.append(file)
                os.system(command)
        return files_restored, files_skipped
        # folders = [join_file_path(restore_path, f['name']) for f in files if f['type'] == 'directory']
        # for f in folders:
            # os.makedirs(f)
        # file_paths = [f['path'] for f in files]
        # files_file = tempfile.NamedTemporaryFile(mode="w")
        # files_file.write('\n'.join(file_paths))
        # files_file.flush()
        # print("restore_path", restore_path)
        # print("remote_path", remote_path)
        # import pdb;pdb.set_trace()
        # command = 'rsync -e "ssh -i {}" --files-from {} {}:{} {}'.format(ssh_identity_path, files_file.name, remote_addr, remote_path, restore_path)
        # os.system(command)
        # files_file.close()

    def _generate_output_path(self, copy_path):
        """
        Generates an output path by concatenating copy_path and file_in.
        """
        file_name = str(uuid.uuid4())
        file_out =  join_file_path(copy_path, file_name)
        # return file_name
        return file_out
