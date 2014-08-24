import sys
import operator
from collections import defaultdict
from secret import PASSWORD, USERNAME

import requests
import logging
logging.basicConfig(filename="output.log", level=logging.DEBUG, format = "%(asctime)s %(levelname)s %(message)s")

def get_repos(user):
	"""Retrieve a list of repos for a user"""
	url = "https://api.github.com/users/{user}/repos".format(user=user)
	response = requests.get(url, auth=(USERNAME, PASSWORD))
	logging.info("Retrive user repo")
	logging.debug(response.url)
	logging.debug("Retrieving user {user} repos".format(user=user))
	return response.json()

def main():
	"""Main"""
	repos=get_repos(sys.argv[1])
	logging.debug("In main: get repo for argv[1]")
	print repos

if __name__ == "__main__": main()