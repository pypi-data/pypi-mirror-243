from abc import ABC, abstractmethod
from typing import Union, Optional, Dict, Any

class IUserRepo(ABC):

    @abstractmethod
    def find(self, user_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Method to find user data.
        :param user_id: User's ID.
        :return: User data or None.
        """
        pass

    @abstractmethod
    def find_token(self, user_id: str, token_names: Union[str, list], legacy: bool = False) -> Union[str, Dict[str, Any], None]:
        """
        Method to find API token(s).
        :param user_id: User's ID.
        :param token_names: Name(s) of the token(s) to find.
        :param legacy: Flag to use legacy method.
        :return: Token value(s) or None.
        """
        pass
