
class ItemListValidator:
    """
    @version 1.0.0

    Basic validator for list items. It looks for a value in the items list, if it's not found, and 
    exception is raised. The items list, the item to search and the custom exception message are
    received by contructor (but only the list and the item to search are mandatory)
    """

    # Default message for the not found exception.
    DEFAULT_NOT_FOUND_MESSAGE = 'Item not found in the list of values.'

    def __init__(
        self,
        items_list: list,
        item_to_find,
        not_found_message: str = None,
    ):
        """
        @param {list} items_list List containing all the available items to search.
        @param {any} item_to_find Specific item to find in the items list.
        @param {str} not_found_message Custom message for the Exception that is raised when the value is not found.
        """
        self.items_list: list = items_list
        self.item_to_find = item_to_find
        self.not_found_message = (
            not_found_message if not_found_message else self.DEFAULT_NOT_FOUND_MESSAGE
        )
    
    def validate(
        self, 
        custom_validator = None
    ):
        """
        @param {function} custom_validator Optional argument to provide a custom validator function that will overwrite the default one.
        The items list is provided as first parameter, and the item to find as second one.

        Performs the validation by executing the custom validator function, if provided; otherwise, it'll
        simply look for the value in the list.
        """
        if custom_validator != None:
            return custom_validator(self.items_list, self.item_to_find)

        if not self.item_to_find in self.items_list:
            raise Exception(self.not_found_message)

