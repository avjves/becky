import json
import os

from tempfile import TemporaryDirectory
from unittest import TestCase

from becky.backups.backup_manager import BackupManager
from tests.providers import generic_tests

class S3ProviderTests(TestCase):
    def setUp(self):
        self.backup_manager = BackupManager()
        # self.backup_manager.delete({'name': 'test_backup', 'action_delete': 'backup'})
        self.backup_model = self.backup_manager.create({'name': 'test_backup', 'provider': 's3'})

        config = self._get_s3_configs() 
        self.backup_model.add_provider_param(key='access_key', value=config['access_key'])
        self.backup_model.add_provider_param(key='secret_key', value=config['secret_key'])
        self.backup_model.add_provider_param(key='host', value=config['host_base'])
        self.backup_model.add_provider_param(key='host_bucket', value=config['host_bucket'])
        self.backup_model.add_provider_param(key='bucket_name', value=config['bucket_name'])

    def tearDown(self):
        self.backup_manager.delete({'name': 'test_backup', 'action_delete': 'backup'})

    def test_single_folder(self):
        backup_folder = TemporaryDirectory()
        generic_tests._test_backup_model_single_folder(self, self.backup_model)
        backup_folder.cleanup()

    def test_single_file(self):
        backup_folder = TemporaryDirectory()
        generic_tests._test_backup_model_single_file(self, self.backup_model)
        backup_folder.cleanup()

    def test_single_differential_file(self):
        backup_folder = TemporaryDirectory()
        generic_tests._test_backup_model_single_differential_file(self, self.backup_model)
        backup_folder.cleanup()

    def test_single_differential_file_wrong_timestamp(self):
        backup_folder = TemporaryDirectory()
        generic_tests._test_backup_model_single_differential_file_wrong_timestamp(self, self.backup_model)
        backup_folder.cleanup()

    def _get_s3_configs(self):
        try:
            config = {}
            home = os.path.expanduser('~')
            config_file = open("{}/.s3cfg".format(home), "r")
            config_lines = config_file.read().split('\n')
            for line in config_lines:
                splits = line.split("=")
                if len(splits) == 2:
                    config[splits[0].strip()] = splits[1].strip()
            config_file.close()
            return config
        except Exception as e:
            raise Exception('For S3 tests to work, there has to be a valid .s3cfg file in the root of the current user')

