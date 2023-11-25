from ..plugins.web_crawler import RemaxExecutor


class Extract:
    @classmethod
    def get_listing_data(cls, pages: list, multithreaded: bool) -> list:
        RemaxExecutor(multithreaded=multithreaded).get_multipage_listing(
            pages=pages, output=True, filename="output_1.json"
        )

    @classmethod
    def get_total_pages(cls) -> int:
        return RemaxExecutor().get_total_pages()
