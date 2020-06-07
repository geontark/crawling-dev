from src.costco.CostcoItem import CostcoItem
from src.smartstore.CostcoRegister import SmartStoreItemRegister
from src.utills import Utills

# 코스트코 아이템을 정보를 읽어와 스마트스토어에 작성하는 실행 로직
def excute():
    webDriverPath = '/Users/tak/tak/python/crawling-dev/chromedriver'
    driver = Utills.getChromeDriver(webDriverPath)

    costcoPath = 'https://www.costco.co.kr/Food/Processed-Food/Instant-Food/Bonjuk-Rice-Abalone-Porridge-500g-x-3ea-x-4/p/624838'
    # 코스트코 정보 크롤링
    costcoItem = CostcoItem(driver, costcoPath).excute()
    costcoItem.quit()

    # 스마트스토어 상품 등록하기
    driver = Utills.getChromeDriver(webDriverPath)
    store = SmartStoreItemRegister(driver)
    store.itemId = costcoItem.itemId
    store.priceMarginRate = 1.08    # 8% 마진
    store.itemTitle = costcoItem.itemTitle
    store.itemPrice = costcoItem.itemPrice
    store.itemImgs = costcoItem.itemImgs
    store.itemDetailInfo = costcoItem.itemDetailInfo
    store.excute()

excute()