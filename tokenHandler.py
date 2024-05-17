import boto3
import logging
from logs.logFile.logFileHandler import LogFileHandler
class TokenHandler:
    """
    A class to handle tokens using AWS Cognito.
    Author
        AbhinavVerma
    """

    def __init__(self):
        """
        Initializes the TokenHandler object.
        """
        self.client = boto3.client('cognito-idp', region_name='us-east-1')
        # Get the token_auth_logger from logFileHandler
        self.logger = logging.getLogger('token_auth_logger')

    def checkToken(self, accessToken):
        """
        Checks the validity of an access token.

        Parameters:
        accessToken (str): The access token to check.

        Returns:
        bool: True if the token is valid, False otherwise.
        """
        try:
            # Using the initialized client
            self.client.get_user(
                AccessToken=accessToken
            )
            return True
        except self.client.exceptions.NotAuthorizedException as e:
            print("Not Authorized:", e)
            return False
        except self.client.exceptions.InvalidParameterException as e:
            print("Invalid Parameter:", e)
            return False
        except self.client.exceptions.ResourceNotFoundException as e:
            print("Resource Not Found:", e)
            return False
        except Exception as e:
            self.logger.error(f"Token authentication failed: Resource Not Found - {e}")
            print("Token authentication failed: Unexpected Error-", e)
            return False