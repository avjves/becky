from becky.databases.database import ShelveDatabase
from becky.backups.backup import Backup

class BackupManager:

    def __init__(self):
        self.db = ShelveDatabase('test.db')

    def add_backup_location(self, cli_args):
        """
        Adds a new local path to be backed up.
        """
        backup = self.get_backup(cli_args['name'])
        backup.add_backup_location(cli_args['path'])
        backup.save()
        print("backup location added.")

    def add_parameter(self, cli_args):
        """
        Used to add a provider/scanner parameter.
        """
        backup = self.get_backup(cli_args['name'])
        if cli_args['type'] == 'provider':
            backup.add_provider_param(cli_args['key'], cli_args['value'])
        elif cli_args['type'] == 'scanner':
            backup.add_scanner_param(cli_args['key'], cli_args['value'])
        else:
            print("Wrong type for param!")
            return
        backup.save()
        print("Param added successfully.")
            

    def get_backup(self, backup_name):
        """
        Gets a backup or creates a new one if none exists.
        """
        backup_data = self.db.get(backup_name)
        backup_db = self.db.get_backup_db(backup_name)
        backup = Backup(backup_db, backup_data)
        return backup
        
    def edit_backup(self, cli_args):
        """
        Adds a new backup.
        """
        backup = self.get_backup(cli_args['name'])
        print(backup)
        for key, value in cli_args.items():
            if key == 'action': continue
            print(key, value)

    def show_backup(self, cli_args):
        """
        Prints information about a backup.
        """
        backup_name = cli_args['name']
        backup = self.get_backup(backup_name)
        show_type = cli_args['show_type']
        if show_type == 'info':
            backup.print_details()
        elif show_type == 'saves':
            backup.print_saved_files()
        elif show_type == 'diffs':
            backup.print_diffs()

    def show_files(self, cli_args):
        """
        Shows files at a given path at the specified time.
        If no time was specified, showing the latest backup.
        """
        backup_name = cli_args['name']
        path = cli_args['path']
        timestamp = cli_args['timestamp']
        timestamp = int(timestamp) if timestamp else 10000000000000 #just a big number
        backup = self.get_backup(backup_name)
        backup.print_files_at_path(path, timestamp)

    def restore_files(self, cli_args):
        """
        Restores file/folder(recursive) at a given timestamp to a restore folder.
        """
        backup_name = cli_args['name']
        path = cli_args['path']
        restore_path = cli_args['restore_path']
        timestamp = int(cli_args['timestamp'])
        backup = self.get_backup(backup_name)
        backup.restore_files(path, restore_path, timestamp)


    def run_backup(self, cli_args):
        """
        Runs a backup.
        """
        backup_name = cli_args['name']
        backup = self.get_backup(backup_name)
        backup.run()

    def delete(self, cli_args):
        """
        Delete handler. Can be called to delete saved diffs or saved files.
        Deleting diffs/saves is more of a debugging feature.
        """
        backup_name = cli_args['name']
        backup = self.get_backup(backup_name)
        delete_action = cli_args['action_delete']
        if delete_action == 'diffs':
            backup.delete_diffs()
        elif delete_action == 'saves':
            backup.delete_saves()

    def create(self, cli_args):
        """
        Creates a new backup.
        """
        backup_name = cli_args['name']
        data = self.db.get(backup_name)
        if data:
            print("A backup has already been created with the given name.")
            return
        else:
            backup = Backup(self.db, cli_args)
            backup.save()
            print("Backup added.")

