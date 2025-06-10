"""자동화 관련 예외 클래스들"""


class RSAEncryptionError(Exception):
    """RSA 암호화 관련 예외"""
    pass


class LoginError(Exception):
    """로그인 관련 예외"""
    pass


class UserDataError(Exception):
    """사용자 데이터 관련 예외"""
    pass 