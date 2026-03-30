import argparse
import sys

import uvicorn

from config import get_settings


def run_api() -> None:
    settings = get_settings()
    uvicorn.run(
        "backend.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )


def run_ui() -> None:
    import streamlit.web.cli as stcli

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
    args = build_parser().parse_args()
    if args.target == "ui":
        run_ui()
        return
    run_api()


if __name__ == "__main__":
    main()
