from datetime import datetime


class KickstarterProject:
    """Kickstarter project details"""

    def __init__(self, raw_details: dict):
        """Constructor accepting dictionary of project details supplied from XPath query of raw HTML page

        :param raw_details:
        """
        self.raw_details: dict = raw_details                                  # cache of the raw dictionary for science
        self.id: int = raw_details.get('id')                                  # Kickstarter ID of the project
        self.name: str = raw_details.get('name')                              # Name of the project
        self.blurb: str = raw_details.get('blurb')                            # short description of the project
        self.goal: float = raw_details.get('goal')                            # how much was asked for
        self.currency: str = raw_details.get('currency_symbol')               # default project currency
        self.pledged: float = raw_details.get('pledged')                      # how much has been raised
        self.percent_funded = self.pledged / self.goal * 100                  # how funded is the project
        self.deadline_epoch_seconds = raw_details.get('deadline')             # epoch seconds of deadline
        self.backers_count = raw_details.get('backers_count')                 # how many people have backed so far
        self.average_back_value = self.pledged / self.backers_count           # average pledge amount
        self.project_url = raw_details.get('urls').get('web').get('project')  # project url

    @staticmethod
    def print_header() -> str:
        return 'Project | Blurb | Goal | Pledged | Funded % | Average Pledge | Ending | Backers'

    @staticmethod
    def print_header_divider() -> str:
        return '--------------------|----------------------------------------|--------------------|--------------------|-----|--------------------|--------------------|----------'

    def to_markdown_string(self) -> str:
        """Print the Markdown String for a table row of this project"""
        deadline: datetime = datetime.utcfromtimestamp(self.deadline_epoch_seconds)
        deadline_str: str = deadline.strftime("%Y-%m-%d %H:%M:%S")

        return "[{}]({})|{}|{}|{}|{}|{}|{}|{}".format(
            self.name,
            self.project_url,
            self.blurb,
            self.currency + str(self.goal),
            self.currency + str(self.pledged),
            str(self.percent_funded),
            self.currency + str(self.average_back_value),
            deadline_str,
            self.backers_count)
