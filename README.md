# Remote file search helper
- search file on remote computer
- mail the file to you

# Use
- run `cp example_setting.yml .yml` or `copy example_setting.yml .yml` to make setting file
- then edit `.yml` file
> if you are using gmail, please enable the sending permission
- run `python socket_server.py` as your server
- run `python socket_client.py` as your client

# File description
- `socket_server.py` : socket server
- `socket_client.py` : socket client
- `socket_event.py` : define socket evevnt
- `socket_comm.py` : handle socket communication
- `smtp.py` : handle mail seading
- `zip.py` : handle zip files
