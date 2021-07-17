import getpass
from crontab import CronTab

from becky_cli.becky.databases.database import ShelveDatabase
from becky_cli.becky.backups.backup import Backup

class BackupManager:

    def __init__(self):
        current_user = getpass.getuser()
        self.db = ShelveDatabase(f"/home/{current_user}/.becky.db")

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
        elif cli_args['type'] == 'backup':
            backup.add_param(cli_args['key'], cli_args['value'])
        else:
            print("Wrong type for param!")
            return
        backup.save()
        print(f"Param {cli_args['key']} added successfully.")
            

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

    def list_backups(self, cli_args):
        """
        List all current backups.
        """
        for backup_i, backup_name in enumerate(self.db.keys()):
            print(f"Backup {backup_i}: {backup_name}")

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
            backup.print_saved_files(all_files=True)
        elif show_type == 'diffs':
            backup.print_diffs()
        elif show_type == 'files':
            backup.print_saved_files(all_files=False)

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
        elif delete_action == 'backup':
            self.db.delete(backup_name)
        else:
            raise NotImplementedError

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
            backup_db = self.db.get_backup_db(backup_name)
            backup = Backup(backup_db, cli_args)
            backup.save()
            print(f"Backup added with name {backup_name}.")
            return backup

    def set_cron(self, cli_args):
        """
        Either enables or disables a cronjob that runs the backup given the schedule.
        """
        backup_name = cli_args['name']
        cron_enabled = cli_args['cron_enabled']
        if cron_enabled:
            cron = CronTab(user=True)
            cron.remove_all(comment=f'Becky - {backup_name}') # Remove any previous schedule set for this job
            cron_schedule = cli_args['schedule']
            job = cron.new(command=f"becky --name '{backup_name}' run", comment=f"Becky - {backup_name}")
            job.setall(cron_schedule)
            job.enable()
            cron.write()
            print("Cron enabled.")
        else: # delete
            cron = CronTab(user=True)
            cron.remove_all(comment=f'Becky - {backup_name}') 
            cron.write()
            print("Cron disabled.")
        

