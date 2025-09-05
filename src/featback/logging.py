import logging

import structlog


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    structlog.configure(
        processors=[structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    )
