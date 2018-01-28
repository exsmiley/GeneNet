import requests
import json
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import os
import shutil

base_url = 'https://www.ncbi.nlm.nih.gov/gene/?term={}'

def get_all_ids_from_trrust():
    with open('data/trrust_raw.json') as f:
        data = json.loads(f.read())

    ids = set()
    all_ids = []
    passage = data['collection']['document']['passage']

    for link in passage:
        annotation = link['annotation']
        gene1 = annotation[0]['infon'][1]['__text']
        gene2 = annotation[1]['infon'][1]['__text']
        ids.add(gene1)
        ids.add(gene2)
    return ids


def scrape_id(id):
    try:
        url = base_url.format(id)
        r = requests.get(url)
        data = load_data_from_html(r.text)
        with open('raw/' + str(id), 'w') as outfile:
            json.dump(data, outfile)
    except:
        print "Failed on {}".format(id)


def load_data_from_html(s):
    data = {}
    soup = BeautifulSoup(s, 'html.parser')

    # handle summary stuffs
    summaryDiv = soup.find(id='summaryDiv')
    dl_data = summaryDiv.find_all("dt")
    for dlitem in dl_data:
        key = ' '.join(dlitem.text.split())
        value = dlitem.find_next_sibling('dd').text.strip()
        if 'provided' in value:
            index = value.find('provided')
            value = value[:index]
        data[key] = value

    # get location
    data['Location'] = soup.find("dl", {"class": "dl-chr-info"}).find('dd').text.strip()
    # print data['location']

    data['Exon count'] = soup.find("dl", {"class": "dl-chr-info exon-count"}).find('dd').text.strip()
    
    data['Chromosome'] = soup.find('p', {'class': 'withnote margin_t2em'}).text.strip()

    return data

def merge_raw():
    all_data = {}
    dirs = os.listdir('raw')
    for id in dirs:
        with open('raw/'+id) as f:
            id_data = json.loads(f.read())
        all_data[id] = id_data
    with open('data/processed.json', 'w') as f:
        json.dump(all_data, f)
    shutil.rmtree('raw')

def scrape_ids():
    ids = get_all_ids_from_trrust()
    p = Pool(8)

    # gives us a bunch of raw json files in raw/ directory
    p.map(scrape_id, ids)
        
    # merges raw data and puts it in a single processed json
    merge_raw()

if __name__ == '__main__':
    scrape_ids()
