import argparse
import sys

from becky.backups.backup_manager import BackupManager


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

def add_show_params(parser):
    parser.add_argument('--type', dest='show_type', help="What data to show. info / saves / diffs", required=True)

def add_delete_params(parser):
    subparsers = parser.add_subparsers(help="What to delete", dest='action_delete', required=True)
    diffs_parser = subparsers.add_parser('diffs')
    saves_parser = subparsers.add_parser('saves')


if __name__ == "__main__":

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

    parser.add_argument('--name', required=True)

    args = parser.parse_args()
    backup_manager = BackupManager()
    if args.action == 'create':
        backup_manager.create(args)
    elif args.action == 'add':
        if args.action_add == 'location':
            backup_manager.add_backup_location(args)
        elif args.action_add == 'param':
            backup_manager.add_parameter(args)
    elif args.action == 'show':
        backup_manager.show_backup(args)
    elif args.action == 'run':
        backup_manager.run_backup(args)
    elif args.action == 'delete':
        backup_manager.delete(args)
    
        

