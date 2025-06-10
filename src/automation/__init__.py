"""자동화 모듈 - 웹 API 자동화 및 비밀번호 관리

새로운 모듈 구조:
- core: 핵심 기능 (예외, 상수, 암호화)
- client: API 클라이언트
- managers: 관리 클래스들
"""

# 핵심 모듈
from .core import (
    RSAEncryptionError, 
    LoginError, 
    UserDataError,
    WebAPIConstants,
    RSAEncryption,
    ConfigManager
)

# 클라이언트 모듈
from .client import WebAPIClient

# 관리자 모듈  
from .managers import UserDataManager, PasswordManager

# 기존 코드와의 호환성을 위한 별칭
HTTPAutomation = WebAPIClient
HTTPPasswordManager = PasswordManager

__all__ = [
    # 핵심 클래스
    'RSAEncryption',
    'WebAPIConstants',
    'ConfigManager',
    
    # 예외 클래스
    'RSAEncryptionError',
    'LoginError',
    'UserDataError',
    
    # 클라이언트
    'WebAPIClient',
    
    # 관리자
    'UserDataManager',
    'PasswordManager',
    
    # 호환성 별칭
    'HTTPAutomation',
    'HTTPPasswordManager',
] 