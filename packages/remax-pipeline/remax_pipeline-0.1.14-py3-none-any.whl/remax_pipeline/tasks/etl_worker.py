from ..pipe import Extract


def start_worker(pages: list):
    return Extract.get_listing_data(pages=pages, multithreaded=True)
