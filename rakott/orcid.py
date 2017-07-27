import requests # http://www.python-requests.org/
# requests.__version__ == '1.2.3'

ORCID_URL = "http://pub.orcid.org/%s/orcid-works"
DOI_BASE_URL = 'http://dx.doi.org/'

def parse_item(data):
    title = data['work-title']['title']['value']
    citation = data['work-citation']['citation'] if data['work-citation'] else ''
    journal = data['journal-title']#['subtitle']['value']
    url = ''
    if data['url']:
        if 'value' in data['url']['value']:
            url = data['url']['value']
        #url = data[0]['url']['value']
    doi = ''
    for v in data['work-external-identifiers']['work-external-identifier']:
       if v['work-external-identifier-type'] == 'DOI':
            doi = v['work-external-identifier-id']['value']
            url = DOI_BASE_URL + doi
    return {'title':title, 'journal':journal, 'url':url, 'doi':doi, 'citation':citation}

def extract_items(request):
    data = request.json()
    data = data['orcid-profile']
    data = data['orcid-activities']
    data = data['orcid-works']['orcid-work']
    return [parse_item(item) for item in data]

def orcid_items(orcid):
    headers = {'accept': 'application/orcid+json'}
    r = requests.get(ORCID_URL % orcid, headers=headers)
    if r.ok:
        return extract_items(r)
    else:
        return []

if __name__ == '__main__':
  print(orcid_items('0000-0002-9653-4458'))