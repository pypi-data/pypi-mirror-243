""" Client to send emails using AWS. """

from datetime import datetime
from jinja2 import Template
import boto3
from botocore.exceptions import ClientError


class DuplicateTemplateException(Exception):
    """ You tried to add a template that already exists. """


class EmailFailedToSendException(Exception):
    """ Email failed to send. """


class ImproperTemplateNameException(Exception):
    """ The template that was used is not valid. """


class EmailClient():
    """ A simple email client for AWS SES system."""

    def __init__(self, sender, region_name="us-west-2", aws_access_key=None, aws_secret_key=None):
        self.sender = sender
        self.templates = dict()
        self.subjects = dict()

        if (aws_access_key and aws_secret_key): # AWS credentials provided
            self.client = boto3.client(
                "ses",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region_name
            )
        else: # Already inside AWS, no credentials needed
            self.client = boto3.client('ses', region_name=region_name)

    def add_template(self, template):
        """
        Adds a template for emails to use.

        Arguments:
            template (string): The name of the template to use.
        """
        template_file = template.split("/")[-1]
        template_name = template_file.split(".")
        if len(template_name) != 2:
            raise ImproperTemplateNameException(
                "That template has an invalid name!")
        elif template_name[1] != "html" and template_name[1] != "xml":
            raise ImproperTemplateNameException(
                "That template is not the correct file type!")
        else:
            template_name = template_name[0]

        if self.templates.get(template_name):
            raise DuplicateTemplateException(
                "That template name has already been created!")

        with open(template, 'r') as file:
            template = Template(file.read())
        self.templates[template_name] = template

    def send_email(self, receiver, template, subject, data, use_template=True):
        """
        Sends an email using AWS.

        Arguments:
            receiver (string or list): The emails to send this email to.
            template (string): The template to use for this email.
            subject (string): The subject of the email.
            data (dict or string):
                The information to be populated in the template (use_template=True)
                OR The message to be emailed directly (use_template = False)
            use_template (bool): Whether or not to use a template

        Raises:
            EmailFailedToSendException: The email couldn't be sent.
        """
        if type(receiver) is not list and type(receiver) is not str:
            raise TypeError("Receiver must be a list or string!")

        if type(receiver) == str:
            receiver = [receiver]

        if self.subjects.get(subject):
            subject = self.subjects[subject]

        if not data:
            data = dict()

        if use_template:
            body = self.templates[template].render(**data)
            message_type = "Html"
        else:
            body = data
            message_type = "Text"
            # Check for passed in Html string
            if body:
                if len(body) > 5:
                    if (body[0:6].lower() == "<html>"):
                        message_type = "Html"

        try:
            self.client.send_email(
                Destination={'ToAddresses': receiver},
                Message={
                    'Body': {
                        message_type: {
                            'Charset': "UTF-8",
                            'Data': body
                        },
                    },
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    },
                },
                Source=self.sender,
            )
        # Display an error if something goes wrong.
        except ClientError:
            print(f"Failed to send email to {receiver} at {datetime.now()}.")
            raise EmailFailedToSendException() from None
        else:
            print(f"Sent email to {receiver} about {data} at{datetime.now()}.")

