import requests # Dependency 1
from typing import List, Set, Tuple, Dict
import re
#import graphviz
#import matplotlib.pyplot as plt
import validators # Dependency 2
import random
import score
import heapq
import json
import sys
import generation


def format_string(string: str) -> str:
    return break_string(string.replace("/", "").replace(":", ""), 20)

def break_string(string: str, step: int) -> str:
    i: int = 0
    while i < len(string):
        string = string[:i] + "\n" + string[i:]
        i += step
    return string

def get_host_url(url: str) -> str:
    return re.search('(https://[^/]*)', url).group(1)

def get_html_from_url(url: str) -> str:
    fp = requests.get(url)
    return fp.text

def get_hyperlinks(host_url: str, html: str) -> List[str]:
    links = []
    for ref in re.findall('<a href="[^"]*"', html):
        possible_link: str = ref[9:-1]
        try:
            if possible_link[0] == "/": # Augmenting with hostname if local/intersite jump
                possible_link = host_url + possible_link
            if validators.url(possible_link):
                links.append(possible_link)
        except:
            pass
    return links

def crawl():
    if len(sys.argv) == 3:
        # Args
        args = sys.argv[1:]
    else:
        args = ['https://scholarships360.org/scholarships/computer-science-scholarships/', 
            'https://www.gograd.org/resources/women-in-stem/'
            'https://builtin.com/women-tech/women-in-stem-scholarships',
            'https://collegerecon.com/stem-scholarships-women/']

        args = [args[random.randrange(0, len(args))]]

    # Hyperparams
    initial_url: str = args[0] # Initial node to start search
    prefix_constraint: str = None # All nodes have to contain this prefix
    max_number_of_nodes: int = 20 # Max amount of nodes to search before graph is generated
    max_branch_factor: int = 20 # Max amount of links to expand for each node

    # Crawling
    edges: List[Tuple] = []
    visited: Set[str] = {initial_url}
    fringe_set: List[str] = [initial_url]
    number_of_nodes: int = 0

    h = []
    while len(fringe_set) > 0 and number_of_nodes < max_number_of_nodes:
        number_of_nodes += 1

        curr: str = fringe_set.pop()
        print(str(number_of_nodes) + ": " + curr)

        html: str = get_html_from_url(curr)
        candidate_links: List[str] = get_hyperlinks(get_host_url(curr), html)

        # Updating max scoring link
        curr_score = score.scholarship_score(html)
        heapq.heappush(h, (-curr_score, curr))

        links: List[str] = []
        for l in candidate_links:
            if prefix_constraint is None:
                links.append(l)
            elif l[:len(prefix_constraint)] == prefix_constraint:
                links.append(l)

        if max_branch_factor is not None:
            links = random.sample(links, min(len(links), max_branch_factor))

        for l in links:
            edges.append((curr, l))
            if l not in visited:
                fringe_set.insert(0, l)
                visited.add(l)

    ranking: Dict = {}
    for i in range(1, len(h) + 1):
        link = heapq.heappop(h)
        ranking[i] = link[1]

    links = ranking.values()
    data = generation.randomize(links)
    
    return data
    # json_ranking: str = json.dumps(ranking)

    # with open('list.json', 'w') as f:
    #     f.write(json_ranking)

if __name__ == '__main__':
    crawl()

    """
    # Generating graph
    DG = graphviz.Digraph(comment='The Web', format='svg')

    DG.attr('graph', size="100,100")
    DG.attr('graph', layout="neato")
    DG.attr('graph', overlap="false")
    DG.attr('graph', sep="0.1")
    DG.attr('graph', pack="true")

    for v in visited:
        DG.node(format_string(v))

    for e_i in range(len(edges)):
        e = edges[e_i]
        if e_i % 100 == 0:
            print(str(e_i) + " out of " + str(len(edges)) + ", Processing edges...")
        DG.edge(format_string(e[0]), format_string(e[1]))

    # Saving graph
    DG.render('test-output/web.gv', view=True)
    """





