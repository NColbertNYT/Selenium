
### Imports
from selenium import webdriver
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

## Set exectutable path for the Google Chrome Driver
ex_path = os.getcwd() + '/chromedriver'

## Set up driver
browser = webdriver.Chrome(executable_path = ex_path)

## Set and open url
wiki_url = 'https://www.wikipedia.org'
browser.get(wiki_url)

## Select the input
search_input = browser.find_element_by_xpath('//*[@id="searchInput"]')

## Type in "The New York Times"
search_input.send_keys("The New York Times")

## Click Search
browser.find_element_by_xpath('//*[@id="search-form"]/fieldset/button/i').click()

## Find all elements on the page that are links
all_links = browser.find_elements_by_tag_name("a")

## Get all of the href (url) attributes at each tag
links = []

for link in all_links[1:21]:
    links.append(link.get_attribute('href'))

## Repeat above for 20 links on each of the 20 pages
page = {}
for i in links:
    ## Go to link i
    browser.get(i)
    ## Find all "a" tags
    new_links = browser.find_elements_by_tag_name("a")
    newer_links = []
    ## Go through all "a" tags to get urls
    for link in new_links[1:21]:
        newer_links.append(link.get_attribute('href'))
    ## save everything in a dictionary
    page.update({i:newer_links})

#################
# Network Graph #
#################

## Declare and empty graph object
G = nx.Graph()

## Create edges from the dictionary, a tuple of each key, with every value
## associated with that key
edges = [(i, page.get(i)[j]) for i in page.keys() for j in range(len(page.get(i)))]

## Add edges to the graph
G.add_edges_from(edges)

## Set Figure Size and Plot
plt.figure(figsize=(50,50), dpi = 45)
nx.draw(G, with_labels = True)
wm = plt.get_current_fig_manager()
wm.full_screen_toggle()
plt.show()
