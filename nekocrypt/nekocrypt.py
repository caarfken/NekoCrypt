from itertools import cycle
import base64

class NekoCrypt:
    '''
    Usage:
    encrypt(password, message) to encrypt
    decrypt(password, message) to decrypt
    password must be str and message must be bytes, will be fixed later.
    '''
    def __processPassword(self, password: str, messagelength: int) -> bytes:
        '''
        Takes in password and extends it for use with NekoCrypt. Returns VERY long bytes sequence.
        '''
        # Repeat the password enough times to cover the message length and then slice it to the exact length
        password_bytes = [ord(char) for char in password]
        password = bytes([next(cycle(password_bytes)) for _ in range(messagelength)])

        return password
    # TODO: fix the type mixing disaster
    def encrypt(self, password: str, message, safeMode=False) -> bytes:
        '''
        Encrypts a message using NekoCrypt. Takes in password and message. Returns a bytes object.
        '''
        password = self.__processPassword(password, len(message))
        message = bytearray(message)  # Convert to bytearray for better performance
        
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
        if safeMode:
            return base64.b64encode(encryptedMessage)
        return encryptedMessage
    
    def decrypt(self, password, message, safeMode=False) -> bytes:
        '''
        Decrypts a message using NekoCrypt. Takes in lengthened password and message. Returns a bytes object.
        '''
        if safeMode:
            message = base64.b64decode(message).decode("ascii")        
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
        
        return bytes(decryptedMessage)
