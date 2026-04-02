import argparse
import logging
import sys

import uvicorn

from config import get_settings
from logging_config import configure_logging, get_logger


logger = get_logger(__name__)


def run_api() -> None:
    settings = get_settings()
    logger.info("Starting API server on %s:%s", settings.api_host, settings.api_port)
    uvicorn.run(
        "backend.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )


def run_ui() -> None:
    import streamlit.web.cli as stcli

    logger.info("Starting Streamlit UI")
    sys.argv = ["streamlit", "run", "frontend/ui.py"]
    raise SystemExit(stcli.main())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TextForge central entry point.")
    parser.add_argument(
        "target",
        nargs="?",
        default="api",
        choices=["api", "ui"],
        help="Choose whether to run the API or the UI.",
    )
    return parser


def main() -> None:
    configure_logging(logging.INFO)
    args = build_parser().parse_args()
    logger.info("Application entrypoint invoked with target=%s", args.target)
    if args.target == "ui":
        run_ui()
        return
    run_api()


if __name__ == "__main__":
    main()
