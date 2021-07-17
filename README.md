# Becky

Becky is a command-line based backup software.
It can periodically scan through your files, find any changes and subsequently backup the new files to a remote location.
Only works on Linux.

## Providers
Becky implements different providers that allow it to backup the data to many different locations or with different protocols.
Right now, Becky supports these providers:
##### Local
   - Simple backupper that copies the files to a different location on the same machine.
   - Can be used to copy files to any local location, such as a mounted drive or just a different folder.
##### SSH
   - Copies the data over SSH to a different machine.
   - Requires an SSH key.
##### S3
   - Copies the data to any S3-compliant object storage. 
   - Uses ```s3cmd``` for the file transfers.


## Usage:

#### Creating a new backup:
```
becky --name new_backup create --provider local
```
This command creates a new backup named ``` new_backup ``` and uses the ``` local ``` provider as backupper.
The other provider options are ``` remote ``` (SSH) or ``` s3 ```.

#### Adding required parameters for providers:
```
becky --name new_backup add param --type provider --key <PARAM NAME> --value <PATH TO BACKUP FOLDER>
```
This will add a provider parameter called <PARAM NAME> with the value <PATH TO BACKUP FOLDER>.
Different providers will require their own parameters.
##### Adding required parameters for local provider:
Local provider will only require one parameter, the location of the folder where all the backups will be stored.
```
becky --name new_backup add param --type provider --key output_path --value /backups
```
##### Adding required parameters for SSH provider:
SSH provider requires 3 params:
- remote_addr - the IP (or name) of the server where one wants to copy the files
- remote_path - location on the remote server where to copy the files
- ssh_id_path - path to the ssh-key which will be used to access the server without password

```
becky --name new_backup add param --type provider --key remote_addr --value 192.168.1.2
becky --name new_backup add param --type provider --key remote_path --value /remote_backups
becky --name new_backup add param --type provider --key shh_id_path --value /home/test/.ssh/id_rsa
```

##### Adding required parameters for S3 provider:

S3 provider requires 5 params:
- access_key
- secret_key
- host
- host_bucket
- bucket_name

These should all be provided by the object storage provider.

#### Adding a location to be backed up:
```
becky --name new_backup add location --path <PATH TO IMPORTANT DATA>
```
This will add the path to the important data to be backed up. 

#### Running the backup:
```
becky --name new_backup run
```
This will run the backup process for the ```new_backup``` backup.
Any files or folders as a location to backed up will be scanned. Any file that is new or has been modified since the last backup iteration will be backed up again.

#### Running the backup on schedule
```
becky cron --name new_backup --enable --schedule <CRONTAB FORMAT>
```
This will add a crontab job that will run the backup job on schedule. 
The given schedule format must be in the same format as crontab, such as ```'* * * * *'``` etc.

#### Disable backup schedule
```
becky cron --name new_backup --disable
```
This will remove any crontab jobs from this backup, so it won't automaticallly be run again.

#### Restore backed up file
```
becky --name new_test restore --path <FULL PATH OF BACKED UP FILE> --restore_path <FOLDER WHERE TO BACKUP FILE> --timestamp <EPOCH TIMESTAMP>
```
This will restore the file to the restore folder at the given timestamp. The timestamp will specify which version of the file to restore. 


## Installation
Becky can be installed from PyPi, by running:
```
pip3 install Becky
```
