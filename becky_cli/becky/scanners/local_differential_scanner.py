import os
from becky_cli.becky.utils.utils import path_to_folders

class LocalDifferentialScanner:

    def __init__(self, parameters, backup_locations, diffs):
        self.parameters = parameters
        self.backup_locations = backup_locations
        self.diffs = diffs

    def scan_files(self):
        scanned_files = []
        for backup_location_i, backup_location in enumerate(self.backup_locations):
            scanned_files += self._scan_local_files(backup_location)
        scanned_files = list(set(scanned_files))
        self._update_differential_information(scanned_files)
        return self._compare_scanned_files(scanned_files), self.diffs

    
    def _compare_scanned_files(self, scanned_files):
        new_files = []
        for i, scanned_file in enumerate(scanned_files):
            diff = self.diffs[scanned_file]
            if diff['previous'] == None: # First time seeing this file
                new_files.append(scanned_file)
            else:
                if diff['previous'] != diff['current']:
                    new_files.append(scanned_file)
        return new_files


    def _update_differential_information(self, scanned_files):
        for f in scanned_files:
            file_diff = self.diffs.get(f, {'previous': None, 'current': None})
            current_modified = int(os.path.getmtime(f))
            file_diff['previous'] = file_diff['current']
            file_diff['current'] = current_modified
            self.diffs[f] = file_diff
            

    def _scan_local_files(self, location):
        if not os.path.exists(location):
            return []
        if os.path.isfile(location):
            return path_to_folders(location)
        else:
            scanned_files = path_to_folders(location) + self._walk_folders(location)
        return scanned_files


    def _walk_folders(self, location):
        files = set()
        for root, directories, dir_files in os.walk(location):
            files.add(root)
            for f in dir_files:
                files.add(os.path.join(root, f))
        return list(files)
