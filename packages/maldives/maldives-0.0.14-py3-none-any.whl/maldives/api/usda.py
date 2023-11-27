import pandas as pd
import re
from zipfile import ZipFile
from maldives.utils.scrapping import download_links_on_page


def _format_tuple(tuple, format):
    return {k: tuple[v] for k, v in format.items()}


def _extract_tables(lines, titles):
    tables = {k: [] for k in titles.keys()}
    write_to = None  # pointer to which table we are writing

    for ln in lines:
        if type(ln) is bytes:
            ln = ln.decode('latin1')
        ln = ln.strip()

        if write_to is not None:
            if '"d"' in ln:
                write_to.append(ln)
            elif '"c"' in ln:
                write_to = None
        else:
            for k, v in titles.items():
                if any([vv in ln for vv in v]) and len(tables[k]) == 0:
                    write_to = tables[k]
                    break
    return tables


def _parse_date(fname):
    fname = fname.split('/')[-1]
    return pd.to_datetime(re.search('[0-9]{4}', fname).group(), format='%m%y')


def _parse_zipped_data(fname):
    zf = ZipFile(fname)
    table_titles = {'Placed': ['Cattle Placed on Feed by Weight Group'],
                    'Inventory': ['Cattle on Feed Inventory, Placements, Marketings, and Other Disappearance', 
                                  'Cattle on Feed, Placements, Marketings, and Other Disappearance']}  
    tables = _extract_tables(
        zf.open('cofd_all_tables.csv').readlines(), table_titles)

    FORMAT_ONFEEDBYWEIGHT = {'PLACED_U600': 3, 'PLACED_U700': 4, 'PLACED_U800': 5,
                             'PLACED_U900': 6, 'PLACED_U1000': 8, 'PLACED_A1000': 9}

    data = _format_tuple(
        tables['Placed'][-1].split(','), FORMAT_ONFEEDBYWEIGHT)
    data['ONFEED_OPEN'] = tables['Inventory'][0].split(',')[-2]
    data['PLACED'] = tables['Inventory'][1].split(',')[-2]
    data['MARKETED'] = tables['Inventory'][2].split(',')[-2]
    data['DISAPPEAR'] = tables['Inventory'][3].split(',')[-2]
    data['ONFEED_CLOSE'] = tables['Inventory'][4].split(',')[-2]
    return data


class USDACattleData(object):
    def __init__(self, base_url="https://usda.library.cornell.edu/concern/publications/m326m174z", work_dir="cattle_data"):
        self.base_url = base_url
        self.work_dir = work_dir
        self.df = None

    def load_data(self, num_months=60, overwrite=False):
        data_files = []
        page = 1
        while len(data_files) < num_months:
            data_files.extend(download_links_on_page(
                f"{self.base_url}?page={page}", self.work_dir, overwrite=overwrite, regex="*.zip"))
            page += 1

        entries = []
        for fname in set(data_files):
            data = _parse_zipped_data(fname)
            data['Date'] = _parse_date(fname)-pd.DateOffset(months=1)
            entries.append(data)
        self.df = pd.DataFrame(entries).set_index('Date').sort_index().astype(float)
        return self.df
