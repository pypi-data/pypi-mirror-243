import os
import requests
from fnmatch import fnmatch
from bs4 import BeautifulSoup


def _try_get(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to retrieve {url}.")
    return response


def download_links_on_page(page_url, download_dir, overwrite=False, regex=None):
    """Download all links on a page

    Args:
        page_url (str): URL to the target page
        download_dir (str): Directory used to store the downloaded content
        overwrite (bool): Whether to re-download exisiting files. Default is False.
        regex (str or None, optional): UNIX filename pattern to filter links, e.g. "*.csv". 
            The match is performed via fnmatch(). If None download everything. Defaults to None.

    Returns:
        downloaded_files (List[str]): Paths to downloaded files
    """
    # check download directory
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    response = _try_get(page_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    if not regex is None:
        links = filter(lambda s: fnmatch(s, regex), links)

    downloaded_files = []
    for link in links:
        fname = f"{download_dir.rstrip('/')}/{link.split('/')[-1]}"
        if fname in downloaded_files:
            continue
        if overwrite or (not os.path.exists(fname)):
            response = _try_get(link)
            with open(fname, 'wb') as f:
                f.write(response.content)
        downloaded_files.append(fname)

    return downloaded_files
