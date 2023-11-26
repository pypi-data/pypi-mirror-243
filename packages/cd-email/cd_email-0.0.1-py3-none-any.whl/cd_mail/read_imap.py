import imaplib
import email
from typing import List, Optional, Tuple


class IMAPClient:
    """
    A simple IMAP client for interacting with an IMAP server.

    Attributes:
    - server (str): The IMAP server's address.
    - port (int): The IMAP server's port (default is 993 for SSL).
    - connection: The current connection to the IMAP server. None if not connected.
    """

    def __init__(self, server: str, port: int = 993):
        """
        Initialize the IMAPClient with server details.

        Args:
        - server (str): The IMAP server's address.
        - port (int, optional): The IMAP server's port. Defaults to 993.
        """
        self.server = server
        self.port = port
        self.connection = None

    def login(self, username: str, password: str) -> bool:
        """
        Login to the IMAP server.

        Args:
        - username (str): The email/username for logging in.
        - password (str): The password for the email account.

        Returns:
        - bool: True if login is successful, False otherwise.
        """
        self.connection = imaplib.IMAP4_SSL(self.server, self.port)
        try:
            self.connection.login(username, password)
            return True
        except:
            return False

    def logout(self) -> None:
        """Logout from the IMAP server and reset the connection."""
        if self.connection:
            self.connection.logout()
            self.connection = None

    def select_folder(self, folder: str = "INBOX") -> Tuple[int, List[str]]:
        """
        Select a folder on the IMAP server.

        Args:
        - folder (str, optional): The folder name. Defaults to "INBOX".

        Returns:
        - Tuple[int, List[str]]: A tuple containing the response code and a list of email IDs in the folder.
        """
        return self.connection.select(folder)

    def search(self, criterion: str = 'ALL') -> List[str]:
        """
        Search emails based on a given criterion.

        Args:
        - criterion (str, optional): The search criterion. Defaults to 'ALL'.

        Returns:
        - List[str]: A list of email IDs that match the criterion.
        """
        _, message_numbers = self.connection.search(None, criterion)
        return message_numbers[0].split()

    def fetch_email(self, message_number: str) -> Optional[email.message.Message]:
        """
        Fetch the email content of a given email ID.

        Args:
        - message_number (str): The ID of the email to fetch.

        Returns:
        - Optional[email.message.Message]: The email message, or None if not found.
        """
        _, data = self.connection.fetch(message_number, '(RFC822)')
        raw_email = data[0][1]
        return email.message_from_bytes(raw_email)

    def delete_email(self, message_number: str) -> None:
        """
        Delete an email based on its ID.

        Args:
        - message_number (str): The ID of the email to delete.
        """
        self.connection.store(message_number, '+FLAGS', '\\Deleted')
        self.connection.expunge()

    def list_folders(self) -> List[Tuple[str]]:
        """
        List all available folders on the IMAP server.

        Returns:
        - List[Tuple[str]]: A list of available folders.
        """
        _, folder_data = self.connection.list()
        return folder_data

    def close_folder(self) -> None:
        """Close the currently selected folder on the IMAP server."""
        self.connection.close()

    def __del__(self):
        """Destructor for the IMAPClient, ensures the connection is terminated when the object is destroyed."""
        self.logout()
