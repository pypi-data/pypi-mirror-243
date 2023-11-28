from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

ACCOUNTING_URL_SYNC = (
    "http://goc-accounting.grid-support.ac.uk/rss/{site_name}_Sync.html"
)
ACCOUNTING_URL_TEST = (
    "http://goc-accounting.grid-support.ac.uk/rss/{site_name}_Pub.html"
)


def _get_accounting_data(url: str) -> List[Dict[str, str]]:
    """Get accounting data from the given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("Failed to get accounting data from %s" % url)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    header = [cell.text for cell in rows[1].find_all("th")]
    data = []
    for row in rows[2:]:
        data.append(dict(zip(header, [cell.text for cell in row.find_all("td")])))

    return data


def check_apel_publication_test(site_name: str) -> Tuple[bool, str]:
    test_column = "Publication  Status"
    data = _get_accounting_data(ACCOUNTING_URL_TEST.format(site_name=site_name))
    test_result = data[0][test_column]
    # test_result is of the form "OK [ last published 2 days ago: 2021-02-31 ]"
    # check how many days ago it was published
    days_ago = int(test_result.split("last published ")[1].split(" days ago")[0])
    return ("OK" in test_result and days_ago < 3), test_result


def check_apel_sync_data(site_name: str) -> Tuple[bool, str]:
    test_column = "Synchronisation  Status"
    data = _get_accounting_data(ACCOUNTING_URL_SYNC.format(site_name=site_name))
    latest_test_result = data[0][test_column]
    # test_result is of the form "OK [ last sync 2 days ago: 2021-02-31 ]"
    # check how many days ago it was published
    days_ago = int(latest_test_result.split("last published ")[1].split(" days ago")[0])
    latest_result = "OK" in latest_test_result and days_ago < 3
    # check if there are any failed tests
    failed_tests = [test for test in data if "OK" not in test[test_column]]
    return latest_result and failed_tests == [], latest_test_result


if __name__ == "__main__":
    from dice_lib import load_config

    config = load_config()
    site_name = config.site_info.gocdb_name

    pub_test, pub_test_msg = check_apel_publication_test(site_name)
    msg = "OK" if pub_test else "NOT OK: " + pub_test_msg
    print(f"Publication test status: {msg}")

    sync_test, sync_test_msg = check_apel_sync_data(site_name)
    msg = "OK" if sync_test else "NOT OK: " + sync_test_msg
    print(f"Synchronisation test status: {msg}")
