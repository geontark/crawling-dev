
# 코스트코 재고 및 가격 변동 확인하기
import schedule
import time
from src.costco.CostcoStockCheck import CostcoStockCheck
from src.utills import Utills


def excute():
    webDriverPath = '/Users/tak/tak/python/crawling-dev/chromedriver'
    driver = Utills.getChromeDriver(webDriverPath)

    stock = CostcoStockCheck(driver)
    stock.excute()

# schedule.every(10).minutes.do(excute)
# excute()
# 매일 10:00 에 실행
schedule.every().day.at("09:00").do(excute)
excute()

# 무한루프를 돌면서 스케줄을 유지
while 1:
    schedule.run_pending()
    time.sleep(60)
