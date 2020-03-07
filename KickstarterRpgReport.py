import requests
import logging

from kickstarterproject import KickstarterProject
from typing import List

kickstarter_rpg_query = "https://www.kickstarter.com/discover/advanced?state=live&term=rpg&category_id=34&sort=newest&page="
pages: List[str] = []
parsed_projects: List[KickstarterProject] = []


def get_next_page(last_page: int) -> str:
    """Give the last page number fetched; fetch the next page"""
    url: str = kickstarter_rpg_query + str(last_page + 1)
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        return None


def get_projects_from_page(page: str) -> List[str]:
    return []


def main():
    page_count: int = 0
    continue_fetching: bool = True

    while continue_fetching:
        page: str = get_next_page(page_count)
        projects = get_projects_from_page(page)
        if len(projects) is not 0:
            continue_fetching = False
        else:
            ++page_count
            for project in projects:
                parsed_projects.append(KickstarterProject(project))

    logging.info("Processed {} pages".format(page_count))


if __name__ == "__main__":
    main()
