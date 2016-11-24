"""
Hogs library items by renewing them all.
Best put in a cronjob.
"""
import colorama
from bs4 import BeautifulSoup
import getpass
import requests
import os

BASE_URL = "https://pugwash.lib.warwick.ac.uk/iii/cas/login"
ACCOUNT_URL = "https://encore.lib.warwick.ac.uk/iii/encore/myaccount?lang=eng&suite=cobalt"

USERNAME_NAME = "extpatid"
PASSWORD_NAME = "extpatpw"
INPUT_SELECTOR = "form#fm1 input"
FAKE_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"

RENEW_ALL_FORM_DATA = {"renewall": "YES"}


def collect_credentials():
    """
    Grabs the user's warwick credentials
    by asking them to type them in.
    """
    if "WARWICK_USERNAME" in os.environ and "WARWICK_PASSWORD" in os.environ:
        return os.environ['WARWICK_USERNAME'], os.environ['WARWICK_PASSWORD']
    username = input("Enter Warwick username: ")
    password = getpass.getpass("Enter Warwick password: ")
    return username, password


def get_defaults(session):
    """
    Grabs the default inputs as a dictionary.
    """
    response = session.get(BASE_URL)
    bs = BeautifulSoup(response.content)
    inputs = {}
    for item in bs.select(INPUT_SELECTOR):
        inputs[item.get('name')] = item.get('value')
    return inputs


def get_account_url(session):
    """
    Gets the iframe URL for the account's list of books
    that are checked out.
    """
    response = session.get(ACCOUNT_URL)
    bs = BeautifulSoup(response.content)
    return bs.select("iframe#accountContentIframe")[0].get("src")


def do_login(session):
    """
    Collects the credentials and performs the login.
    """
    auth_tuple = collect_credentials()
    form_items = get_defaults(session)
    form_items[USERNAME_NAME] = auth_tuple[0]
    form_items[PASSWORD_NAME] = auth_tuple[1]
    session.post(BASE_URL, data=form_items)


def print_renewal_summary(response):
    """
    Prints a summary of the renewals.
    """
    bs = BeautifulSoup(response.text)
    if len(bs.select("#renewfailmsg")) > 0:
        print(colorama.Fore.RED + "✗" + " Not all renews were successful!" + colorama.Style.RESET_ALL)
    for item in bs.select(".patFuncEntry"):
        split = item.select(".patFuncTitleMain")[0].text.split("/")
        if len(item.select(".patFuncStatus em div")) > 0:
            print(
                colorama.Fore.RED +
                "[" + item.select(".patFuncStatus em div")[0].text.strip() + "] " +
                colorama.Style.RESET_ALL,
                end="")
        print(
            "{} by {}".format(
                colorama.Fore.BLUE + split[0].strip() + colorama.Style.RESET_ALL,
                split[1].strip()
            ),
            end="")
        print()


def main():
    """
    The main function, script entry-point.
    """
    print("LibraryHog\n==========\n")
    colorama.init()
    session = requests.Session()
    session.headers.update({"User-Agent": FAKE_USER_AGENT})
    do_login(session)
    renew_response = session.post(get_account_url(session), RENEW_ALL_FORM_DATA)
    print_renewal_summary(renew_response)


if __name__ == "__main__":
    main()
