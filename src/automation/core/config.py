"""설정 관리 모듈"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class AuthConfig:
    """인증 설정 클래스"""
    admin_id: str
    admin_password: str
    new_password: str


class ConfigManager:
    """설정 관리자 클래스"""
    
    def __init__(self):
        self._auth_config: Optional[AuthConfig] = None
    
    def load_auth_from_env(self) -> AuthConfig:
        """환경변수에서 인증 정보 로드"""
        admin_id = os.getenv('SOFTMANAGER_ADMIN_ID')
        admin_password = os.getenv('SOFTMANAGER_ADMIN_PASSWORD')
        new_password = os.getenv('SOFTMANAGER_NEW_PASSWORD')
        
        if not all([admin_id, admin_password, new_password]):
            raise ValueError(
                "필수 환경변수가 설정되지 않았습니다: "
                "SOFTMANAGER_ADMIN_ID, SOFTMANAGER_ADMIN_PASSWORD, SOFTMANAGER_NEW_PASSWORD"
            )
        
        self._auth_config = AuthConfig(
            admin_id=admin_id,
            admin_password=admin_password,
            new_password=new_password
        )
        return self._auth_config
    
    def load_auth_from_file(self, config_path: str = ".env") -> AuthConfig:
        """설정 파일에서 인증 정보 로드 (.env 파일)"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"설정 파일 {config_path}을 찾을 수 없습니다")
        
        # .env 파일 로드
        load_dotenv(config_path, override=True)
        
        admin_id = os.getenv('SOFTMANAGER_ADMIN_ID')
        admin_password = os.getenv('SOFTMANAGER_ADMIN_PASSWORD')
        new_password = os.getenv('SOFTMANAGER_NEW_PASSWORD')
        
        if not all([admin_id, admin_password, new_password]):
            raise ValueError(
                f"설정 파일 {config_path}에서 필수 설정을 찾을 수 없습니다: "
                "SOFTMANAGER_ADMIN_ID, SOFTMANAGER_ADMIN_PASSWORD, SOFTMANAGER_NEW_PASSWORD"
            )
        
        self._auth_config = AuthConfig(
            admin_id=admin_id,
            admin_password=admin_password,
            new_password=new_password
        )
        return self._auth_config
    
    def set_auth_config(self, admin_id: str, admin_password: str, new_password: str) -> AuthConfig:
        """인증 정보를 직접 설정 (테스트용)"""
        self._auth_config = AuthConfig(
            admin_id=admin_id,
            admin_password=admin_password,
            new_password=new_password
        )
        return self._auth_config
    
    @property
    def auth_config(self) -> AuthConfig:
        """현재 인증 설정 반환"""
        if self._auth_config is None:
            # 기본적으로 환경변수에서 로드 시도
            try:
                return self.load_auth_from_env()
            except ValueError:
                # 환경변수가 없으면 .env 파일에서 로드 시도
                return self.load_auth_from_file()
        return self._auth_config