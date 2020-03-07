class KickstarterProject:
    """An individual Kickstarter Project parsed out from a KickstarterPage"""

    def __init__(self, project_text: str):
        """Constructor

        :param project_text: the raw div tag that contains a kickstarter project
        """
        self.project_text = project_text
