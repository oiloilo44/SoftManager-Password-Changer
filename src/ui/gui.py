"""GUI 애플리케이션 - SoftManager Password Changer"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime

from ..automation import PasswordManager


class PasswordManagerGUI:
    """비밀번호 관리 GUI 애플리케이션"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SoftManager Password Changer")
        
        app_width = 600  # 창 너비
        app_height = 500  # 창 높이
        screen_width = self.root.winfo_screenwidth()  # 화면 너비
        screen_height = self.root.winfo_screenheight()  # 화면 높이
        x = (screen_width / 2) - (app_width / 2)  # x 좌표 계산
        y = (screen_height / 2) - (app_height / 2)  # y 좌표 계산
        self.root.geometry(f"{int(app_width)}x{int(app_height)}+{int(x)}+{int(y)}")  # 크기와 위치 설정
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        
        self.password_manager = None
        self.is_running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성요소 설정"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 1. User ID 입력 섹션
        ttk.Label(main_frame, text="User ID:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.user_id_var = tk.StringVar()
        self.user_id_entry = ttk.Entry(main_frame, textvariable=self.user_id_var, width=30)
        self.user_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        
        # 2. 실행 버튼
        self.execute_button = ttk.Button(
            main_frame, 
            text="비밀번호 변경", 
            command=self.on_execute_clicked
        )
        self.execute_button.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # 3. 로그 창 섹션
        log_frame = ttk.LabelFrame(main_frame, text="실행 로그", padding="5")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 스크롤 가능한 텍스트 위젯
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 로그 클리어 버튼
        clear_button = ttk.Button(log_frame, text="로그 지우기", command=self.clear_log)
        clear_button.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        
        # 엔터 키 바인딩
        self.user_id_entry.bind('<Return>', lambda event: self.on_execute_clicked())
        
        # 초기 포커스
        self.user_id_entry.focus()
    
    def log_message(self, message: str):
        """로그 메시지를 GUI에 표시"""
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        formatted_message = f"{timestamp} {message}\n"
        
        # UI 스레드에서 안전하게 업데이트
        self.root.after(0, self._append_log, formatted_message)
    
    def _append_log(self, message: str):
        """로그 텍스트 위젯에 메시지 추가"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)  # 자동 스크롤
        self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """로그 창 내용 지우기"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def on_execute_clicked(self):
        """실행 버튼 클릭 이벤트"""
        user_id = self.user_id_var.get().strip()
        
        if not user_id:
            messagebox.showerror("입력 오류", "User ID를 입력해주세요.")
            return
        
        if self.is_running:
            messagebox.showwarning("실행 중", "이미 비밀번호 변경 프로세스가 실행 중입니다.")
            return
        
        # 별도 스레드에서 실행하여 GUI 블로킹 방지
        self.execute_button.config(state=tk.DISABLED, text="실행 중...")
        self.is_running = True
        
        thread = threading.Thread(target=self.execute_password_change, args=(user_id,))
        thread.daemon = True
        thread.start()
    
    def execute_password_change(self, user_id: str):
        """비밀번호 변경 프로세스 실행"""
        try:
            self.log_message(f"비밀번호 변경 프로세스를 시작합니다. (User ID: {user_id})")
            
            # PasswordManager 인스턴스 생성 (로그 함수 전달)
            self.password_manager = PasswordManager(log_func=self.log_message)
            
            # 비밀번호 변경
            self.password_manager.change_user_password(user_id)
            
            self.log_message("비밀번호 변경이 성공적으로 완료되었습니다!")
            
            # 성공 메시지 표시
            self.root.after(0, lambda: messagebox.showinfo("완료", "비밀번호 변경이 성공적으로 완료되었습니다!"))
            
        except Exception as e:
            error_msg = f"오류 발생: {str(e)}"
            self.log_message(error_msg)
            
            # 오류 메시지 표시
            self.root.after(0, lambda: messagebox.showerror("오류", f"비밀번호 변경 중 오류가 발생했습니다:\n{str(e)}"))
        
        finally:
            # UI 복원
            self.root.after(0, self._reset_ui)
    
    def _reset_ui(self):
        """UI 상태 복원"""
        self.execute_button.config(state=tk.NORMAL, text="비밀번호 변경")
        self.is_running = False
    
    def run(self):
        """GUI 애플리케이션 실행"""
        self.log_message("SoftManager Password Changer 프로그램이 시작되었습니다.")
        self.log_message("User ID를 입력하고 '비밀번호 변경' 버튼을 클릭하세요.")
        self.root.mainloop()


def main():
    """GUI 애플리케이션 메인 함수"""
    app = PasswordManagerGUI()
    app.run()


if __name__ == "__main__":
    main() 