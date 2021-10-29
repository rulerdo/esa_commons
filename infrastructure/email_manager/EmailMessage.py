import mimetypes
# Email module
import email.encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Utils
from utils.files.FileManager import FileManager

class EmailMessageFactory:
    """
    @version 1.0.0

    Class that implements the factory design pattern, to create the appropiate instance of email.mime
    based on the provided message type.
    
    @note All the methods are static, so there's no need to create instances of this class, just invoke the 
    method in the following way: EmailMessageFactory.create_by_type(message_type).
    """
    # Supported email types
    TEXT        = 'TEXT'
    MIME_BASE   = 'MIME_BASE'
    MULTIPART   = 'MULTIPART'

    # Default message type
    DEFAULT_MESSAGE_TYPE = MIMEText

    # Default MIME type
    DEFAULT_MIME_TYPE = 'application/octet-stream'

    # MIME class
    message_types = {
        TEXT: MIMEText,
        MIME_BASE: MIMEBase,
        MULTIPART: MIMEMultipart
    }

    def create_by_type(message_type: str, *args, **kwargs):
        """
        Creates an email.mime message of the desired type. If the provided type is not in the message_types,
        we crate a simple text message.
        """
        return (
            EmailMessageFactory.message_types[message_type](*args, **kwargs)
                if message_type in EmailMessageFactory.message_types
                else EmailMessageFactory.DEFAULT_MESSAGE_TYPE(*args, **kwargs)
        )
    
    def create_text_message(text: str, *args, **kwargs):
        """
        Facade method to directly create a MIMEText message.
        """
        return EmailMessageFactory.message_types[EmailMessageFactory.TEXT](text, *args, **kwargs)

    def create_mime_base_message(main_type = None, sub_type = None, *args, **kwargs):
        """
        Facade method to directly create a MIMEBase message (for attachments).
        """
        return EmailMessageFactory.message_types[EmailMessageFactory.MIME_BASE](main_type, sub_type, *args, **kwargs)

    def create_multipart_message(*args, **kwargs):
        """
        Facade method to create a MIMEMultipart message, useful as root message, because it can contain
        text and attachments.
        """
        return EmailMessageFactory.message_types[EmailMessageFactory.MULTIPART](*args, **kwargs)


class EmailAttachment:
    """
    @version 1.1.2

    Class that provides a facade to create email attachments by providing only the path to the attachment.
    It performs all the required operations to determine automatically the MIME main type and subtype. It also
    creates the MIMEBase wrapper and initializes it with all the necessary parameters to get an instance
    that is ready to be attached to the root message.
    """
    def __init__(self, attachment_path: str):
        """
        @param {str} attachment_path Path to the attachment.
        """
        self.attachment_path = attachment_path
        # To be set later
        self.attachment_name = None
        self.attachment_content = None
        self.attachment_wrapper: MIMEBase = None


    def create(self, *args, **kwargs):
        """
        Facade method to create an attachment. It determines automatically the content type, as well
        as the content of the file. Then, this content is wrapped into a MIMEBase instance, to finally 
        be encoded and with some added headers.

        @returns The attachment wrapper, ready to be attached to another message.
        """
        # We set the MIME type and subtype internally
        self.__set_attachment_content_type()
        # We set the attachment content from the file
        self.__set_attachment_file_content()
        # We wrap the attachment and set the payload
        self.__set_attachment_wrapper(*args, **kwargs)
        # Finally, we enconde the attachment (Base64) and add the required headers to indicate that it's an attachment
        self.__enconde_attachment_and_add_headers()
        # We return the attachment wrapper
        return self.attachment_wrapper


    def __set_attachment_content_type(self) -> tuple[str, str]:
        """
        @param {str} attachment_path Path to the attachment.

        Method to guess the MIME type of an attachment. If no MIME type could be determined, the
        DEFAULT_MIME_TYPE is set.

        @returns {tuple(str, str)} Tuple with the main type and the subtype, respectively.
        """
        try:
            content_type, encoding = mimetypes.guess_type(self.attachment_path)
            if content_type is None or encoding is not None:
                raise Exception('MIME type undefined')
        except:
            content_type = EmailMessageFactory.DEFAULT_MIME_TYPE
        # We set the main type and the subtype internally
        self.main_type, self.subtype = content_type.split('/', 1)

    def __set_attachment_file_content(self):
        """
        Sets the content of the file by opening it in rb mode. It also sets the file name.
        """
        # We get the file content in binary
        file_manager = FileManager(self.attachment_path)
        self.attachment_content = file_manager.read_file_content(mode = 'rb')
        # We also set the file name
        self.attachment_name = file_manager.file_name

    def __set_attachment_wrapper(self, *args, **kwargs):
        """
        Initializes the attachment wrapper with the main type, subtype and the file content.
        """
        # We wrap the attachment in a MIMEBase instance, specifying the main type and the subtype
        self.attachment_wrapper = MIMEBase(self.main_type, self.subtype, *args, **kwargs)
        self.attachment_wrapper.set_payload(self.attachment_content)

    def __enconde_attachment_and_add_headers(self):
        """
        It performs a validation of the components of the attachment, encodes it (base64) and adds a 
        header to indicate that this is an attachment.
        """
        # We validate that all the attachment parameters are correct at this point
        self.__validate_attachment_components()
        # We encode the attachment (Base64) and add the header that indicates that it's an attachment
        email.encoders.encode_base64(self.attachment_wrapper)
        self.attachment_wrapper.add_header(
            'Content-Disposition', 
            'attachment',
            filename = self.attachment_name
        )
    
    def __validate_attachment_components(self):
        """
        Validation of the existance of all the required components of the attachment.
        """
        if (
            not self.attachment_path or
            not self.attachment_name or
            not self.attachment_content or
            not self.attachment_wrapper
        ):
            raise Exception('The attachment could not be created.')