#! /usr/bin/env python

import pwd
import grp
import spwd
import operator
import re
import os
import csv

users = []																#create emtpy user list
for u in pwd.getpwall():														#retrieve and walk the user list
        users.append(u[0])														#populate the user list

with open('list.csv', 'wb') as csvfile:													#setup the csv file
	listwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)					#setup the csv file
	listwriter.writerow(["Username", "Primary group", "other groups", "locked", "non-system user", "last access", "home dir"])	#setup the cloumn headers in the csv file

	for user in users:														#main loop, for every user gets the needed data
		group = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]								#gets the groups the user is member of (but not the primary)
		str_rep_group = str(group)												#transforms the array in a usable object
		str_group = str_rep_group.replace("', '"," ").replace("[","").replace("]","").replace("'","")				#sanitizes the string 
		if not str_group: str_group = " "											#if the string is empty displays a empty space to retain csv alignment
		home = pwd.getpwnam(user).pw_dir											#gets the homedir of the user
		gr_id = pwd.getpwnam(user).pw_gid											#gets the id of the primary group of the user
		main_gr = grp.getgrgid(gr_id)[0]											#gets the name of the group using the id
		if len(spwd.getspnam(user).sp_pwd) >= 3: sys_usr = "yes" 								#to understand if a user is a system user, it checks if the password is longer than 3chars, if it is, the user is considered a non-system user
		else: sys_usr = " "													#
		if "!!" in spwd.getspnam(user).sp_pwd: usr_lock = "yes"									#to understand if the user is locked or not, looks for !! in the password
		else: usr_lock = " "													#
		f=os.popen("last " + user + " | tail -n 3 | grep " + user)								#command used to retrieve the last access
		usr_lastacc = f.readlines()												#read the output of the command for the last access
		rep_usr_lastacc = str(usr_lastacc)											#transforms the	array in a usable object
		str_usr_lastacc = rep_usr_lastacc.replace("[","").replace("]","").replace(",","").replace("'","").rstrip()		#sanitizes the string
		if not str_usr_lastacc: str_usr_lastacc = "user never logged on"							#if the string is empty, the filed is filled with text stating the user never logged on the system
		print "-----------------------------------------------------------"							#DEBUG OUTPUT
		print "User: " + user 													#DEBUG OUTPUT
		print "primary group: " + main_gr											#DEBUG OUTPUT
		print "other groups: " + str_group											#DEBUG OUTPUT
		print "user locked?: " + usr_lock											#DEBUG OUTPUT
		print "system user?: " + sys_usr											#DEBUG OUTPUT
		print "last access: " + str_usr_lastacc											#DEBUG OUTPUT
		print "home dir: " + home												#DEBUG OUTPUT
		listwriter.writerow([user, main_gr, str_group, usr_lock, sys_usr, str_usr_lastacc, home])				#writes the retrieved fields in the csv file
