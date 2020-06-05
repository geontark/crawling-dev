# crawling-dev


코스트코 물품  크롤링후 스마트 스토어에 자동등록 하는 프로그램

1. src/excute/CostcoRegisterExcute 에서 webDriverPath에 크롬 버전에 맞는 드라이버 경로 설정하기
2. src/excute/CostcoRegisterExcute 에서 costcoPath에 코스트코 물품 url 넣기
3. src/smartstore/CostcoRegister.py 에서 def login(self): 함수에서 스마트스토어
아이디, 비밀번호 설정해주기 
idText = smartStoreAuthConst('id')
pwText = smartStoreAuthConst('pw')
4. src/excute/CostcoRegisterExcute.py실행
5. 아무것도 만지지말고 기다리기(스마트스토에서 상세페이지 입력하면 자동입력단계 완료)
