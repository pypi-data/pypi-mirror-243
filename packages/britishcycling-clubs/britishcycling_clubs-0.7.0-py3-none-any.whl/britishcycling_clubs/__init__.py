"""Module with functions to retrieve information about a club."""

from __future__ import annotations

import logging
import time
from typing import TypedDict

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from playwright.sync_api import sync_playwright

PROFILE_BASE_URL = "https://www.britishcycling.org.uk/club/profile/"
MANAGER_BASE_URL = "https://www.britishcycling.org.uk/uac/connect?success_url=/dashboard/club/membership?club_id="
REQUESTS_TIMEOUT = 10  # For `requests` library operations

log = logging.getLogger(__name__)


class PublicClubInfo(TypedDict):
    """Return type for `get_public_club_info()` function."""

    club_name: str
    total_members: int


def get_private_member_counts(
    club_id: str,
    username: str,
    password: str,
    manager_page_load_delay: int = 5,
) -> dict[str, int]:
    """Get number of active, pending, expired members from the club manager page.

    This is a slow operation (circa 10s), so get them all in one go.
    From the club manager page, return the values from these tabs:

    - 'Active Club Members'
    - 'New [i.e. pending] Club Subscriptions'
    - 'Expired Club Members'

    Parameters
    ----------
    club_id
        From the URL used to access club pages.

    username
        Username

    password
        Password

    manager_page_load_delay
        Time (s) allowed for club manager page to load. Defaults to 5.
        Consider increasing if 'Active member count was zero' exceptions occur.

    Returns
    -------
    dict[str, int]
        keys: 'active', 'pending', 'expired'
        values: corresponding ints

    Raises
    ------
    ValueError if zero 'active members' would be returned, as this probably means
    values hadn't populated correctly.

    """
    start_time = time.time()
    _log_info("Started timer for Playwright operations", start_time)

    club_manager_url = f"{MANAGER_BASE_URL}{club_id}/"

    start_time = time.time()
    _log_info("Started timer for Playwright operations", start_time)

    with sync_playwright() as p:
        _log_info("Launching browser", start_time)
        browser = p.chromium.launch()
        page = browser.new_page()

        # login page
        page.goto(club_manager_url)
        page.locator("id=username2").fill(username)
        page.locator("id=password2").fill(password)
        page.locator("id=login_button").click()
        _log_info("Got club manager page; logging in", start_time)

        # allow time for club manager page to load fully,
        # as page.wait_for_load_state() is ineffective
        _log_info(
            f"Waiting extra {manager_page_load_delay} s for page load",
            start_time,
        )
        time.sleep(manager_page_load_delay)

        raw_member_counts = {
            "active": page.locator("id=members-active-count").inner_text(),
            "pending": page.locator("id=members-new-count").inner_text(),
            "expired": page.locator("id=members-expired-count").inner_text(),
        }

        _log_info("Raw data retrieved", start_time)
        browser.close()
        _log_info("Closed browser", start_time)

        # Raw values will be blank if there aren't any members (although they appear
        # as zeros during page load); convert to 0 and ensure ints.
        member_counts = {}
        for key, value in raw_member_counts.items():
            if value == "":
                member_counts[key] = 0
            else:
                member_counts[key] = int(value)

        # Raise exception if zero 'active members' value.
        # 'active' appears to be the slowest value to populate.
        # 'pending' will often be genuinely zero; 'expired' could be genuinely zero
        if member_counts["active"] == 0:
            error_message = (
                "Active member count was zero; assuming error. "
                f"{member_counts['active']=}; "
                f"{member_counts['pending']=}; "
                f"{member_counts['expired']=}. "
                "Consider increasing `manager_page_load_delay`."
            )
            raise ValueError(error_message)

        return member_counts


def get_public_club_info(club_id: str) -> PublicClubInfo:
    """Return information from the club's public profile page.

    Parameters
    ----------
    club_id
        From the URL used to access club pages.

    Returns
    -------
    PublicClubInfo
    """
    profile_page = requests.get(
        f"{PROFILE_BASE_URL}{club_id}/",
        timeout=REQUESTS_TIMEOUT,
    )
    profile_soup = BeautifulSoup(profile_page.content, "html.parser")
    return {
        "club_name": _get_club_name_from_profile(profile_soup),
        "total_members": _get_total_members_from_profile(profile_soup),
    }


def _get_club_name_from_profile(soup: BeautifulSoup) -> str:
    """Return the club's name from BeautifulSoup object."""
    club_name_h1 = soup.find("h1", class_="article__header__title-body__text")

    # For type-checking purposes: ensures unambiguous type is passed
    if not isinstance(club_name_h1, Tag):
        raise TypeError

    # For type-checking purposes: ensures unambiguous type is passed
    if not isinstance(club_name_h1.string, str):
        raise TypeError

    return club_name_h1.string


def _get_total_members_from_profile(soup: BeautifulSoup) -> int:
    """Return the club's total members count from BeautifulSoup object."""
    about_div = soup.find("div", id="about")

    # TypeError is raised if page other than a club profile page is returned
    # e.g. club_id is incorrect; club's profile is offline pending reaffiliation
    # Consider checking URL returned as a more explicit check
    if not isinstance(about_div, Tag):
        raise TypeError

    # TypeError raised if string is not found as exact tag content
    member_count_label = about_div.find(string="Total club members:")
    if not isinstance(member_count_label, NavigableString):
        raise TypeError

    member_count_label_outer = member_count_label.parent

    # For type-checking purposes: ensures unambiguous type is passed
    if not isinstance(member_count_label_outer, Tag):
        raise TypeError

    member_count_label_outer2 = member_count_label_outer.parent

    # For type-checking purposes: ensures unambiguous type is passed
    if not isinstance(member_count_label_outer2, Tag):
        raise TypeError

    strings = list(member_count_label_outer2.strings)
    return int(strings[-1])


def _log_info(message: str, start_time: float) -> None:
    """Add INFO level log entry, with elapsed time since `start_time`."""
    elapsed_time = time.time() - start_time
    log_message = f"Elapsed: {elapsed_time:.1f} s. {message}"
    log.info(log_message)
