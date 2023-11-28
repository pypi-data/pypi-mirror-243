from __future__ import absolute_import, division, print_function

import json
import logging
import os
import re
import stat
import sys
import subprocess
from six.moves.urllib.parse import urlencode

from locker import ROOT_PATH, util, error


class BinaryAdapter(object):
    def __init__(self, access_key_id=None, access_key_secret=None, api_base=None, api_version=None, headers=None,
                 logger=None):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.api_base = api_base
        self.api_version = api_version
        self.headers = headers
        self.system_platform = self.get_platform()
        self.logger = logger or logging.getLogger("locker")

    @classmethod
    def make_executable(cls, path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

    @staticmethod
    def get_platform():
        # Return darwin/win32/linux
        return sys.platform

    @staticmethod
    def get_sdk_version():
        _about_file = os.path.join(ROOT_PATH, "__about__.json")
        with open(_about_file, 'r') as fd:
            version = json.load(fd).get("version")
        return version

    def get_binary_file(self):
        # Checking the os system, returns the corresponding binary
        # OS X
        if self.system_platform == "darwin":
            return os.path.join(ROOT_PATH, "bin", "locker_mac")
        # Windows
        elif self.system_platform == "win32":
            return os.path.join(ROOT_PATH, "bin", "locker_windows.exe")
        # Default is linux
        else:
            return os.path.join(ROOT_PATH, "bin", "locker_linux")

    def call(
        self,
        cli,
        params=None,
        asjson=True,
        shell=True,
        timeout=30,
        skip_cli_lines=0
    ):
        binary_file = self.get_binary_file()
        if binary_file:
            self.make_executable(binary_file)
        # if self.access_key:
        #     my_access_key = self.access_key
        # else:
        #     from locker import access_key
        #     my_access_key = access_key
        my_access_key_id = self.access_key_id
        my_access_key_secret = self.access_key_secret
        if my_access_key_id is None or my_access_key_secret is None:
            raise error.AuthenticationError(
                "No Access key provided. (HINT: set your API key using "
                '"locker.access_key_id = <ACCESS-KEY-ID>" and "locker.access_key_secret = <ACCESS-KEY-SECRET>"). '
                "You can generate Access Key from the Locker Secret web interface."
            )
        my_headers = self.headers or {}
        # default_user_agent = f"Python{sys.version_info[0]}"
        default_client_agent = f"Python - {self.get_sdk_version()}"
        command = f'{binary_file} {cli} ' \
                  f'--access-key-id "{my_access_key_id}" ' \
                  f'--access-key-secret "{my_access_key_secret}" ' \
                  f'--api-base {self.api_base} ' \
                  f'--agent "{default_client_agent}" ' \
                  f'--verbose'

        if my_headers:
            if isinstance(my_headers, dict):
                my_headers_list = [f"{k}:{v}" for k, v in my_headers.items()]
                my_headers = ",".join(my_headers_list)
            command += f' --headers "{my_headers}"'
        else:
            command += ' --headers ""'

        # Building full command with params
        post_data = None
        if "get" in cli or "delete" in cli:
            encoded_params = urlencode(list(util.api_encode(params or {})))
            # Don't use strict form encoding by changing the square bracket control
            # characters back to their literals. This is fine by the server, and
            # makes these parameter strings easier to read.
            encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")
            # TODO: Build api url by passing filter params to command
            # if params:
            #     abs_url = _build_api_url(abs_url, encoded_params)
            pass
        elif "update" in cli or "create" in cli:
            post_data = json.dumps(json.dumps(params or {}))
        if post_data:
            command += f' --data {post_data}'

        self.logger.debug(f"[+] Running cli command: {command}")
        try:
            raw = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT, shell=shell, universal_newlines=True, timeout=timeout
            )
        except subprocess.TimeoutExpired as e:
            exc = error.CliRunError(e.stdout)
            exc.process = e
            raise exc
        except subprocess.CalledProcessError as e:
            signs = ['"success": false', '"success": true', '"object": "error"']
            if any(s in e.output for s in signs):
                raw = e.output
            elif str(e.output).strip() == 'Killed' or 'returned non-zero exit status 1' in str(e):
                exc = error.CliRunError(e.stdout)
                exc.process = e
                raise exc
            else:
                self.logger.warning(f"[!] subprocess.CalledProcessError: {e} {e.output}. The command is: {command}")
                exc = error.CliRunError(e.stdout)
                exc.process = e
                raise exc
        return self.interpret_response(res_body=raw, asjson=asjson, skip_cli_lines=skip_cli_lines)

    def interpret_response(self, res_body, asjson=True, skip_cli_lines=0):
        # Skip cli lines
        if skip_cli_lines > 0:
            res_body = res_body.split("\n", skip_cli_lines)[skip_cli_lines]
        # Log break
        try:
            res_body = res_body.split("----------- LOG BREAK -----------")[1]
        except IndexError:
            pass
        if not asjson:
            return res_body
        try:
            if hasattr(res_body, "decode"):
                res_body = res_body.decode("utf-8")
        except Exception:
            self.logger.warning(f"[!] Invalid decode response body from CLI:::{res_body}")
            exc = error.CliRunError(
                f"Invalid decode response body from CLI: {res_body}",
                res_body
            )
            exc.process = res_body
            raise exc
        try:
            res_body = json.loads(res_body)
        except json.decoder.JSONDecodeError:
            self.logger.warning(f"[!] CLI result json decode error:::{res_body}")
            exc = error.CliRunError(
                f"CLI JSONDecodeError:::{res_body}", res_body
            )
            exc.process = res_body
            raise exc
        if self._should_handle_as_error(res_body):
            res_body.update({"object": "error"})
            self.handle_error_response(res_body)
        return res_body

    @staticmethod
    def _should_handle_as_error(res_body):
        try:
            return res_body.get("object") == "error" or res_body.get("success") is False or\
                res_body.get("success") == "false"
        except AttributeError:
            return False

    def handle_error_response(self, res_body):
        exc = self.specific_cli_error(error_data=res_body)
        raise exc

    def specific_cli_error(self, error_data):
        self.logger.info(f"[!] CLI return error object:::{error_data}")
        status_code = error_data.get("status_code")
        error_code = error_data.get("error")
        if status_code == 429 or error_code == "rate_limit":
            return error.RateLimitError(
                error_data.get("message"), error_data
            )
        elif status_code == 401 or error_code == "unauthorized":
            return error.AuthenticationError(
                error_data.get("message"), error_data
            )
        elif status_code == 403 or error_code == "permission_denied":
            return error.PermissionDeniedError(
                error_data.get("message"), error_data
            )
        else:
            return error.APIError(
                error_data.get("message"), error_data
            )
