"""RSA 암호화 모듈"""

from .exceptions import RSAEncryptionError


class RSAEncryption:
    """RSA 암호화를 담당하는 클래스"""
    
    def __init__(self, modulus: str, exponent: str):
        self.modulus = modulus
        self.exponent = exponent
    
    def _pkcs1_pad(self, message: bytes, key_size: int) -> bytes:
        """PKCS#1 v1.5 패딩 구현"""
        message_len = len(message)
        if key_size < message_len + 11:
            raise RSAEncryptionError("메시지가 너무 길어서 RSA 암호화할 수 없습니다")
        
        ps_len = key_size - message_len - 3
        ps = bytes([i for i in range(1, 256) if i != 0] * (ps_len // 255 + 1))[:ps_len]
        
        padded = b'\x00\x02' + ps + b'\x00' + message
        return padded
    
    def encrypt(self, text: str) -> str:
        """RSA 암호화"""
        try:
            message_bytes = text.encode('utf-8')
            
            modulus_int = int(self.modulus, 16)
            exponent_int = int(self.exponent, 16)
            
            key_size = (modulus_int.bit_length() + 7) // 8
            padded_message = self._pkcs1_pad(message_bytes, key_size)
            
            m = int.from_bytes(padded_message, 'big')
            c = pow(m, exponent_int, modulus_int)
            
            hex_result = hex(c)[2:].upper()
            if len(hex_result) % 2 == 1:
                hex_result = '0' + hex_result
                
            return hex_result
            
        except Exception as e:
            raise RSAEncryptionError(f"RSA 암호화 실패: {e}") from e 