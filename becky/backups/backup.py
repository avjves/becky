import natsort
import time

from becky.providers.local_provider import LocalProvider
from becky.scanners.local_differential_scanner import LocalDifferentialScanner

class Backup:

    def __init__(self, db, values):
        self.name = values.get('name')
        self.backup_locations = values.get('backup_locations', [])
        self.provider_params = values.get('provider_params', {})
        self.scanner_params = values.get('scanner_params', {})
        self.timestamps = values.get('timestamps', [])
        self.saved_keys = ['name', 'backup_locations', 'provider_params', 'scanner_params', 'timestamps']
        self.diffs = values.get('diffs', {})
        self.saved_files = values.get('saved_files', [])
        self.db = db

    def __str__(self):
        return f"Backup: {self.name}"

    def add_backup_location(self, backup_location):
        """
        Adds a new local path to be backed up.
        """
        self.backup_locations.append(backup_location)

    def add_provider_param(self, key, value):
        """
        Adds a new param for the provider.
        """
        self.provider_params[key] = value

    def add_scanner_param(self, key, value):
        """
        Adds a new param for the scanner.
        """
        self.scanner_params[key] = value

    def delete_diffs(self):
        """
        Deletes any saved diffs from this backup.
        Forces the backupper to re-backup everything again.
        """
        self.db.save('diffs', {})

    def delete_saves(self):
        """
        Deletes list of saved files.
        This will disable the ability to restore any backuped file
        without re-verifying the files.
        """
        self.db.save('saved_files', [])

    def print_details(self):
        """
        Prints all details about the current model.
        """
        for key in self.saved_keys:
            print(f"{key} -- {getattr(self, key)}")

    def print_saved_files(self):
        """
        Prints the saved files for this current model.
        """
        self.saved_files.sort(key=lambda x: x['name'])
        for saved_file in self.saved_files:
            if 'path' not in saved_file: continue
            print(f"{saved_file['name']} @ {saved_file['date']} --> {saved_file['path']}")

    def print_diffs(self):
        """
        Prints all available diffs.
        """
        diffs = []
        for file_name, diff_info in self.diffs.items():
            diffs.append([file_name, diff_info])
        diffs.sort(key=lambda x: x[0])
        for (file_name, diff_info) in diffs:
            print(f"{file_name} --> previous: {diff_info['previous']}, current: {diff_info['current']}")

    def run(self):
        """
        Runs a backup.
        """
        current_timestamp = int(time.time())
        scanner = self._get_scanner()
        provider = self._get_provider()
        new_files, diffs = scanner.scan_files()
        saved_files = provider.backup_files(new_files, current_timestamp)
        print(f"Backed up {len(saved_files)} new files.")
        all_saved_files = self.saved_files + saved_files

        self.db.save('diffs', diffs)
        self.db.save('saved_files', all_saved_files)
        self.db.add('timestamps', [current_timestamp], default=[])

    def save(self):
        """
        Saves the current backup data to the DB.
        """
        for key in self.saved_keys:
            self.db.save(key, getattr(self, key))

    def _get_provider(self):
        provider = LocalProvider(parameters=self.provider_params, saved_files=self.saved_files)
        return provider

    def _get_scanner(self):
        scanner = LocalDifferentialScanner(parameters=self.scanner_params, backup_locations=self.backup_locations, diffs=self.diffs)
        return scanner

