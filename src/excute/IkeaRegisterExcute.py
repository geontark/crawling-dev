from src.ikea.IkeaItem import IkeaItem
from src.smartstore.CostcoRegister import SmartStoreItemRegister
from src.utills import Utills

# 이케아 아이템을 정보를 읽어와 스마트스토어에 작성하는 실행 로직
def excute():
    webDriverPath = '/Users/tak/tak/python/crawling-dev/chromedriver'
    driver = Utills.getChromeDriver(webDriverPath)

    ikeaPath = 'https://www.ikea.com/kr/ko/p/raskog-trolley-grey-green-90443140/'
    # 이케아 정보 크롤링
    ikeaItem = IkeaItem(driver, ikeaPath).excute()
    ikeaItem.quit()

    # 스마트스토어 상품 등록하기
    driver = Utills.getChromeDriver(webDriverPath)
    store = SmartStoreItemRegister(driver)
    store.itemId = ikeaItem.itemId
    store.priceMarginRate = 1.08    # 8% 마진
    store.deliveryPrice = 5000  # 배송료 5000
    store.itemTitle = ikeaItem.itemTitle
    store.itemPrice = ikeaItem.itemPrice
    store.itemImgs = ikeaItem.itemImgs
    store.itemDetailInfo = ikeaItem.itemDetailInfo
    store.excute()

excute()