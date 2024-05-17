## TODO: Not a good practice to change the python interpreter
## Change it 
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))
from GLOBAL import CONNECTED_CLIENTS
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from pathlib import Path
from protocol.protocolHandler import ProtocolHandler
from protection.protectionHandler import ProtectionHandler
from tokens.tokenHandler import TokenHandler


class WebSocketHandler:
    """
    Class to handle WebSocket connections and messages.

    Author:
        AbhinavVerma
    """

    def __init__(self, logger):
        """
        Initialize WebSocketHandler.

        Parameters:
            logger: Logger instance for logging events.
        """
        # Store connected WebSocket clients
        self.protocolHandler = ProtocolHandler()
        self.protectionHandler = ProtectionHandler()
        self.tokenHandler = TokenHandler()
        self.logger = logger

    async def websocketEndpoint(self, websocket: WebSocket, token: str, initialUserID: str):
        """
        WebSocket endpoint to handle incoming messages and send responses.

        Parameters:
            websocket (WebSocket): WebSocket instance for the client connection.
            token (str): Token used for authentication.
        """
        # Check if token is valid (e.g., authenticate against a database)
        if self.tokenHandler.checkToken(token) == False:
            self.logger.error(f"Token authentication failed for client: {token}")
            await websocket.close()
            return

        await websocket.accept()  # Accept the WebSocket connection
        
        try:
            # Add the connected WebSocket client to the list
            CONNECTED_CLIENTS[initialUserID] = websocket
            self.logger.logPlatform(token, "Client Connected")
            
            # Continuously listen for messages from the client
            while True:
                try:
                    data = await self.receive(websocket, token)
                    data = self.protectionHandler.protect(data)
                    data = self.protocolHandler.process(data, websocket)
                    if data is None:
                        # Do not send any message
                        pass
                    else:
                        await self.send(websocket, data, token)
                except WebSocketDisconnect:
                    # WebSocket disconnected
                    self.logger.logPlatform(token, "Client Disconnected")
                    break  
        finally:
            # Remove the WebSocket client when connection is closed
            CONNECTED_CLIENTS.pop(initialUserID)

    async def send(self, websocket: WebSocket, message: str, token: str):
        """
        Method to send a message to a WebSocket client.

        Parameters:
            websocket (WebSocket): WebSocket instance for the client connection.
            message (str): Message to be sent.
            token (str): Token associated with the client.
        """
        # Log sent message
        self.logger.logSent(token, message)

        await websocket.send_text(message)

    async def receive(self, websocket: WebSocket, token: str) -> str:
        """
        Method to receive a message from a WebSocket client.

        Parameters:
            websocket (WebSocket): WebSocket instance for the client connection.
            token (str): Token associated with the client.

        Returns:
            str: The received message.
        """
        message = await websocket.receive_text()
        # Log received message
        self.logger.logReceived(token, message)
        return message


