import argparse
import pathlib

parser = argparse.ArgumentParser()

parser.add_argument(
    "url",
    type=str,
    help="URL of video on YouTube to download",
)

parser.add_argument(
    "-d",
    "--destination",
    type=pathlib.Path,
    help="destination path",
    required=False,
)
