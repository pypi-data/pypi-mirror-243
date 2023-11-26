from mediagrab.content import Content
from mediagrab.parser import parser


def main():
    args: dict = vars(parser.parse_args())
    video = Content(**args)
    video.download()


if __name__ == "__main__":
    main()
