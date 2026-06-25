"""웹 관리자 API 자동화 관련 상수 정의"""

import os


class WebAPIConstants:
    """웹 관리자 API 관련 상수"""
    
    # User-Agent (config에서 가져옴)
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # 웹 사이트 URL. 실제 운영 주소는 환경변수로 주입합니다.
    WEBSITE_URL = os.getenv("WEB_ADMIN_BASE_URL", "http://localhost:8080/")

    # HTML 요소 ID
    RSA_MODULUS_ID = 'RSAModulus'
    RSA_EXPONENT_ID = 'RSAExponent'
    
    # API 엔드포인트
    LOGIN_ENDPOINT = '/commonLogin'
    CHANGE_PASSWORD_ENDPOINT = '/eidtPwData'
    USER_CONFIG_ENDPOINT = '/userConfigFormData'
    SAVE_USER_DATA_ENDPOINT = '/saveUserData'
    
    # 응답 관련
    SUCCESS_RESPONSE = 'success'
    PASSWORD_CHANGE_SUCCESS = '0'
    
    # 폼 데이터 타입
    HOME_TYPE = '0'
    VIEW_TYPE = '0'
    OPTION_TYPE = '0'
    DATA_TYPE = '0'
