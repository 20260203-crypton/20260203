#week11 실습

##오늘 한 것
- PyInstaller 설치 및 빌드
- resource_path() 함수 추가
- --add-data 옵션으로 에셋 포함
- .exe 실행 확인
## resource_path() 를 써야 하는 이유

## 빌드 명령어
pyinstaller --onefile --noconsol --add-data "sound;sound" immunoid_final.py

스프라이트는 문자열로 바꿔서 넣었기에 사운드만 해줬음.
## AI 활용 내역
