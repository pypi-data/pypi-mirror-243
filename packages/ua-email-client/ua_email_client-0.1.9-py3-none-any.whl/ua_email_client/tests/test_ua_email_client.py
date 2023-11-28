import os
import json
from unittest import TestCase
from nose.tools import raises
from ua_email_client import ua_email_client


class TestEmailClient(TestCase):
    def setUp(self):
        token_path = os.path.join(
            os.path.split(__file__)[0], "email_creds.json")
        with open(token_path, 'r') as file:
            creds = json.loads(file.read())

        self.email = creds["email"]
        self.default_recipient = creds["default_recipient"]
        self.secondary_recipient = creds["secondary_recipient"]

        self.email_client = ua_email_client.EmailClient(self.email)

    def test_add_template(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)

        assert self.email_client.templates.get("test_template") is not None

    @raises(ua_email_client.ImproperTemplateNameException)
    def test_add_improper_template_name(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "invalid.template.html")
        self.email_client.add_template(template_path)

    @raises(ua_email_client.ImproperTemplateNameException)
    def test_add_improper_template_file_type(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "invalid_type.md")
        self.email_client.add_template(template_path)

    @raises(ua_email_client.DuplicateTemplateException)
    def test_add_duplicate_template(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)
        assert self.email_client.templates.get("test_template") is not None
        self.email_client.add_template(template_path)

    def test_send_email(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)

        self.email_client.send_email(
            self.default_recipient,
            "test_template",
            "UA-Email-Client Test Suite Email",
            {
                "content": "This is a test"
            }
        )

    def test_send_email_with_multiple_recipients(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)

        self.email_client.send_email(
            [self.default_recipient, self.secondary_recipient],
            "test_template",
            "UA-Email-Client Test Suite Email",
            {
                "content": "This is a test"
            }
        )

    @raises(TypeError)
    def test_send_email_with_bad_data_type(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)

        self.email_client.send_email(
            self.default_recipient,
            "test_template",
            "UA-Email-Client Test Suite Email",
            "data"
        )

    @raises(TypeError)
    def test_send_email_with_bad_receiver_type(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)

        self.email_client.send_email(
            None,
            "test_template",
            "UA-Email-Client Test Suite Email",
            {
                "content": "This is a test"
            }
        )

    def test_send_email_without_data(self):
        template_path = os.path.join(
            os.path.split(__file__)[0], "templates", "test_template.html")
        self.email_client.add_template(template_path)

        self.email_client.send_email(
            self.default_recipient,
            "test_template",
            "UA-Email-Client Test Suite Email",
            None
        )
