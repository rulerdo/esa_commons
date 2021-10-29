from typing import Union
# SMTP
from smtplib import SMTP
# Message utils
from .EmailMessage import EmailAttachment, EmailMessageFactory


class EmailManager:
    """
    @version 1.0.1

    Class that provides email functionality, by encapsulating all the process and exposing only the 
    facade and setters we are able to hide the underlying complexity of this process, making it a lot
    easier to use.
    It supports basic text messages, as well as attachments. One important thing about attachments is
    that we don't need to worry about the MIMETypes, because they're inferred automatically, also, they
    are processed and attached automatically, so we just need to provide the path to the attachment, and
    the class will do all the required stuff under the hood.
    """
    
    def __init__(
        self,
        server: str,
        sender: str = None,
        target: Union[str, list] = None,
        subject: str = None,
        email_body: str = '',
        attachments: list = []
    ):
        """
        @param {str} server The SMTP server IP or domain.
        @param {str} sender The email user that sends the message.
        @param {str} target The email target user of the message.
        @param {str} subject The email subject.
        @param {str} email_body The email text body.
        @param {str} attachments The attachments list (path to the attachments, actually).
        """
        self.server = server
        self.sender = sender
        self.target = target
        self.subject = subject
        self.email_body = email_body
        self.attachments = attachments
        # To be set later
        self.root_message = None

    # Setters 

    def set_participants(
        self,
        sender: str,
        target: Union[str, list]
    ):
        """
        Sets the participants of the mail (to and from).
        """
        self.sender = sender
        self.target = target

    def set_subject(self, subject):
        """
        Sets the mail subject.
        """
        self.mail_subject = subject

    def set_email_body(self, email_body):
        """
        Sets the mail text body.
        """
        self.email_body = email_body
    
    def add_attachment(
        self, 
        attachment_path: str
    ):
        """
        Adds an attachment to the attachments list.
        """
        self.attachments.append(attachment_path)

    # Facade

    def send(self):
        """
        Facade method to send the email. It calls all the necessary method to, first validate the email
        components, create and initialize the root message (or email tree), attach the text message body,
        attach the attachments and send the message via the SMTP server.
        """
        # We perform a validation of the mandatory mail components (to, from and body)
        self.__validate_mail_components()
        # We create and initialize the root message (the email tree, which will contain the text body and the attachments)
        self.__initialize_root_message()
        # We attach the message body (provided as text) to the root message
        self.__attach_text_message_body()
        # We add the attachments to the root message
        self.__incorporate_attachments()
        # Finally, we actually send the mail
        self.__send_root_message_via_smtp()

    # Private methods

    def __initialize_root_message(self):
        """
        Creates and initialize a root message (MIMEMultipart), to support text and attachments.
        Also, the email data is set, such as email_to, email_from and the subject.
        """
        self.root_message = EmailMessageFactory.create_by_type(EmailMessageFactory.MULTIPART)
        self.root_message['To'] = self.target
        self.root_message['From'] = self.sender
        self.root_message['Subject'] = self.subject

    def __attach_text_message_body(self):
        """
        Attaches the provided text email body to the root message.
        """
        text_message_body = EmailMessageFactory.create_text_message(self.email_body)
        self.root_message.attach(text_message_body)

    def __incorporate_attachments(self):
        """
        Iterates through the attachments list, creating an EmailAttachment instance for each (this
        class prepares the attachment to be ready to be attached directly to the root message, without
        us having to worry about setting the content type, subtype, the file content or the encoding and
        headers).
        """
        for attachment_path in self.attachments:
            attachment = EmailAttachment(attachment_path).create()
            self.root_message.attach(attachment)

    def __send_root_message_via_smtp(self):
        """
        Method to finally send the message via the SMTP protocol, using the specified server.
        """
        with SMTP(self.server) as server:
            server.ehlo()
            server.sendmail(
                self.sender, 
                self.target, 
                self.root_message.as_string()
            )

    # Validations
    def __validate_mail_components(self):
        """
        Validates that the mandatory data is not empty, throwing an exception if that's the case.
        """
        if (
            not self.sender or
            not self.target or
            not self.email_body
        ):
            raise Exception('The mail cannot be send without the mandatory data (to, from and payload).')