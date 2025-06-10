"""비밀번호 관리 모듈"""

from typing import Optional

from ..client.api_client import WebAPIClient
from .user_manager import UserDataManager
from ..core.exceptions import LoginError, UserDataError


class PasswordManager:
    """비밀번호 관리 클래스"""
    
    def __init__(self, log_func: Optional[callable] = None):
        self.log_func = log_func or print
        self.api_client = WebAPIClient(self.log_func)
        self.data_manager = UserDataManager(self.log_func)
    
    def change_user_password(self, user_id: str) -> None:
        """사용자 비밀번호 변경 프로세스"""
        self.log_func("=== 비밀번호 변경 프로세스 시작 ===")
        self.log_func(f"대상 사용자 ID: {user_id}")
        
        try:
            # 로그인
            if not self.api_client.login():
                raise LoginError("로그인에 실패했습니다")
            
            # 사용자 설정 데이터 가져오기
            config_data = self.api_client.get_user_config_data(user_id)
            if 'LOGINID' not in config_data or config_data['LOGINID'] != user_id:
                raise UserDataError("사용자 조회에 실패했습니다")
            
            # 계정 잠금/해제 프로세스 (비밀번호 이력 초기화를 위함)
            lock_data = self.data_manager.modify_user_data_for_unlock(config_data, unlock=False)
            unlock_data = self.data_manager.modify_user_data_for_unlock(config_data, unlock=True)

            self.api_client.save_user_data(lock_data)
            self.api_client.save_user_data(unlock_data)
                        
            # 비밀번호 변경
            if not self.api_client.change_password(user_id):
                raise UserDataError("비밀번호 변경에 실패했습니다")
            
            self.log_func("=== 비밀번호 변경 프로세스 완료 ===")
            
        except Exception as e:
            self.log_func(f"비밀번호 변경 프로세스 실패: {str(e)}")
            raise 