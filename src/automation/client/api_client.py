"""웹 API 클라이언트 모듈"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Tuple, Optional, Any
import json

from ..core.constants import WebAPIConstants
from ..core.exceptions import LoginError, UserDataError
from ..core.encryption import RSAEncryption
from ..core.config import ConfigManager


class WebAPIClient:
    """웹 API 클라이언트 클래스"""
    
    def __init__(self, log_func: Optional[callable] = None):
        self.log_func = log_func or print
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': WebAPIConstants.USER_AGENT
        })
        self._rsa_encryption: Optional[RSAEncryption] = None
    
    def _get_rsa_keys_from_login_page(self) -> Tuple[str, str]:
        """로그인 페이지에서 RSA 공개키 정보 추출"""
        self.log_func("로그인 페이지 접속 중...")
        
        try:
            response = self.session.get(WebAPIConstants.WEBSITE_URL)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rsa_modulus_element = soup.find('input', {'id': WebAPIConstants.RSA_MODULUS_ID})
            rsa_exponent_element = soup.find('input', {'id': WebAPIConstants.RSA_EXPONENT_ID})

            if not rsa_modulus_element or not rsa_exponent_element:
                raise LoginError("RSA 공개키 정보를 찾을 수 없습니다")
            
            modulus = rsa_modulus_element.get('value')
            exponent = rsa_exponent_element.get('value')
            
            self.log_func(f"RSA 공개키 정보 추출 완료: {modulus}, {exponent}")
            return modulus, exponent
            
        except Exception as e:
            raise LoginError(f"로그인 페이지 접속 실패: {e}") from e
    
    def _is_login_successful(self, response: requests.Response) -> bool:
        """로그인 성공 여부 확인"""
        return response.status_code == 200 and "webmain" in response.url
    
    def login(self) -> bool:
        """웹 로그인 수행"""
        self.log_func("웹 로그인 시작...")
        
        try:
            modulus, exponent = self._get_rsa_keys_from_login_page()
            self._rsa_encryption = RSAEncryption(modulus, exponent)
            
            auth_config = ConfigManager().auth_config
            login_id = auth_config.admin_id.upper()
            encrypted_id = self._rsa_encryption.encrypt(login_id)
            encrypted_pw = self._rsa_encryption.encrypt(auth_config.admin_password)
            
            self.log_func("ID/PW RSA 암호화 완료")
            
            login_data = {
                'loginid': encrypted_id,
                'loginpw': encrypted_pw,
                'homeType': WebAPIConstants.HOME_TYPE,
                'redirectUrl': '',
                'redirectUser': '',
            }
            
            login_url = f"{WebAPIConstants.WEBSITE_URL}{WebAPIConstants.LOGIN_ENDPOINT}"
            response = self.session.post(login_url, data=login_data)
            response.raise_for_status()
            
            if self._is_login_successful(response):
                self.log_func("웹 로그인 성공")
                return True
            else:
                self.log_func("웹 로그인 실패")
                return False
                
        except Exception as e:
            raise LoginError(f"로그인 프로세스 실패: {e}") from e
    
    def change_password(self, user_id: str) -> bool:
        """비밀번호 변경"""
        self.log_func(f"사용자 {user_id}의 비밀번호 변경 시작...")
        
        try:
            change_pwd_url = f"{WebAPIConstants.WEBSITE_URL}{WebAPIConstants.CHANGE_PASSWORD_ENDPOINT}"
            auth_config = ConfigManager().auth_config
            change_data = {
                'target': user_id,
                'info': auth_config.new_password,
            }
            
            response = self.session.post(change_pwd_url, data=change_data)
            response.raise_for_status()
            
            if response.text == WebAPIConstants.PASSWORD_CHANGE_SUCCESS:
                self.log_func("비밀번호 변경 성공!")
                return True
            else:
                self.log_func(f"비밀번호 변경 실패: {response.text}")
                return False
                
        except Exception as e:
            raise UserDataError(f"비밀번호 변경 실패: {e}") from e

    def get_user_config_data(self, user_id: str) -> Dict[str, Any]:
        """사용자 설정 데이터 가져오기"""
        self.log_func(f"사용자 {user_id}의 설정 데이터 요청 중...")
        
        try:
            config_url = f"{WebAPIConstants.WEBSITE_URL}{WebAPIConstants.USER_CONFIG_ENDPOINT}"
            config_data = {
                'keyword': user_id,
                'viewName': WebAPIConstants.VIEW_TYPE,
                'opt': WebAPIConstants.OPTION_TYPE,
            }

            response = self.session.post(config_url, data=config_data)
            response.raise_for_status()
            
            try:
                result = response.json()['gridData'][0]
                self.log_func("사용자 설정 데이터 수신 완료")
                return result
            except ValueError:
                self.log_func("응답이 JSON 형식이 아닙니다.")
                return {"raw_data": response.text}
                
        except Exception as e:
            raise UserDataError(f"사용자 설정 데이터 요청 실패: {e}") from e

    def save_user_data(self, config_data: Dict[str, Any]) -> bool:
        """수정된 사용자 데이터를 서버에 저장"""
        self.log_func("사용자 데이터 저장 시작...")
        
        try:
            save_url = f"{WebAPIConstants.WEBSITE_URL}{WebAPIConstants.SAVE_USER_DATA_ENDPOINT}"
            save_data = {
                'addRowList': '[]',
                'editRowList': json.dumps([config_data]),
                'delRowList': '',
                'type': WebAPIConstants.DATA_TYPE
            }
            
            self.log_func("사용자 데이터 전송 중...")
            response = self.session.post(save_url, data=save_data)
            response.raise_for_status()
            
            if response.text == WebAPIConstants.SUCCESS_RESPONSE:
                self.log_func("사용자 데이터 저장 성공!")
                return True
            else:
                self.log_func(f"사용자 데이터 저장 실패: {response.text}")
                return False
                    
        except Exception as e:
            raise UserDataError(f"사용자 데이터 저장 실패: {e}") from e 