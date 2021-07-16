import json

from tempfile import TemporaryDirectory
from unittest import TestCase

from becky.backups.backup_manager import BackupManager
from tests.providers import generic_tests


class RemoteProviderTests(TestCase):
    def setUp(self):
        self.backup_manager = BackupManager()
        self.backup_model = self.backup_manager.create({'name': 'test_backup', 'provider': 'remote'})

    def tearDown(self):
        self.backup_manager.delete({'name': 'test_backup', 'action_delete': 'backup'})

    def test_single_folder(self):
        backup_folder = TemporaryDirectory()
        self.backup_model.add_provider_param(key='remote_path', value=backup_folder.name)
        self.backup_model.add_provider_param(key='remote_addr', value='localhost')
        self.backup_model.add_provider_param(key='ssh_id_path', value='~/.ssh/id_rsa')
        generic_tests._test_backup_model_single_folder(self, self.backup_model)
        backup_folder.cleanup()

    def test_single_file(self):
        backup_folder = TemporaryDirectory()
        self.backup_model.add_provider_param(key='remote_path', value=backup_folder.name)
        self.backup_model.add_provider_param(key='remote_addr', value='localhost')
        self.backup_model.add_provider_param(key='ssh_id_path', value='~/.ssh/id_rsa')
        generic_tests._test_backup_model_single_file(self, self.backup_model)
        backup_folder.cleanup()

    def test_single_differential_file(self):
        backup_folder = TemporaryDirectory()
        self.backup_model.add_provider_param(key='remote_path', value=backup_folder.name)
        self.backup_model.add_provider_param(key='remote_addr', value='localhost')
        self.backup_model.add_provider_param(key='ssh_id_path', value='~/.ssh/id_rsa')
        generic_tests._test_backup_model_single_differential_file(self, self.backup_model)
        backup_folder.cleanup()

    def test_single_differential_file_wrong_timestamp(self):
        backup_folder = TemporaryDirectory()
        self.backup_model.add_provider_param(key='remote_path', value=backup_folder.name)
        self.backup_model.add_provider_param(key='remote_addr', value='localhost')
        self.backup_model.add_provider_param(key='ssh_id_path', value='~/.ssh/id_rsa')
        generic_tests._test_backup_model_single_differential_file_wrong_timestamp(self, self.backup_model)
        backup_folder.cleanup()
