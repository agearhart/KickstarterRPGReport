import requests
import logging
import json

from lxml import html
from typing import List
from kickstarter_project import KickstarterProject

kickstarter_rpg_query = "https://www.kickstarter.com/discover/advanced?state=live&term=rpg&category_id=34&sort=newest&page="
parsed_projects: List[KickstarterProject] = []


def get_next_page(last_page: int) -> str:
    """Given the last page number fetched; fetch the next page"""
    current_page: int = last_page + 1
    logging.info("Fetching Page {}".format(current_page))

    url: str = kickstarter_rpg_query + str(current_page)
    response = requests.get(url)
    if response.ok:
        return response.content
    else:
        return None


def get_projects_from_page(page: str) -> List[dict]:
    """Scrape the webpage passed in for projects

    Using methods learned from https://docs.python-guide.org/scenarios/scrape/
    """
    xml_tree = html.fromstring(page)
    project_divs = xml_tree.xpath('//div/@data-project')  # get all the div tags containing data-project attributes
    project_dicts: List[dict] = []

    for project in project_divs:
        new_dict = json.loads(project)
        project_dicts.append(new_dict)

    return project_dicts


def main():
    page_count: int = 0
    last_page_project_count:int = 1 # a white lie to allow processing of the first loop

    while last_page_project_count > 0:
        page: str = get_next_page(page_count)
        projects: List[dict] = get_projects_from_page(page)
        last_page_project_count = len(projects)

        if last_page_project_count is not 0:
            page_count += 1
            for project in projects:
                parsed_projects.append(KickstarterProject(project))

    logging.info("Processed {} pages for {} projects".format(page_count, len(parsed_projects)))

    print(KickstarterProject.print_header())
    print(KickstarterProject.print_header_divider())

    for project in parsed_projects:
        print(project.to_markdown_string())


if __name__ == "__main__":
    main()
