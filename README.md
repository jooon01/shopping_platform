# shopping_platform
WHS secure-coding 

# 📚 secure_coding - Django 중고거래 플랫폼

중고 상품을 등록하고, 채팅, 송금, 신고 기능 등을 통해 사용자 간 거래를 안전하게 할 수 있는 Django 기반 웹 플랫폼입니다.

---

## 🔧 환경 설정 및 실행 방법

### 1. 프로젝트 클론
git clone https://github.com/jooon01/shopping_platform.git
cd bookmarket

### 2. 가상환경 설정
python -m venv venv
source venv/bin/activate  

### 3. 패키지 설치
pip install -r requirements.txt

### 4. DB 마이그레이션
python manage.py makemigrations
python manage.py migrate

### 5. 관리자 계정 생성
python manage.py createsuperuser

### 6. 서버 실행
python manage.py runserver
접속 주소: http://127.0.0.1:8000

--------------------------------
📦 주요 기능
사용자 회원가입 / 로그인

상품 등록, 수정, 삭제, 검색

사용자 간 채팅 (1:1 및 전체방)

사용자 및 상품 신고

사용자 간 송금

거래 완료 표시

관리자 페이지에서 전체 관리

------------------
🛠️ 기술 스택
Python 3.13

Django 5.2

SQLite3 (개발용)

HTML / Bootstrap 5

Git / GitHub

