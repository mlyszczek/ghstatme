#!/usr/bin/env python3

## ==========================================================================
#                         ░▀█▀░█▄█░█▀█░█▀█░█▀▄░▀█▀░█▀▀
#                         ░░█░░█░█░█▀▀░█░█░█▀▄░░█░░▀▀█
#                         ░▀▀▀░▀░▀░▀░░░▀▀▀░▀░▀░░▀░░▀▀▀
## ==========================================================================
import argparse
import github
import sys
import os


## ==========================================================================
#                     ░█▀▀░█░█░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀
#                     ░█▀▀░█░█░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█
#                     ░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀
## ==========================================================================
#                                 ⢀⣀⢀⡀⡇⡇⢀⡀⢀⣀⣰⡀
#                                 ⠣⠤⠣⠜⠣⠣⠣⠭⠣⠤⠘⠤
## ==========================================================================
#   Collects views and clones from github, merges them into single dict,
#   and returns that dict.
## ==========================================================================
def collect(user, repo, token):
	# connect to github and check if user/repo is valid
	gh = github.GitHub(token)
	try:
		gh.repos(user, repo).get()
	except Exception:
		sys.exit("repo: " + user + "/" + repo + " not found")

	# fetch views and clones, we will have max of 14 days worth of data
	views = gh.repos(user, repo).traffic.views.get()
	clones = gh.repos(user, repo).traffic.clones.get()

	db = {}
	# views and clones are too similar and yet to different in format,
	# we need to run custom loop to merge them together
	for view in views['views']:
		# convert long timestamp in short YYYY-mm-dd format
		timestamp = view['timestamp'][0:10]
		if timestamp not in db.keys():
			db[timestamp] = {}
		db[timestamp]["vuniqs"] = view['uniques']
		db[timestamp]["vcount"] = view['count']
	for clone in clones['clones']:
		# convert long timestamp in short YYYY-mm-dd format
		timestamp = clone['timestamp'][0:10]
		if timestamp not in db.keys():
			db[timestamp] = {}
		db[timestamp]["cuniqs"] = clone['uniques']
		db[timestamp]["ccount"] = clone['count']

	return db


## ==========================================================================
#                                ⢀⣀⢀⣀⡀⢀⢀⡀ ⢀⣸⣇⡀
#                                ⠭⠕⠣⠼⠱⠃⠣⠭ ⠣⠼⠧⠜
## ==========================================================================
def save_db(user, repo, db, out):
	# create database directory for repo if it doesn't exist yet
	workdir = out + "/" + user + "/" + repo
	os.makedirs(workdir, exist_ok=1)

	# dump db to files. One file is created for each entry in db,
	# if file already exists, it's not modified
	for timestamp in db:
		file = workdir + "/" + timestamp

		if os.path.exists(file):
			# file exists, stats already fetched and stored for that day
			continue

		# file does not exist, store new statistics, this little print
		# will simply store numbers delimited by spaces
		with open(file, "w") as f:
			vuniqs = db[timestamp].setdefault("vuniqs", 0)
			vcount = db[timestamp].setdefault("vcount", 0)
			cuniqs = db[timestamp].setdefault("cuniqs", 0)
			ccount = db[timestamp].setdefault("ccount", 0)
			print(vuniqs, vcount, cuniqs, ccount, file=f)
			print("{} {}: uniq views: {}, views: {}, uniq clones: {}, clones: {}".
					format(timestamp, repo, vuniqs, vcount, cuniqs, ccount))


## ==========================================================================
#                               ░█▄█░█▀█░▀█▀░█▀█
#                               ░█░█░█▀█░░█░░█░█
#                               ░▀░▀░▀░▀░▀▀▀░▀░▀
## ==========================================================================
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--repo', required=1,help="repo name to fetch")
parser.add_argument('-u', '--user', required=1, help="owner ofthe repo to fetch")
parser.add_argument('-t', '--token', required=1, help="your github token")
parser.add_argument('-o', '--out', default=".", help="where stats should be stored")

args = parser.parse_args()

db = collect(args.user, args.repo, args.token)
save_db(args.user, args.repo, db, args.out)
