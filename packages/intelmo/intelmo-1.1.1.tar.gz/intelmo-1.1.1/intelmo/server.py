from typing import List
from string import punctuation
from heapq import nlargest
from collections import Counter
from typing import Union
from nicegui import ui
from .webui import rss_page, reader_page
from .models.task import InteractiveTaskConfiguration, TaskModelConfiguration, Composition, Compatible


class Server:
    def __init__(self, configuration: TaskModelConfiguration, debug: bool = False):
        self.configuration = configuration

    def create_routes(self):
        @ui.page('/')
        def rss_page_index():
            return rss_page.content()

        @ui.page('/{rss_source_id}')
        def rss_page_feed(rss_source_id: str):
            return rss_page.detail_content(rss_source_id)

        @ui.page('/reader/article')
        def reader_article(url: str):
            functions = self.configuration.task_tree.get_leaves()
            return reader_page.content(url, functions, self.configuration)

    def run(self):
        self.create_routes()
        ui.run(
            title=self.configuration.name if self.configuration.name else "INTELMO",
            storage_secret="intelmo",
        )


def create_server(name: str, description: str,
                  tasks: Union[InteractiveTaskConfiguration, Composition]):
    return Server(TaskModelConfiguration(name, description, tasks))

###
# Example below
###


# Note: a class is not required by packages, but it is recommended to use one for better organization
