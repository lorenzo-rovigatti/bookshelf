import re

import requests

import json

def form_url(ISBN='9780980200447'):
    """Formulate an url that will be sent to openlibrary.org/api'.

    Parameters
    ----------
    ISBN : string
        a string of book's ISBN.

    Returns
    -------
    string
        An url that will be sent to openlibrary/org/api.

    """
    url = 'https://openlibrary.org/api/books?bibkeys=ISBN:' + \
        ISBN + '&jscmd=data&format=json'

    return url


def get_ISBN_from_title(title, author):

    h = {'Authorization': '43360_fd60754106422e4ff2600025312a1118'}
    title = title.title()
    #title = "%20".join( title.split() )
    resp = requests.get("https://api2.isbndb.com/books/{" \
             +title +"}", headers=h)


    results = resp.json()['books']
    # note that this gets the last ISBN in the list--there maybe multiple copies
    # of the book--hopefully all additions have the same dewey decimal number
    right = None
    for x in results:
        try:
            if 'authors' in x.keys():
                if author in x['authors']:
                    right= x['isbn13']
        except:
                pass

    return right

def get_reponse(url):
    response = requests.get(url)
    print('Acquired following info about the book {}'.format(response.text))
    return response.text


def extract_ddc(text):
    dewey_pattern = re.compile('(\\d{3}/.\\d)')
    ddc = dewey_pattern.findall(text)[0]
    print('Dewey decimal code of the book is {}'.format(ddc))
    return ddc


def get_ddc_api(ISBN=None, title=None, author_name=None):
    if ISBN:
        url = form_url(ISBN)
    elif title & author_name:
        ISBN = get_ISBN_from_title(title, author_name)
        url = form_url(ISBN)
    else:
        url = form_url(author_name)

    response = get_reponse(url)
    ddc = extract_ddc(response)
    return ddc
