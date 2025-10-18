import collections
import hashlib
import hmac
import logging
import json
import six
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading

try:
    config = json.loads(open("./plugin/conf/OlivaGithub/config.json", "r").read())
    path = config['settings']['path']
except:
    path = "/webhook"


class Webhook(object):
    """
    Construct a webhook using Python's built-in http.server.

    :param endpoint: the endpoint for the registered URL rule
    :param secret: Optional secret, used to authenticate the hook comes from Github
    """

    def __init__(self, endpoint=path, secret=None):
        self.endpoint = endpoint
        self.secret = secret
        self._hooks = collections.defaultdict(list)
        self._logger = logging.getLogger("webhook")
        self._config = {}
        self._server = None
        self._thread = None

    def set_config(self, config):
        """Set the configuration dictionary"""
        self._config = config

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, secret):
        if secret is not None and not isinstance(secret, six.binary_type):
            secret = secret.encode("utf-8")
        self._secret = secret

    def hook(self, event_type="push"):
        """
        Registers a function as a hook. Multiple hooks can be registered for a given type, but the
        order in which they are invoke is unspecified.

        :param event_type: The event type this hook will be invoked for.
        """

        def decorator(func):
            self._hooks[event_type].append(func)
            return func

        return decorator

    def _get_digest(self, data):
        """Return message digest if a secret key was provided"""
        return hmac.new(self._secret, data, hashlib.sha1).hexdigest() if self._secret else None

    def _process_webhook(self, headers, body):
        """Process the webhook request"""
        digest = self._get_digest(body)

        if digest is not None:
            sig_header = headers.get('X-Hub-Signature', '')
            sig_parts = sig_header.split("=", 1)
            if not isinstance(digest, six.text_type):
                digest = six.text_type(digest)

            if len(sig_parts) < 2 or sig_parts[0] != "sha1" or not hmac.compare_digest(sig_parts[1], digest):
                return 400, "Invalid signature"

        event_type = headers.get('X-Github-Event')
        if not event_type:
            return 400, "Missing header: X-Github-Event"

        try:
            data = json.loads(body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return 400, "Request body must contain json"

        delivery_id = headers.get('X-Github-Delivery', 'unknown')
        self._logger.info("%s (%s)", _format_event(event_type, data), delivery_id)

        for hook in self._hooks.get(event_type, []):
            hook(data)

        return 204, ""

    def run(self, host='0.0.0.0', port=3000):
        """Start the HTTP server"""
        webhook_instance = self

        class WebhookHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                """Handle GET requests"""
                parsed_path = urlparse(self.path)
                if parsed_path.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"<h1>Hi,I'm Listening...<h1>")
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):
                """Handle POST requests"""
                parsed_path = urlparse(self.path)
                
                if parsed_path.path != webhook_instance.endpoint:
                    self.send_response(404)
                    self.end_headers()
                    return

                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)

                status_code, message = webhook_instance._process_webhook(self.headers, body)

                self.send_response(status_code)
                self.end_headers()
                if message:
                    self.wfile.write(message.encode('utf-8'))

            def log_message(self, format, *args):
                """Override to use custom logger"""
                webhook_instance._logger.info("%s - - [%s] %s\n" %
                                             (self.address_string(),
                                              self.log_date_time_string(),
                                              format % args))

        self._server = HTTPServer((host, port), WebhookHandler)
        self._logger.info(f"Starting HTTP server on {host}:{port}")
        self._server.serve_forever()


def _format_event(event_type, data):
    EVENT_DESCRIPTIONS = {
        "commit_comment": "{comment[user][login]} commented on " "{comment[commit_id]} in {repository[full_name]}",
        "create": "{sender[login]} created {ref_type} ({ref}) in " "{repository[full_name]}",
        "delete": "{sender[login]} deleted {ref_type} ({ref}) in " "{repository[full_name]}",
        "deployment": "{sender[login]} deployed {deployment[ref]} to "
        "{deployment[environment]} in {repository[full_name]}",
        "deployment_status": "deployment of {deployement[ref]} to "
        "{deployment[environment]} "
        "{deployment_status[state]} in "
        "{repository[full_name]}",
        "fork": "{forkee[owner][login]} forked {forkee[name]}",
        "gollum": "{sender[login]} edited wiki pages in {repository[full_name]}",
        "issue_comment": "{sender[login]} commented on issue #{issue[number]} " "in {repository[full_name]}",
        "issues": "{sender[login]} {action} issue #{issue[number]} in " "{repository[full_name]}",
        "member": "{sender[login]} {action} member {member[login]} in " "{repository[full_name]}",
        "membership": "{sender[login]} {action} member {member[login]} to team " "{team[name]} in {repository[full_name]}",
        "page_build": "{sender[login]} built pages in {repository[full_name]}",
        "ping": "ping from {sender[login]}",
        "public": "{sender[login]} publicized {repository[full_name]}",
        "pull_request": "{sender[login]} {action} pull #{pull_request[number]} in " "{repository[full_name]}",
        "pull_request_review": "{sender[login]} {action} {review[state]} "
        "review on pull #{pull_request[number]} in "
        "{repository[full_name]}",
        "pull_request_review_comment": "{comment[user][login]} {action} comment "
        "on pull #{pull_request[number]} in "
        "{repository[full_name]}",
        "push": "{pusher[name]} pushed {ref} in {repository[full_name]}",
        "release": "{release[author][login]} {action} {release[tag_name]} in " "{repository[full_name]}",
        "repository": "{sender[login]} {action} repository " "{repository[full_name]}",
        "status": "{sender[login]} set {sha} status to {state} in " "{repository[full_name]}",
        "team_add": "{sender[login]} added repository {repository[full_name]} to " "team {team[name]}",
        "watch": "{sender[login]} {action} watch in repository " "{repository[full_name]}",
    }
    try:
        return EVENT_DESCRIPTIONS[event_type].format(**data)
    except KeyError:
        return event_type


# -----------------------------------------------------------------------------
# Copyright 2015 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------- END-OF-FILE -----------------------------------
