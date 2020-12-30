#! /usr/bin/env python3

import re

import util

URL1 = "https://fi.wikipedia.org/wiki/Suuntanumero?action=raw&section=1"
# TODO: https://fi.wikipedia.org/wiki/Operaattoritunnus
# TOOD: https://fi.wikipedia.org/wiki/Matkapuhelinnumerot_Suomessa

CACHE1 = "suuntanumero.wiki"

COLUMNS = ["Alue", "Uusi", "Vanha"]
NEW = re.compile(r"^\* (0\d\d?) ([A-Za-zä -]+)$")
OLD = re.compile(r"^\*\* Aikaisemmin verkkoryhmät? ([\d, a-z*]+)$")


def scrape():
    area = newcode = oldcodes = None
    for line in open(util.get_cache_file(CACHE1, URL1)):
        new = NEW.match(line)
        if new:
            area = new.group(2)
            newcode = new.group(1)
        old = OLD.match(line)
        if old:
            assert area and newcode and not oldcodes
            oldcodes = old.group(1).replace(",", "").replace(" ja ", " ")
            oldcodes = " ".join(oldcodes.split())
            yield area, newcode, oldcodes
            area = newcode = oldcodes = None
    assert not (area or newcode or oldcodes)


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
