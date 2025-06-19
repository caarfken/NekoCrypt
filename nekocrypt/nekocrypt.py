from itertools import cycle
import base64
from typing import Union

class NekoCrypt:
    '''
    Usage:
    encrypt(password, message) to encrypt
    decrypt(password, message) to decrypt
    useB64 prevents usage of non-printable characters but significantly lengthens output
    '''
    def __processPassword(self, password: str, messagelength: int) -> bytes:
        '''
        Takes in password and extends it for use with NekoCrypt. Returns VERY long bytes sequence.
        '''
        # Repeat the password enough times to cover the message length and then slice it to the exact length
        password_bytes = [ord(char) for char in password]
        password = bytes([next(cycle(password_bytes)) for _ in range(messagelength)])

        return password
    def encrypt(self, password: str, message: Union[str, bytes], useB64=False) -> Union[str, bytearray]:
        '''
        Encrypts a message using NekoCrypt. Takes in password and message.
        If useB64, encodes to base64 (Useful for printing) and returns a string.
        Otherwise, returns a bytearray object.
        '''
        password = self.__processPassword(password, len(message))
        message = bytearray(message, "utf-8")  # Use bytearray for better performance
        
        encryptedMessage = bytearray() # Use bytearray for better performance
        zeroMarkers = []
        footer = b"Encrypted with NekoCrypt"
        
        for i, char in enumerate(message):
            if char != 0:
                # Add password value and wrap around using modulo 256
                char = (char + password[i]) % 256
            else:
                # Record positions of zero bytes
                zeroMarkers.append(f" {i}")
            encryptedMessage.append(char)
        
        # Append footer and zero markers to the encrypted message
        encryptedMessage = encryptedMessage + footer + bytes(''.join(zeroMarkers), "utf-8")
        if useB64:
            return base64.b64encode(encryptedMessage).decode("utf-8")
        return encryptedMessage
    
    def decrypt(self, password, message: Union[str, bytes], useB64=False) -> Union[str, bytearray]:
        '''
        Decrypts a message using NekoCrypt. Takes in password and message. 
        If useB64, decodes base64 for the encrypted message first and returns a string.
        Otherwise, returns a bytearray.
        '''
        if useB64:
            message = base64.b64decode(message).decode("utf-8")        
        message = bytearray(message)
        password = self.__processPassword(password, len(message))
        
        decryptedMessage = bytearray()  # Use bytearray for better performance
        # Find the offset where the footer starts
        offset = message.find(b"Encrypted with NekoCrypt") + 25
        # Extract zero markers positions
        zeroPositions = {int(n) for n in message[offset:].split(b" ")}
        
        for i, char in enumerate(message[:offset - 25]):
            if char != 0 or i not in zeroPositions:
                # Subtract password value and wrap around using modulo 256
                char = (char - password[i]) % 256
            decryptedMessage.append(char)
        if useB64:
            return decryptedMessage.decode("utf-8")
        return decryptedMessage
