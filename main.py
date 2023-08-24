from collections import deque
import requests as request
from bs4 import BeautifulSoup
import re

WIKIPEDIA_URL = "https://en.wikipedia.org/api/rest_v1/page/html"
CUSTOM_HEADERS = {'User-Agent': 'wiki-crawler/0.0.1'}

SOURCE = "John_Rawls"
DESTINATION = "Garden"

# get page html
def get_wiki_page(page: str):
	response = request.get("%s/%s" % (WIKIPEDIA_URL, page), headers = CUSTOM_HEADERS)
	return response.text

# parse html for links
def get_wiki_links(html: str):
	links = []

	LINK_REGEX = r"\.\/(.*)"
	soup = BeautifulSoup(html, 'html.parser')
	anchors = soup.find_all("a")
	for anchor in anchors:
		href = anchor.get("href")
		if href:
			match = re.match(LINK_REGEX, href)
			if match:
					links.append(match.group(1))
	
	return links

# perform a BFS search using wikipedia links as neighbors
def bfs(root_page: str):
	visited, queue = set(), deque([(root_page, ())])
	visited.add(root_page)

	while queue:
		current_page, trail = queue.popleft()

		# do not want
		# * "#" in article name
		# * "?" in article name
		# * starts with "File:"
		# * starts with "Help:"
		if "#" in current_page or "?" in current_page or current_page.startswith("File:") or current_page.startswith("Help:"):
			continue

		html = get_wiki_page(current_page)
		links = get_wiki_links(html)
		print("article %s has %s links at depth %s" % (current_page, len(links), len(trail)))

		if current_page == DESTINATION:
			print(trail)
			break

		for link in links:
			if link not in visited:
				visited.add(link)
				queue.append((link, trail + (link,)))

bfs(SOURCE)
