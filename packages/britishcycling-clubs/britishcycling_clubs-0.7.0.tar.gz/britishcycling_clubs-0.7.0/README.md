# britishcycling-clubs

## About

**Unofficial, not affiliated or endorsed by British/Scottish/Welsh Cycling.**

Library to automate aspects of British Cycling's Club Management Tool, in order to
simplify administration for clubs using it. It probably works for Scottish/Welsh
Cycling clubs too, but this hasn't been tested.

Priority is to read data in order to create reports/notifications to club
administrators.

## Prerequisites

- Credentials for a club using the Club Management Tool

## Installation

Install from PyPI, e.g:

`pip install britishcycling-clubs`

Some functions use [Playwright](https://playwright.dev/python/) to automate a 
headless Chromium browser. This needs to be installed:

`playwright install chromium`

If you're installing in e.g. a bare-bones server/CI environment, you'll probably be 
prompted to install system dependencies, which you can do with:

`playwright install-deps chromium`

See also https://playwright.dev/python/docs/browsers#install-system-dependencies


## Usage

```
def get_private_member_counts(
    club_id: str,
    username: str,
    password: str,
    manager_page_load_delay: int = 5,
) -> dict[str, int]:
```
Get numbers of active, pending, expired members from the club manager page.

Specifically, returns the counts from these tabs:

- Active Club Members
- New [i.e. pending] Club Subscriptions
- Expired Club Members

This takes about 10s.

```
get_public_club_info(club_id: str) -> dict[str, int | str]
```
Return information from the club's public profile page; doesn't require login.

Specifically, returns these values:

- Club name
- Total club members (note that this isn't always a live value even if the club uses 
  the Club Management Tool to manage members)


## Example scripts

You'll need to copy `config_dist.ini`, rename to `config.ini` and populate it with club
ID and (optionally) credentials.

`example_private_member_counts.py` loads  club ID and credentials from `config.ini`.
It then retrieves and prints the number of active, expired and new/pending club member
counts from the club's Club Manager pages. 

`example_public_club_info.py` loads club ID from `config.ini`. It then retrieves and
prints the club name and 'total member count' from the club's public profile page.


