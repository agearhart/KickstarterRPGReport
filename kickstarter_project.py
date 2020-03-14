from datetime import datetime


class KickstarterProject:
    """Kickstarter project details"""

    def __init__(self, raw_details: dict):
        """Constructor accepting dictionary of project details supplied from XPath query of raw HTML page

        :param raw_details:
        """
        self.raw_details: dict = raw_details  # cache of the raw dictionary for science
        self.id: int = raw_details.get('id')  # Kickstarter ID of the project

        # Name of the project with whitespace and unicode characters removed
        self.name: str = raw_details.get('name').rstrip().encode('ascii', 'ignore').decode('unicode_escape')

        # short description of the project with whitespace and unicode characters removed
        self.blurb: str = raw_details.get('blurb').rstrip().encode('ascii', 'ignore').decode('unicode_escape')

        self.goal: float = raw_details.get('goal')               # how much was asked for
        self.currency: str = raw_details.get('currency_symbol')  # default project currency
        self.pledged: float = raw_details.get('pledged')         # how much has been raised
        self.percent_funded = self.pledged / self.goal * 100     # how funded is the project

        # project end date
        self.deadline_epoch: datetime = datetime.utcfromtimestamp(raw_details.get('deadline'))

        # date when project was launched
        self.launched_epoch: datetime = datetime.utcfromtimestamp(raw_details.get('launched_at'))

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
        deadline_str: str = self.deadline_epoch.strftime("%Y-%m-%d %H:%M:%S")

        return "[{}]({})|{}|{}|{}|{}|{}|{}|{}".format(
            self.name,
            self.project_url,
            self.blurb,
            self.currency + ('%.2f' % self.goal),
            self.currency + ('%.2f' % self.pledged),
            ('%.0f' % self.percent_funded) + '%',
            self.currency + ('%.2f' % self.average_back_value),
            deadline_str + ' UTC',
            self.backers_count)
