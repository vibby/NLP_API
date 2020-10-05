"""The entrypoint for starting NLPAPI."""
import argparse
import logging
import sys

# Is there a better way to do this?
try:

    # If running from deployment
    from .nlp_api import NLPAPI

except ImportError as e:

    # If running from source.
    from nlp_api import NLPAPI


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
        help='The host NLP-API should run on. Defaults to localhost.')

    arg_parser.add_argument(
        'port',
        nargs='?',
        type=int,
        default=8888,
        help='The port NLP-API should be available on. Defaults to 8888.')

    arg_parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Whether or not to provide verbose logging output when running NLP-API.')

    args = arg_parser.parse_args()

    return args.host, args.port, args.verbose


def main():
    """The main method, starts NLPAPI.
    """
    logging.debug('Entering main method')

    host, port, is_verbose = gather_args()

    logging_level = logging.INFO if not is_verbose else logging.DEBUG

    logging.basicConfig(level=logging_level)

    nlp_api = NLPAPI()

    logging.debug(f'Starting NLPAPI with params: [HOST: {host}, PORT: {port}]')

    nlp_api.run(host=host, port=port, debug=True)


if __name__ == "__main__":
    """The main entry point for NLPAPI.
    """

    sys.exit(main())  # pragma: no cover
