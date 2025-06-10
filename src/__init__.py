"""소프트웨어 관리자 패키지

모듈 구조:
- config: 설정 및 환경변수 관리
- automation: 웹 자동화 기능
"""

from .automation import PasswordManager, WebAPIClient, UserDataManager, ConfigManager

__version__ = "1.0.0"

__all__ = [
    'PasswordManager',
    'WebAPIClient',
    'UserDataManager',
    'ConfigManager',
] 