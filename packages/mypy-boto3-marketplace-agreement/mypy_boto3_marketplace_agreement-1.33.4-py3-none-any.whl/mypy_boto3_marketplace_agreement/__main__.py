"""
Main CLI entrypoint.
"""

import sys


def print_info() -> None:
    """
    Print package info to stdout.
    """
    print(
        "Type annotations for boto3.AgreementService 1.33.4\nVersion:         1.33.4\nBuilder"
        " version: 7.21.0\nDocs:           "
        " https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_agreement//\nBoto3"
        " docs:     "
        " https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-agreement.html#AgreementService\nOther"
        " services:  https://pypi.org/project/boto3-stubs/\nChangelog:      "
        " https://github.com/youtype/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    """
    Print package version to stdout.
    """
    print("1.33.4")


def main() -> None:
    """
    Main CLI entrypoint.
    """
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
