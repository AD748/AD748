import logging

class LogFileHandler:
    """
    Class to handle logging for WebSocket messages.
    """

    # Define class-level variables for log file paths
    receivedLogFile = "logs/logFile/logs/received.log"
    sentLogFile = "logs/logFile/logs/sent.log"
    platformLogFile = "logs/logFile/logs/platform.log"
    errorLogFile = "logs/logFile/logs/error.log"
    token_auth_logFile = "logs/logFile/logs/token_auth.log"  # New log file

    def __init__(self):
        """
        Initialize LogFileHandler.
        """
  
        self.receivedLogger = self._setupLogger("ReceivedLogger", self.receivedLogFile)

        self.sentLogger = self._setupLogger("SentLogger", self.sentLogFile)

        self.platformLogger = self._setupLogger("PlatformLogger", self.platformLogFile)

        self.errorLogger = self._setupLogger("ErrorLogger", self.errorLogFile)

        # New logger for token authentication failures
        self.token_auth_logger = self._setupLogger("TokenAuthLogger", self.token_auth_logFile)

    def _setupLogger(self, name, logFile):
        """
        Setup logger with specified name and log file.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.ERROR)  # Set to ERROR for token_auth_logger
        handler = logging.FileHandler(logFile)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def logReceived(self, token, message):
        """
        Log received message.
        """
        detailedMessage = f"Received message from client with token {token}: {message}"
        self.receivedLogger.info(detailedMessage)

    def logSent(self, token, message):
        """
        Log sent message.
        """
        detailedMessage = f"Sent message to client with token {token}: {message}"
        self.sentLogger.info(detailedMessage)
    
    def logPlatform(self, token, message):
        """
        Log platform message.
        """
        detailedMessage = f"Platform Update for client with token {token}: {message}"
        self.platformLogger.info(detailedMessage)
    def logError(self, token, message):
        """
        Log error message.
        """
        detailedMessage = f"Platform Error for client with token {token}: {message}"
        self.errorLogger.info(detailedMessage)
    def logAuthFailure(self, token, message):
        """
        Log authentication failure message.
        """
        detailedMessage = f"Authentication Failure for client with token {token}: {message}"
        self.authFailureLogger.info(detailedMessage) 
