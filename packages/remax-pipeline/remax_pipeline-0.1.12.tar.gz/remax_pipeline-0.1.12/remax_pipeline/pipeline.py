from .celery_app import run_etl_worker


def run(dev: bool = False):

    # workload = Extract.get_total_pages()
    pages = list(range(1, 27))

    action = {True: run_etl_worker, False: run_etl_worker.delay}

    return action[dev](pages)
