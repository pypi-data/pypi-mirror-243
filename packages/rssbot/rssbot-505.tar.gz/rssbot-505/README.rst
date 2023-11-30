**R  S  S  B  O  T**


!!


**NAME**

|
| RSSBOT - feed rss into your channel
|

**DESCRIPTION**

|
| RSSBOT is a python3 bot able to display rss feeds in your channel.
| It provides all the tools to program a bot, such as disk perisistence
| for configuration files, event handler to handle the client/server
| connection, code to introspect modules for commands, deferred
| exception handling to not crash on an error, a parser to parse
| commandline options and values, etc.
|
| You can copy/paste the service file and run it under systemd for
| 24/7 presence in a IRC channel.
|
| RSSBOT is a contribution back to society and is Public Domain.
|

**SYNOPSIS**

|
| rssbot <cmd> [key=val] 
| rssbot <cmd> [key==val]
| rssbot [-c] [-d] [-v] 
|

**INSTALL**

|
| pipx install rssbot
|

**USAGE**

|
| default action is doing nothing
|
| $ rssbot
| $

first argument is a command

|
| $ rssbot cmd
| cfg,cmd,dpl,mre,nme,pwd,rem,rss,ver

starting a console requires an option

|
| $ rssbot -c
| >

to start the rssbot as daemon

|
| $ rssbot -d
| $ 

add -v if you want to have verbose logging

|
| $ rssbot -cv
| RSSBOT started Wed Nov 8 15:38:56 2023 CVI
| >
|

**CONFIGURATION**


irc configuration is done with the cli interface
using the ``cfg`` command

|
| $ rssbot cfg server=<server>
| $ rssbot cfg channel=<channel>
| $ rssbot cfg nick=<nick>

sasl need a nickserv nick/password pair to generate
a password for sasl

|
| $ rssbot pwd <nsnick> <nspass>
| $ rssbot cfg password=<frompwd>

rss has several configuration commands

|
| $ rssbot rss <url>
| $ rssbot dpl <url> <item1,item2>
| $ rssbot rem <url>
| $ rssbot nme <url> <name>
|

**COMMANDS**


here is a list of the commands (use rssbot <cmd>)

|
| cfg - irc configuration
| cmd - commands
| dpl - sets display items
| mre - displays cached output
| pwd - sasl nickserv name/pass
| rem - removes a rss feed
| rss - add a feed
| sts - show status
| thr - show the running threads
|

**SYSTEMD**

save the following it in /etc/systems/system/rssbot.service and
replace "<user>" with the user running pipx

|
| [Unit]
| Description=feeding rss into your channel
| Requires=network.target
| After=network.target
|
| [Service]
| Type=simple
| User=<user>
| Group=<user>
| WorkingDirectory=/home/<user>/.rssbot
| ExecStart=/home/<user>/.local/pipx/venvs/rssbot/bin/rssbot -d
| RemainAfterExit=yes
|
| [Install]
| WantedBy=multi-user.target
|

then run this

|
| $ sudo systemctl enable rssbot --now
|
| default channel/server is #rssbot on localhost
|

**FILES**

|
| ~/.rssbot
| ~/.local/bin/rssbot
| ~/.local/pipx/venvs/rssbot/
|

**AUTHOR**

|
| Bart Thate <libbotx@gmail.com>
|

**COPYRIGHT**

|
| RSSBOT is a contribution back to society and is Public Domain.
