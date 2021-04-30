"""The entrypoint for starting nalapi."""
import argparse
import logging
import sys

# Is there a better way to do this?
try:

    # If running from deployment
    from .nalapi import nalapi

except ImportError as e:

    # If running from source.
    from nalapi import nalapi


def gather_args():
    """Gathers and returns the command line arguments via argparse.

    :return: The host and port provided by the user.
    :rtype: str, int
    """

    logging.debug('Gathering command line args.')

    arg_parser = argparse.ArgumentParser(
        description='A Bottle api for processing text with nlp.')

    arg_parser.add_argument(
        'host',
        nargs='?',
        default='localhost',
        help='The host nalapi should run on. Defaults to localhost.')

    arg_parser.add_argument(
        'port',
        nargs='?',
        type=int,
        default=8888,
        help='The port nalapi should be available on. Defaults to 8888.')

    arg_parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Whether or not to provide verbose logging output when running nalapi.')

    args = arg_parser.parse_args()

    return args.host, args.port, args.verbose


def main():
    """The main method, starts nalapi.
    """
    logging.debug('Entering main method')

    host, port, is_verbose = gather_args()

    logging_level = logging.INFO if not is_verbose else logging.DEBUG

    logging.basicConfig(level=logging_level)

    nalapiServer = nalapi()

    logging.debug('Starting nalapi with params: [HOST: {host}, PORT: {port}]')

    nalapiServer.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    """The main entry point for nalapi.
    """

    sys.exit(main())  # pragma: no cover
