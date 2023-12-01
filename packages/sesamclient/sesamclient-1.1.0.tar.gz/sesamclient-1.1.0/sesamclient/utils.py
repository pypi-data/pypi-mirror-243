# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import inspect
import itertools
import os.path
import json
import logging

from . import exceptions
from configparser import ConfigParser

logger = logging.getLogger(__name__)


def validate_in(key, mapping):
    if key not in mapping:
        raise AssertionError("The key '%s' was not found in the mapping %s!" % (key, mapping))


def validate_response_is_ok(response, allowable_response_status_codes=frozenset([200])):
    if isinstance(allowable_response_status_codes, int):
        allowable_response_status_codes = {allowable_response_status_codes}
    if response.status_code not in allowable_response_status_codes:
        if response.status_code == 403:
            exception_class_to_use = exceptions.ForbiddenException

        elif 400 <= response.status_code <= 499:
            exception_class_to_use = exceptions.BadRequestException

        elif response.status_code == 503:
            exception_class_to_use = exceptions.ServiceUnavailable

        else:
            exception_class_to_use = exceptions.InternalServerError

        try:
            response_text = response.content.decode("utf-8")
        except:
            response_text = response.text

        raise exception_class_to_use(
            """response.status_code(%s) not in allowable_response_status_codes(%s) for the url\
             '%s' (request method:'%s'). response.content:\n%s""" % (
                response.status_code, allowable_response_status_codes,
                response.url,
                response.request.method,
                response_text[:1000]),
            response=response
        )

    if is_called_by_unittest():
        # The sesamclient is being used by a ci-test, so do some additional checks.
        # check for headers with duplicate values

        # We must skip a couple of special case nodes that runs an old version of the code.
        url = response.request.url
        if not ("_msgpack-version-1" in url or "_msgpack-version-2" in url):
            for header_name, header_value in response.headers.items():
                if header_value:
                    header_values = header_value.split(",")
                    header_values_set = set()
                    for value in header_values:
                        value = value.strip()
                        if value in header_values_set:
                            raise AssertionError(
                                "Got a duplicate value '%s' in the '%s' response header for the url '%s'! "
                                "Header value: '%s'" % (
                                    value, header_name, response.request.url, header_value))
                        header_values_set.add(value)


def parse_json_response(response):
    """Utility-function for parsing a http response as json and reporting any parsing-errors in a human-readable
    way. The response.json() method doesn't give very helpful error-messages.

    :param response: The http response object
    :return: The response.content parsed as json
    """
    try:
        return response.json()
    except Exception as e:
        try:
            response_text = response.content.decode("utf-8")
        except:
            response_text = response.text

        raise AssertionError(
            """Failed to parse the response as json for the url\
             '%s' (request method:'%s'): %s. response.content:\n%s""" % (
                response.url,
                response.request.method,
                e,
                response_text[:1000]))


def validate_equal_case_insensitive(expected, actual, msg=None):
    if isinstance(expected, str) and isinstance(actual, str):
        if expected.lower() == expected.lower():
            # the arguments are strings and they are the same when ignoring case.
            return
    if msg:
        raise AssertionError("""actual(%s) != expected(%s)! %s""" % (actual, expected, msg))
    else:
        raise AssertionError("""actual(%s) != expected(%s)""" % (actual, expected))


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')) as version_file:
        return version_file.read().strip()


def read_config_file(filename):
    file_config = {}
    try:
        curr_dir = os.getcwd()

        # Find config on disk, if any
        parents_dirs: list[str] = os.path.abspath(curr_dir).split(os.sep)[1:]
        parent_path = curr_dir
        if os.path.isfile(filename):
            file_config = parse_config_file(filename)
        else:
            # iterate over all parent directories and look for .syncconfig file
            for _ in parents_dirs:
                parent_path = os.path.dirname(parent_path)
                file_path = os.path.join(parent_path, filename)
                if os.path.isfile(file_path):
                    file_config = parse_config_file(file_path)
                    if file_config:
                        curr_dir = parent_path
                        break

        if file_config:
            logger.debug("Found config file '%s' in '%s'" % (filename, curr_dir))
        else:
            logger.debug("Cannot locate config file '%s' in current or parent folder. "
                         "Proceeding without it." % filename)
    except BaseException as e:
        logger.exception(f"Failed to read '{filename}' from either the current directory or the "
                         "parent directory. Check that you are in the correct directory, that "
                         "you have the required permissions to read the files and that the files "
                         "have the correct format.")

    return file_config


def parse_config_file(filename):
    config = {}
    # try to parse as json, if fails parse as ini
    with open(filename, "r") as fp:
        try:
            config = json.load(fp)
        except ValueError:
            pass
    if not config:
        with open(filename) as fp:
            parser = ConfigParser(strict=False)
            # [sesam] section is prepended to support .syncconfig file
            #  in which section is omitted
            parser.read_file(itertools.chain(["[sesam]"], fp), source=filename)
            config = {}
            for section in parser.sections():
                for key, value in parser.items(section):
                    config[key.lower()] = value

    return config


def get_node_and_jwt_token(node_url=None, jwt_token=None, config_filename='.syncconfig'):
    try:
        file_config = read_config_file(config_filename)
        if not node_url:
            node_url = os.environ.get("NODE", file_config.get("node"))

        if not jwt_token:
            jwt_token = os.environ.get("JWT", file_config.get("jwt"))

        if jwt_token and jwt_token.startswith('"') and jwt_token[-1] == '"':
            jwt_token = jwt_token[1:-1]

        if jwt_token.startswith("bearer "):
            jwt_token = jwt_token.replace("bearer ", "")

        if jwt_token.startswith("Bearer "):
            jwt_token = jwt_token.replace("Bearer ", "")

        node_url = node_url.replace('"', "")

        if not node_url.startswith("http"):
            node_url = f"https://{node_url}"

        if not node_url[-4:] == "/api":
            node_url = f"{node_url}/api"

    except BaseException as e:
        logger.exception(f"Failed getting node_url and/or jwt_token: {e}")

    return node_url, jwt_token


_is_called_by_unittest = None

def is_called_by_unittest():
    global _is_called_by_unittest
    if _is_called_by_unittest is None:
        stack = inspect.stack()
        if any(x[0].f_globals['__name__'].startswith('nose.') for x in stack):
            _is_called_by_unittest = True
        else:
            _is_called_by_unittest = any(x[0].f_globals['__name__'].startswith('_pytest') for x in stack)
    return _is_called_by_unittest
