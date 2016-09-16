#!/usr/bin/env python
from lxml import html
import requests
import urllib, json

from os import listdir
from os.path import isfile,isdir, join
from time import sleep
import os,sys
import subprocess, shlex
import re


def install_files():
	my_json = get_json()
	print "\nJSON:"
	for item in my_json:
		print item
		print

	failures = []
	not_apks = []
	installed_packages = []
	double_installs = []

	# COMMENT OUT LINE BELOW IF FILES ALREADY DOWNLOADED:
	download_files(my_json)

	uninstall_apps()

	# REFACTOR INTO A METHOD THIS CHUNK OF CODE:
	print "\nINSTALLING:"

	file_path = "/Users/markmcquillen/Desktop/JSON_Parse/"
	# APKsToPush = [f for f in os.listdir(file_path) if f.endswith(".apk")]
	APKsToPush = [f for f in os.listdir(file_path)]

	APKsToPush.remove('.DS_Store')
	APKsToPush.remove('.git')
	APKsToPush.remove('JSONScrape.py')

	for apk in APKsToPush:
		print apk
		if apk.endswith(".apk"):
			command = 'aapt list -a ' + file_path + apk + ' | sed -n "/^Package Group[^s]/s/.*name=//p"'
			package_name = subprocess_cmd(command)
			if any(package_name in s for s in installed_packages):
				print package_name + " HAS ALREADY BEEN INSTALLED! NOT INSTALLING AGAIN! ***************************************"
				print
				double_installs.append(apk)
				double_installs.append(package_name)
			else:
				command = "adb install -r " + file_path + apk
				print command
				if "Success" not in subprocess_cmd(command):
					failures.append(apk)
				else:
					installed_packages.append(package_name)
		else:
			print "************************* NOT APK FILE **************************"
			print
			not_apks.append(apk)

	print "\nFAILURES:"
	for name in failures:
		print name

	print "\nNOT APK:"
	for name in not_apks:
		print name

	print "\nINSTALLED PACKAGES:"
	for name in installed_packages:
		print name

	print "\nDUPLICATE PACKAGE NAMES:"
	counter = 1
	for name in double_installs:
		print name
		if counter % 2 == 0:
			print
		counter += 1
	print


def uninstall_apps():
	file_path = "/Users/markmcquillen/Desktop/JSON_Parse/"
	APKsToPush = [f for f in os.listdir(file_path) if f.endswith(".apk")]
	print "\nFILENAMES FROM DIRECTORY:"
	for name in APKsToPush:
		print name
	print

	package_names = []

	print "FILENAMES WITH PACKAGE NAMES:"
	for apk in APKsToPush:
		print apk
		command = 'aapt list -a ' + file_path + apk + ' | sed -n "/^Package Group[^s]/s/.*name=//p"'
		name = silent_subprocess_cmd(command)
		print name
		print
		package_names.append(name)
	print "PACKAGE NAMES:"	
	for name in package_names:
		print name

	print "\nUNINSTALLING:"
	package_names = reversed(package_names)
	for name in package_names:
		print name
		order = "adb uninstall " + name
		subprocess_cmd(order)


def get_json():
	url = "http://videoplayer-builder-dev.elasticbeanstalk.com/latest/json"
	response = urllib.urlopen(url)
	my_json = json.loads(response.read())
	return my_json


def get_urls():
	urls = []
	url = "http://videoplayer-builder-dev.elasticbeanstalk.com/latest/json"
	response = urllib.urlopen(url)
	json_response = json.loads(response.read())
	for element in json_response:
		urls.append(element["url"])
	return urls


def download_files(my_json):
	print "\nDOWNLOADING:"
	counter = 1
	for item in my_json:
		if counter < 10:
			num = "0" + str(counter)
		else:
			num = str(counter)
		link = item["url"]
		title = num + "_" + item["filename"]
		print title
		urllib.urlretrieve (link, title)
		counter += 1


def subprocess_cmd(command):
	process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	print proc_stdout
	rc = process.returncode
	print "return code: %s" % (rc)
	print
	return proc_stdout


def silent_subprocess_cmd(command):
	process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
	proc_stdout = process.communicate()[0].strip()
	rc = process.returncode
	return proc_stdout


install_files()

