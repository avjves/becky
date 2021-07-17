import os
import glob
import uuid
import subprocess
from tempfile import TemporaryDirectory
from shutil import copyfile

from becky_cli.becky.utils.utils import remove_prefix, join_file_path, path_to_folders

"""
A provider that can backup to and from any S3 compatible object storage server in a
differential fashion.
"""
class S3Provider:
    
    def __init__(self, parameters, saved_files):
        self.parameters = parameters
        self.saved_files = saved_files

    def backup_files(self, new_files, current_timestamp):
        """
        Receives a list of files to be backed up. 
        TODO: Use rsync or something a bit more efficient than
        going through files one at a time.
        """
        bucket_name = self._get_parameter('bucket_name')
        saved_files = []
        for file_in_index, file_in in enumerate(new_files):
            directory_path = file_in.rsplit("/", 1)[0]
            if not directory_path: directory_path = '/'
            file_out = self._generate_output_path(bucket_name)
            if os.path.isdir(file_in): 
                saved_file = {'name': file_in, 'directory': directory_path, 'path': file_out, 'type': 'directory', 'date': current_timestamp}
            else:
                saved_file = {'name': file_in, 'directory': directory_path, 'path': file_out, 'type': 'file', 'date': current_timestamp}
            self._copy_file(saved_file)
            saved_files.append(saved_file)
        return saved_files

    def restore_files(self, files_to_restore, restore_path, **kwargs):
        """
        Restores selected files from the backups to the restore folder.
        """
        restored_files = []
        skipped_files = []
        for selection_file in files_to_restore:
            restored_file = join_file_path(restore_path, selection_file['name'])
            self._restore_file(selection_file, restored_file)
            restored_files.append(selection_file)
        return restored_files, skipped_files


    # def verify_files(self):
        # """
        # Verifies that the the internal state of BackupItems matches the copied files on the s3 storage.
        # """
        # current_items = self.backup_model.get_all_backup_items()
        # bucket_name = self._get_parameter('bucket_name')
        
        # mismatched_files = set()
        # for backup_item in current_items:
            # if backup_item.file_type == 'directory': continue
            # backup_path = self._generate_output_path(backup_item, bucket_name)
            # result, err = self._run_command(['ls', '--list-md5', backup_path.path])
            # matched = False
            # if result.strip():
               # splits = result.strip().split()
               # if backup_item.checksum == splits[3]:
                   # matched = True
            # if not matched:
                # mismatched_files.add(backup_item.path)
        # if len(mismatched_files) > 0:
            # self._log('INFO', "Found {} files that didn't pass the verification process.".format(len(mismatched_files)))
            # raise exceptions.DataVerificationFailedException(fail_count=len(mismatched_files))
        # self._log('INFO', "Verified {} files.".format(len(current_items) - len(mismatched_files)))    


        
    def _copy_file(self, f):
        """
        Receives a list of files that should be copied to the s3 object storage server.
        S3 doesn't have a concept of a directory, so we only have to copy the normal files themselves.
        """
        bucket_name = self._get_parameter('bucket_name')
        if f['type'] == 'directory': return
        result, err = self._run_command(['put', f['name'], f['path']])

    def _restore_file(self, backup_file, restored_file):
        """
        Restores a single file from the S3 storage to the given path.
        """
        if backup_file['type'] == 'directory':
            if not os.path.exists(restored_file):
                os.makedirs(restored_file)
        else:
            result, err = self._run_command(['get', backup_file['path'], restored_file])

    def _run_command(self, commands):
        """
        Given the command to run, runs it on the command line through s3cmd to the configured bucket.
        Returns whatever the command returns.
        """
        access_key = self._get_parameter('access_key')
        secret_key = self._get_parameter('secret_key')
        host = self._get_parameter('host')
        host_bucket = self._get_parameter('host_bucket')
        result = subprocess.run(['s3cmd'] + commands + ['--access_key', access_key, '--secret_key', secret_key, '--host', host, '--host-bucket', host_bucket], stdout=subprocess.PIPE)
        stdout = result.stdout.decode() if result.stdout else None
        stderr = result.stderr.decode() if result.stderr else None
        return stdout, stderr

    def _generate_output_path(self, bucket_name):
        """
        Generates an output path by concatenating copy_path and file_in.
        """
        file_name = str(uuid.uuid4())
        file_out = join_file_path('s3://', bucket_name, file_name)
        return file_out

    def _get_parameter(self, key):
        """
        Returns the parameter with the given key from the backup parameters.
        """
        return self.parameters[key]

