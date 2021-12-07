from argparse import ArgumentParser

from sqlparser import __version__ as version
from sqlparser.query import Query, create_query_dict
from sqlparser.utils import print_process_heading, print_query_dict
from sqlparser.validators import __all_validators__ as validator_list


def validate_query(query):
    context_text = "VALIDATION"
    print_process_heading(context_text)

    for validator_func in validator_list:
        validator_func(query)
        validator_func_name = validator_func.__name__
        print(f"{validator_func_name} successfully validated the query")


def run(args=None):
    arg_parser = ArgumentParser(
        description=f'SQL Parser - {version}',
        prog='sqlparser',
    )

    arg_parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'SQL Parser - {version}',
    )

    arg_parser.add_argument(
        '-q', '--query',
        type=str,
        help='SQL query to parse',
        required=True,
    )

    arg_parser.add_argument(
        '-vq', '--validate-query',
        action='store_true',
        help='Validate the query',
    )

    arg_parser.add_argument(
        '-r', '--raw-output',
        action="store_true",
        help="print raw query dict",
        default=False,
    )

    args = arg_parser.parse_args(args)
    should_validate = args.validate_query

    query = Query(args.query)

    if should_validate:
        validate_query(query)

    query_dict = create_query_dict(query)
    if args.raw_output:
        print(query_dict)
    else:
        print_query_dict(query_dict)


if __name__ == '__main__':
    run()
