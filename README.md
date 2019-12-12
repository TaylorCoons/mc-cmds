# mc-cmds
## A python command line tool to help backup a linux minecraft server

### Setup assumptions:
Currently I wrote this with some assumptions in mind since it is for personal
use.

1. The file structure assumes that there is a root directory with each individual minecraft server residing in a subdirectory
  * minecraft_root/
    * minecraft_server/
      * world/
      * minecraft_server.jar
      * eula.txt
      * etc...
1. The minecraft server must be named minecraft_server.jar since this is currently how the program checks to see if a directory contains a minecraft server (since there might be other folders other than server folders under minecraft_root)
1. I wrote this on Ubuntu using the commands and used the commands top, service, and tail so if your on a os where those commands dont exist or have different outputs then let me know and I can come up with a better way

### Supported commands
Alright now to the fun part. Currently, there are 4 commands they are:
1. list
2. env
3. backup
4. clean
5. status

#### list
the list command just lists the minecraft servers under the root directory since you made them you probably know what they are but this command also acts to see if your environment variables are setup properly

ex.

    cmd.py list

#### env
The env command just lists the environment variables the script uses and what they are so you know what to change to customize the script.

ex.

    cmd.py env

#### backup
The backup command takes the current servers world and places a copy of the folder with the date appended to the backups folder set with the env variables.
This command can be supplied with **all** instead of a server name to backup the worlds of all servers.

ex.

    cmd.py backup serv1
#### clean
The clean command takes in a server as an argument (again the **all** option is also available) and an integer argument specifying the number of backups to keep! Therefore if the command was invoked with:

    cmd.py clean serv1 -n 5

all of the backups *except* the 5 most recent backups in the serv1 backups folder would be removed

#### status
The status command will specify some basic stats about a server such as:
1. The current status (active, disabled, exited, etc...)
1. The RAM the server is using
1. The memory percent of the server for the rigs ram (not the allocated ram)
1. The cpu percent

ex.

    cmd.py status serv1


### Intended Setup
I put the commands:

    cmd.py backup serv1
    cmd.py clean serv1 -n 10

into a cronjob to run daily to backup the world data on each server every day and only keep 10 copies at a time.

### Ideas:
1. Add a restore command that allows the user to specify a backup to restore. The backup could be chosen based on:
  * A time stamp
  * The most recent
  * A time diff (like 5 days ago)
1. Update the time stamping process to be a full time stamp instead of an iso formated date to allow multiple backups per day without overwrite
1. Show memory percent based on allocated memory instead of rigs memory as well
1. Network stats of server (somehow this has to be possible but might require modding the servers)

