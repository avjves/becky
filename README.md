# Becky

Becky is a command-line based backup software.
It can periodically scan through your files, find any changes and subsequently backup the new files to a remote location.
Only works on Linux.

## Providers
Becky implements different providers that allow it to backup the data to many different locations or with different protocols.
Right now, Becky supports these providers:
#### Local
   - Simple backupper that copies the files to a different location on the same machine.
   - Can be used to copy files to any local location, such as a mounted drive or just a different folder.
#### SSH
   - Copies the data over SSH to a different machine.
   - Requires an SSH key.
#### S3
   - Copies the data to any S3-compliant object storage. 
   - Uses ```s3cmd``` for the file transfers.

## Installation

