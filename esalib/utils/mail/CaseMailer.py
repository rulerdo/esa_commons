# Email manager
from ...infrastructure.email_manager.EmailManager import EmailManager
# ESA utils
from ...esa_utils.ESAParameters import ESAEmailParameters
from ...esa_utils.ESARemediationStatus import ESARemediationStatus
# Utils
from ...utils.logger.Logger import Logger


class CaseMailer:
    """
    @version 2.0.0

    Class that encapsulates the process and values involved in the process of sending the informative
    mail with the remediation status.
    It makes use of the EmailManager class to easily send a mail, by providing the most elemental data,
    such as the case owner email, and the remediation status (from which the email text body and attachments
    are obtained via the get_remediation_messages() and get_remediation_attachments() respectively).
    """

    # SMTP server domain
    __SMTP_SERVER = 'outbound.cisco.com'

    # Email subject helper string, it is completed with the cas number
    __EMAIL_SUBJECT = 'SR:%s'

    # Default email body (to indicate a general error)
    __DEFAULT_EMAIL_BODY = 'There was an error, please review the attached log file.'

    def __init__(
        self, 
        esa_status: ESARemediationStatus,
        esa_email_parameters: ESAEmailParameters
    ):
        """
        @param {ESARemediationStatus} esa_status Instance that contains the status of the remediation, as well as the record of the modified files.
        @param {str} case_ownr_email Email address of the case owner.
        @param {str} case_identification_number ID of the case (SR).
        """
        self.esa_status = esa_status
        self.case_owner_email = esa_email_parameters.case_owner_email
        self.case_identification_number = esa_email_parameters.case_identification_number

    def send_mail(self):
        """
        Method to send the mail, using the EmailManager class. It only requires all the data that
        we already have, such as the SMTP server domain, the sender (from), target (to), subject,
        email body and attachments. These last 2 are obtained from the ESA remediation status instance.
        """
        # We compose the subject with the case number
        subject = self.__EMAIL_SUBJECT % self.case_identification_number
        # We send the mail via the EmailManager
        Logger.info(f'Sending email to { self.case_owner_email } with the remediation details...')
        EmailManager(
            server = self.__SMTP_SERVER,
            sender = self.case_owner_email,
            target = self.case_owner_email,
            subject = subject,
            email_body = self.__get_email_body(),
            attachments = self.__get_email_attachments()
        ).send()
        Logger.info('Email sent successfully!')

    def __get_email_body(self):
        """
        Method to get the email body from the ESARemediationStatus instance, if available, otherwise, we send a default message
        to indicate a general error.
        """
        return ( 
            self.esa_status.get_remediation_messages() 
            if self.esa_status != None
            else self.__DEFAULT_EMAIL_BODY
        )

    def __get_email_attachments(self):
        """
        Method to get the rerieved files during the process from the ESARemediationStatus instance, if available, otherwise, we send 
        the own log file that contains the general error.
        """
        attachments = [Logger.output_log_file_name]
        if self.esa_status != None:
            attachments += self.esa_status.get_remediation_attachments()
        return attachments