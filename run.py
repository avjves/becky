import argparse
import sys

from becky_cli.becky.backups.backup_manager import BackupManager


def add_add_params(parser):
    subparsers = parser.add_subparsers(help='What to add', dest='action_add', required=True)
    location_parser = subparsers.add_parser('location')
    location_parser.add_argument('--path', required=True)

    param_parser = subparsers.add_parser('param')
    param_parser.add_argument('--type', help="provider or scanner", required=True)
    param_parser.add_argument('--key', required=True)
    param_parser.add_argument('--value', required=True)


def add_create_params(parser):
    parser.add_argument('--provider', required=True)
    parser.add_argument('--provider_param', action='append', nargs='*')
    parser.add_argument('--scanner', required=True)
    parser.add_argument('--scanner_param', action='append', nargs='*')

def add_cron_params(parser):
    parser.add_argument('--name', required=True)
    parser.add_argument('--enable', dest='cron_enabled', action='store_true')
    parser.add_argument('--disable', dest='cron_enabled', action='store_false') 
    parser.add_argument('--schedule')
    parser.set_defaults(cron_enabled=True)

def add_show_params(parser):
    parser.add_argument('--type', dest='show_type', help="What data to show. info / saves / diffs", required=True)

def add_delete_params(parser):
    subparsers = parser.add_subparsers(help="What to delete", dest='action_delete', required=True)
    diffs_parser = subparsers.add_parser('diffs')
    saves_parser = subparsers.add_parser('saves')

def add_files_params(parser):
    parser.add_argument('--path', help="Shows any backed up files at the given path.", required=True)
    parser.add_argument('--timestamp', help="Specify the timestamp to use.")

def add_restore_params(parser):
    parser.add_argument('--path', help="The file/folder (recursive) to be restored.", required=True)
    parser.add_argument('--restore_path', help="Location of restore folder.", required=True)
    parser.add_argument('--timestamp', help="Specify the timestamp to use.", required=True)


def main():

    parser = argparse.ArgumentParser(description='CLI backupper')
    subparsers = parser.add_subparsers(help='Action to take', dest='action', required=True)

    create_parser = subparsers.add_parser('create')
    add_create_params(create_parser)

    add_parser = subparsers.add_parser('add')
    add_add_params(add_parser)

    show_parser = subparsers.add_parser('show')
    add_show_params(show_parser)

    run_parser = subparsers.add_parser('run')

    delete_parser = subparsers.add_parser('delete')
    add_delete_params(delete_parser)

    files_parser = subparsers.add_parser('files')
    add_files_params(files_parser)

    restore_parser = subparsers.add_parser('restore')
    add_restore_params(restore_parser)

    list_parser = subparsers.add_parser('list')

    cron_parser = subparsers.add_parser('cron')
    add_cron_params(cron_parser)


    parser.add_argument('--name')

    args = parser.parse_args()
    vargs = vars(args)
    backup_manager = BackupManager()
    if args.action == 'create':
        backup_manager.create(vargs)
    elif args.action == 'add':
        if args.action_add == 'location':
            backup_manager.add_backup_location(vargs)
        elif args.action_add == 'param':
            backup_manager.add_parameter(vargs)
    elif args.action == 'show':
        backup_manager.show_backup(vargs)
    elif args.action == 'run':
        backup_manager.run_backup(vargs)
    elif args.action == 'delete':
        backup_manager.delete(vargs)
    elif args.action == 'files':
        backup_manager.show_files(vargs)
    elif args.action == 'restore':
        backup_manager.restore_files(vargs)
    elif args.action == 'list':
        backup_manager.list_backups(vargs)
    elif args.action == 'cron':
        if args.cron_enabled:
            if not args.schedule:
                parser.error('cron + enabled requires --schedule.')
        backup_manager.set_cron(vargs)

    
if __name__ == "__main__":
    main()
