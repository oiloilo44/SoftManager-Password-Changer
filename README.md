# SoftManager Password Changer 🔐

> 웹 기반 소프트웨어 관리 시스템을 위한 자동화된 비밀번호 변경 도구

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-green.svg)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 프로젝트 개요

SoftManager Password Changer는 특정 웹 기반 소프트웨어 관리 시스템에서 사용자 비밀번호를 자동으로 변경하는 도구입니다. 복잡한 RSA 암호화 과정과 다단계 API 호출을 자동화하여 관리자가 효율적으로 사용자 계정을 관리할 수 있도록 도와줍니다.

## ✨ 주요 기능

- **🔒 RSA 암호화**: 웹 페이지에서 공개키를 추출하여 보안 로그인 수행
- **🔄 자동화된 비밀번호 변경**: 복잡한 API 호출 과정을 자동화
- **🖥️ GUI 인터페이스**: 사용자 친화적인 Tkinter 기반 인터페이스
- **📝 실시간 로깅**: 모든 작업 과정을 실시간으로 로그로 표시
- **🧵 비동기 처리**: GUI 블로킹 없이 백그라운드에서 작업 수행
- **⚡ 모듈화된 구조**: 확장 가능한 객체지향 설계

## 🏗️ 아키텍처

```
src/
├── automation/           # 핵심 자동화 로직
│   ├── core/            # 기본 구성요소
│   │   ├── encryption.py    # RSA 암호화 처리
│   │   ├── constants.py     # API 상수 및 설정
│   │   ├── config.py        # 환경 설정 관리
│   │   └── exceptions.py    # 커스텀 예외 클래스
│   ├── client/          # API 클라이언트
│   │   └── api_client.py    # 웹 API 통신 로직
│   └── managers/        # 고수준 관리 클래스
│       ├── password_manager.py  # 비밀번호 변경 워크플로
│       └── user_manager.py      # 사용자 데이터 관리
└── ui/
    └── gui.py           # Tkinter GUI 애플리케이션
```

## 🛠️ 기술 스택

- **언어**: Python 3.12+
- **패키지 관리**: [uv](https://github.com/astral-sh/uv)
- **GUI**: Tkinter
- **웹 통신**: requests, BeautifulSoup4
- **암호화**: cryptography (RSA)
- **환경 설정**: python-dotenv
- **배포**: PyInstaller

## 🚀 설치 및 실행

### 필수 요구사항
- Python 3.12 이상
- uv 패키지 매니저

### 설치

```bash
# 프로젝트 클론
git clone https://github.com/yourusername/softmanager.git
cd softmanager

# 의존성 설치
uv sync
```

### 실행

```bash
# GUI 애플리케이션 실행
uv run python main.py

# 또는 직접 실행
python main.py
```

### 실행파일 빌드

```bash
# PyInstaller로 실행파일 생성
uv run pyinstaller main.spec
```

## 📖 사용법

1. **애플리케이션 시작**: `main.py` 실행
2. **User ID 입력**: 변경할 사용자의 ID 입력
3. **비밀번호 변경**: "비밀번호 변경" 버튼 클릭
4. **진행상황 확인**: 실시간 로그를 통해 작업 진행상황 모니터링

## 🔧 주요 구현 기술

### RSA 암호화 처리
```python
# 웹 페이지에서 RSA 공개키 추출 및 암호화
rsa_encryption = RSAEncryption()
encrypted_data = rsa_encryption.encrypt_data(login_data, public_key)
```

### 비동기 GUI 처리
```python
# GUI 블로킹 방지를 위한 스레드 처리
thread = threading.Thread(target=self.execute_password_change, args=(user_id,))
thread.daemon = True
thread.start()
```

### 모듈화된 API 클라이언트
```python
# 재사용 가능한 API 클라이언트 설계
api_client = WebAPIClient(log_func=self.log_message)
result = api_client.change_password(user_id)
```

## 🔍 핵심 특징

- **보안성**: RSA 공개키 암호화를 통한 안전한 데이터 전송
- **신뢰성**: 단계별 검증과 예외처리로 안정적인 작업 수행
- **사용성**: 직관적인 GUI와 실시간 피드백
- **확장성**: 모듈화된 구조로 새로운 기능 추가 용이
- **유지보수성**: 명확한 분리된 관심사와 문서화

## 📁 프로젝트 구조

```
softmanager/
├── src/
│   ├── automation/     # 자동화 핵심 로직
│   │   ├── core/      # 기본 구성요소
│   │   ├── client/    # API 통신
│   │   └── managers/  # 비즈니스 로직
│   └── ui/            # 사용자 인터페이스
├── main.py            # 애플리케이션 진입점
├── main.spec          # PyInstaller 설정
├── pyproject.toml     # 프로젝트 설정
└── README.md          # 프로젝트 문서
```