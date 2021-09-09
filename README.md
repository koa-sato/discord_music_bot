# discord_music_bot

####Create a config.env with the following:
#!/bin/bash

export DISCORD_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export DEEZER_APP_ID="XXXXXX"
export DEEZER_SECRET="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

#### Then, run config.env to export the env variables
. config.env

### Install dependenices
pip3 install -r requirements.txt

### Run app with:
python3 bot.py


### Starting mysql
sudo apt-get install mysql-server
sudo service mysql start
sudo mysql --defaults-file=/etc/mysql/debian.cnf
