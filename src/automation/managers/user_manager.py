"""사용자 데이터 관리 모듈"""

from typing import Dict, Optional, Any
from datetime import datetime
import copy

from ..core.exceptions import UserDataError


class UserDataManager:
    """사용자 데이터 관리 클래스"""
    
    def __init__(self, log_func: Optional[callable] = None):
        self.log_func = log_func or print
    
    def modify_user_data_for_unlock(self, config_data: Dict[str, Any], unlock: bool = True) -> Dict[str, Any]:
        """계정 잠금/잠금 해제를 위해 사용자 데이터 설정"""
        try:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d 오후 %I:%M:%S")
            current_date = now.strftime("%Y-%m-%d")
            
            user_data = copy.deepcopy(config_data)
            
            user_data.update({
                'EDTDATE': current_time,
                'EDTUSID_name': '',
                'ORGLINKDATE': current_date,
                'PASSWDMINDATE': current_date,
                'ISLOCK': '' if unlock else 'true'
            })
            
            lock_status = "잠금 해제" if unlock else "잠금"
            self.log_func(f"사용자 데이터 설정 - 계정 {lock_status} 완료")
            
            return user_data
            
        except Exception as e:
            raise UserDataError(f"사용자 데이터 설정 실패: {e}") from e 