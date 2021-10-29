# Base validator
from ..utils.validators.ItemListValidator import ItemListValidator


class ESAVersionValidator(ItemListValidator):
    """
    @version 1.1.0

    Validator for the ESA version. Although the ItemListValidator could be functional standalone for this
    use case, a dedicated class wrapper was created because of the number of versions in the list,
    that could be difficult to mantain in the class that makes use of it (ESAStateManager).
    In this way we centralize the maintenance of the version list.
    """
    # Supported versions list
    supported_versions = [
        '11.0.0-074',
        '11.0.0-105',
        '11.0.0-255',
        '11.0.0-274',
        '11.0.1-027',
        '11.0.2-037',
        '11.0.2-044',
        '11.1.0-131',
        '11.1.0-135',
        '11.1.1-042',
        '13.0.0-375'
    ]

    def __init__(self, version: str):
        """
        @param {str} version ESA version number.
        """
        # We call the constructor of the base validator, providing the list, the intem to find and the exception message.
        super().__init__(
            items_list = self.supported_versions, 
            item_to_find = version,
            not_found_message = 'Version number not supported by this script'
        )

    def validate(self):
        """
        Method to perform the actual validation, it checks for the existance of the version in the
        supported versions list, raising an exception if not found.
        """
        # Executes the validate method of the parent class
        super().validate()





    
