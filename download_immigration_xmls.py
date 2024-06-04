import csv
import logging
import requests

from tqdm import tqdm
from time import sleep

XML_PREFIX = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles"


def get_immigration_eins():
    eins = set()
    with open("../data/raw/immigration-eins.txt", "r") as f:
        for line in f.readlines():
            eins.add(line.strip())

    return eins


def main():
    urls = []
    eins = get_immigration_eins()
    with open("../data/raw/index_2023.csv") as index_file:
        reader = csv.DictReader(index_file)
        for row in reader:
            if row["EIN"] in eins:
                urls.append(
                    (
                        row["EIN"],
                        row["OBJECT_ID"],
                        f"{XML_PREFIX}/{row['OBJECT_ID']}_public.xml",
                    )
                )

    for ein, obj_id, url in tqdm(urls):
        r = requests.get(url)

        if r.status_code == 404:
            logging.error(f"404 for {url}")
            continue

        r.raise_for_status()
        with open(f"../990-xml-reader/irs_reader/XML/{obj_id}_public.xml", "wb") as f:
            f.write(r.content)

        sleep(0.1)


if __name__ == "__main__":
    main()
