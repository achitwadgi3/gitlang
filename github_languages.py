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

def get_lang_dict(repos):
	""" 
	Return a list of dicts containing languages used in each repo
	"""
	lang_dict =[]
	for repo in repos:
		url = "https://api.github.com/repos/{owner}/{reposit}/languages".format(owner=repo["owner"]["login"], reposit = repo["name"] )
		logging.debug("IN GET_LANG_URL: {}".format(url))
		print url
		response = requests.get(url, auth=(USERNAME,PASSWORD))
		lang_dict.append(response.json())
	return lang_dict

def accumulate_languages(language_dictionaries):
	""" Calculate total size for each lang """
	accumulated = defaultdict(int)
	total =0
	for language_dict in language_dictionaries:
		for lang_name, no_bytes in language_dict.iteritems():
			accumulated[lang_name] +=no_bytes
			total += no_bytes
	return accumulated, total


def main():
	"""Main"""
	repos=get_repos(sys.argv[1])
	logging.debug("In main: get repo for argv[1]")
	lang_dicts= get_lang_dict(repos)
	#print lang_dicts
	#print repos[1]
	lang_total, total_bytes = accumulate_languages(lang_dicts)

	print lang_total, total_bytes
	sorted_lang_totals = sorted(lang_total.iteritems(), key=operator.itemgetter(1), reverse=True)

	print sorted_lang_totals
	for lang_name, no_bytes in sorted_lang_totals:
		percent = 100 * no_bytes / total_bytes
		print "{}: {:.2f}%".format(lang_name, percent)

if __name__ == "__main__": main()