import json

from tempfile import TemporaryDirectory
from unittest import TestCase
from collections import namedtuple

from becky.backups.backup_manager import BackupManager
from tests.providers import generic_tests

class LocalProviderTests(TestCase):
    def setUp(self):
        self.backup_manager = BackupManager()
        pass

    def tearDown(self):
        self.backup_manager.delete({'name': 'test_backup', 'action_delete': 'backup'})
        pass

    def test_single_folder(self):
        backup_model = self.backup_manager.create({'name': 'test_backup'})
        backup_folder = TemporaryDirectory()
        backup_model.add_provider_param(key='output_path', value=backup_folder.name)
        generic_tests._test_backup_model_single_folder(self, backup_model)
        backup_folder.cleanup()

    def test_single_file(self):
        backup_model = self.backup_manager.create({'name': 'test_backup'})
        backup_folder = TemporaryDirectory()
        backup_model.add_provider_param(key='output_path', value=backup_folder.name)
        generic_tests._test_backup_model_single_file(self, backup_model)
        backup_folder.cleanup()

    def test_single_differential_file(self):
        backup_model = self.backup_manager.create({'name': 'test_backup'})
        backup_folder = TemporaryDirectory()
        backup_model.add_provider_param(key='output_path', value=backup_folder.name)
        generic_tests._test_backup_model_single_differential_file(self, backup_model)
        backup_folder.cleanup()

    def test_single_differential_file_wrong_timestamp(self):
        backup_model = self.backup_manager.create({'name': 'test_backup'})
        backup_folder = TemporaryDirectory()
        backup_model.add_provider_param(key='output_path', value=backup_folder.name)
        generic_tests._test_backup_model_single_differential_file_wrong_timestamp(self, backup_model)
        backup_folder.cleanup()

    # def test_verify_files(self):
        # backup_model = self.backup_manager.create({'name': 'test_backup'})
        # backup_folder = TemporaryDirectory()
        # backup_model.add_provider_param(key='output_path', value=backup_folder.name)
        # generic_tests._test_backup_model_file_verification(self, backup_model)
        # backup_folder.cleanup()


