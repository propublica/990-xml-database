import sys
import csv
import logging
import requests

from tqdm import tqdm
from time import sleep

XML_PREFIX = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles"


def get_immigration_eins():
    eins = set()
    with open("./data/raw/all-immigration-ein-matches.txt", "r") as f:
        for line in f.readlines():
            eins.add(line.strip())

    return eins


def main():
    year = sys.argv[1]

    urls = []
    eins = get_immigration_eins()
    with open(f"./data/raw/index_{year}.csv") as index_file:
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

    logging.info(f"Found {len(urls)} matches in the index file")

    not_found = []
    for ein, obj_id, url in tqdm(urls):
        r = requests.get(url)

        if r.status_code == 404:
            not_found.append(ein)
            continue

        r.raise_for_status()
        with open(f"./990-xml-reader/irs_reader/XML/{obj_id}_public.xml", "wb") as f:
            f.write(r.content)

        sleep(0.1)

    print(f"Couldn't find {len(not_found)} 990s: {not_found}")


if __name__ == "__main__":
    main()
