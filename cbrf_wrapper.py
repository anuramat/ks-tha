import requests
import xml.etree.ElementTree as ET
from decimal import Decimal

_usd_id = "R01235"


def get_usd_rate() -> Decimal:
    """
    returns RUB/USD exchange rate
    """
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
    # except requests.exceptions.RequestException # TODO
    # if req.status_code != 200: # TODO exception

    # XXX change to read from file object?
    root = ET.fromstring(response.text)
    # tree = ET.parse(response.raw)
    # root = tree.getroot()

    # TODO exceptions
    for currency in root:
        # <Element 'NumCode' at 0x1037751d0> 840
        # <Element 'CharCode' at 0x103775220> USD
        # <Element 'Nominal' at 0x103775270> 1
        # <Element 'Name' at 0x1037752c0> Доллар США
        # <Element 'Value' at 0x103775310> 58,5322
        if currency.attrib["ID"] == _usd_id:
            # XXX check charcode, name?
            # TODO catch for empty/nonparseable string
            str_rate = currency.find("Value").text
            decimal_rate = Decimal(".".join(str_rate.split(",")))
            return decimal_rate
    # TODO change exception type
    raise Exception


def main():
    print(get_usd_rate())


if __name__ == "__main__":
    main()
