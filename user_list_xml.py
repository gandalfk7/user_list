#! /usr/bin/env python

# LICENSE:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# INFO:
# This script has been developed under CentOS and has been tested with CentOS 6.7 and Oracle Linux Server 6.4
# it requires python 2.x and root privileges (to read the shadow file)
# it exports and .xml file named: HOSTNAME_UserGroupList_DATE.xml containing data of users and groups.


import pwd
import grp
import spwd
import operator
import re
import os
import csv
import time

line_open = '<tr><td>'
line_mid = '</td><td>'
line_close = '</td></tr>\n'

xmlfilename = str(os.uname()[1].split(".")[0]) + "_UserGroupList_" + str(time.strftime("%Y%m%d")) + ".xml"				#builds the filename with the hostname, the arbitrary title, the date and the extension

file = open(xmlfilename, "w")

users = []																#create emtpy user list
for u in pwd.getpwall():														#retrieve and walk the user list
        users.append(u[0])														#populate the user list

file.write('<?xml version="1.0" encoding="utf-8"?><html lang="en-US" xmlns="http://www.w3.org/1999/xhtml"><head><style>\n')
file.write('table {border-collapse: collapse;}\n')
file.write('table, td, th {border: 1px solid gray;}\n')
file.write('</style></head><body style="font-size: 11pt; font-family: Verdana, Arial;"><table><tr class="sep" style="background-color: silver;"><td><b>Username</b></td><td><b>Primary Group</b></td><td><b>Other Groups</b></td><td><b>Locked</b></td><td><b>Type</b></td><td><b>Last Access</b></td><td><b>Home Dir</b></td></tr>\n')

for user in users:														#main loop, for every user gets the needed data
	group = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]								#gets the groups the user is member of (but not the primary)
	str_rep_group = str(group)												#transforms the array in a usable object
	str_group = str_rep_group.replace("', '"," ").replace("[","").replace("]","").replace("'","")				#sanitizes the string 
	if not str_group: str_group = " "											#if the string is empty displays a empty space to retain csv alignment
	home = pwd.getpwnam(user).pw_dir											#gets the homedir of the user
	gr_id = pwd.getpwnam(user).pw_gid											#gets the id of the primary group of the user
	main_gr = grp.getgrgid(gr_id)[0]											#gets the name of the group using the id
	if len(spwd.getspnam(user).sp_pwd) >= 3: sys_usr = "User" 								#to understand if a user is a system user, it checks if the password is longer than 3chars, if it is, the user is considered a non-system user
	else: sys_usr = "System"												#
	if "!!" in spwd.getspnam(user).sp_pwd: usr_lock = "yes"									#to understand if the user is locked or not, looks for !! in the password
	else: usr_lock = " "													#
	f=os.popen("last " + user + " | head -n 1 | grep " + user)								#command used to retrieve the last access
	usr_lastacc = f.readlines()												#read the output of the command for the last access
	rep_usr_lastacc = str(usr_lastacc)											#transforms the	array in a usable object
	str_usr_lastacc = rep_usr_lastacc.replace("[","").replace("]","").replace(",","").replace("'","").rstrip()		#sanitizes the string
	if not str_usr_lastacc: str_usr_lastacc = "user never logged on"							#if the string is empty, the filed is filled with text stating the user never logged on the system
	file.write(line_open + user + line_mid + main_gr + line_mid + str_group + line_mid + usr_lock + line_mid + sys_usr + line_mid + str_usr_lastacc + line_mid + home + line_close)
#	print "-----------------------------------------------------------"							#DEBUG OUTPUT
#	print "User: " + user 													#DEBUG OUTPUT
#	print "primary group: " + main_gr											#DEBUG OUTPUT
#	print "other groups: " + str_group											#DEBUG OUTPUT
#	print "user locked?: " + usr_lock											#DEBUG OUTPUT
#	print "system user?: " + sys_usr											#DEBUG OUTPUT
#	print "last access: " + str_usr_lastacc											#DEBUG OUTPUT
#	print "home dir: " + home												#DEBUG OUTPUT

file.write('</table>\n')

file.write('<br /><br />\n')

file.write('<table><tr style="background-color: silver;"><td><b>Group</b></td><td><b>Members</b></td></tr>')

all_groups = grp.getgrall()
for group in sorted(all_groups):
	file.write(line_open + str(group.gr_name) + line_mid + str(group.gr_mem).replace("', '"," ").replace("[","").replace("]","").replace("'","") + line_close)

file.write('</table></body></html>\n')

file.close()
