# Web Admin Password Tool

웹 관리자 화면에서 반복되는 사용자 비밀번호 변경 절차를 자동화한 Python 데스크톱 도구입니다.

## 기능

- 관리자 로그인 자동화
- 페이지에서 RSA 공개키를 읽어 로그인 값 암호화
- 사용자 조회 및 비밀번호 변경 API 호출
- Tkinter 기반 간단한 GUI
- 작업 로그 표시

## 기술 스택

- Python 3.12
- Tkinter
- requests
- BeautifulSoup4
- cryptography
- python-dotenv

## 설정

실제 서버 주소와 인증 정보는 환경변수 또는 `.env` 파일로 주입합니다.

```env
WEB_ADMIN_BASE_URL=http://localhost:8080/
SOFTMANAGER_ADMIN_ID=admin
SOFTMANAGER_ADMIN_PASSWORD=password
SOFTMANAGER_NEW_PASSWORD=new-password
```

## 실행

```bash
git clone https://github.com/oiloilo44/SoftManager-Password-Changer.git
cd SoftManager-Password-Changer
uv sync
uv run python main.py
```

## 구조

```text
src/automation/  로그인, 암호화, API 호출, 비밀번호 변경 흐름
src/ui/          Tkinter GUI
main.py          실행 진입점
```
