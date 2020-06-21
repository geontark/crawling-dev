import time
import urllib.request
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from src.utills import Utills

# 코스트코의 상품 정보를 얻어옴
# 상품 아이디, 이름, 이미지, 상세정보
# itemId, itemTitle, itemPrice, itemImgs, itemDetailInfo, itemUrl, itemStockState
class CostcoItem:
     # 웹 드라이버, 코스트코 상품 url
    def __init__(self, driver = None, costcoPath = None):
        self.__itemId = ''
        self.__itemTitle = ''
        self.__itemPrice = ''
        self.__itemStockState = ''
        self.__itemUrl = ''
        self.__itemImgs = []
        self.__itemDetailInfo = []

        if driver is not None:
            self.__driver = driver
        if costcoPath is not None:
            self.__costcoPath = costcoPath
            self.__itemUrl = costcoPath

    @property
    def itemUrl(self):
        return self.__itemUrl

    @itemUrl.setter
    def itemUrl(self, url):
        self.__itemUrl = url

    @property
    def itemId(self):
         return self.__itemId

    @itemId.setter
    def itemId(self, str):
         self.__itemId = str

    @property
    def itemTitle(self):
         return self.__itemTitle

    @itemTitle.setter
    def itemTitle(self, str):
         self.__itemTitle = str

    @property
    def itemPrice(self):
         return self.__itemPrice

    @itemPrice.setter
    def itemPrice(self, str):
         self.__itemPrice = str

    @property
    def itemImgs(self):
         return self.__itemImgs

    @itemImgs.setter
    def itemImgs(self, imgs):
         self.__itemImgs = imgs

    @property
    def itemDetailInfo(self):
         return self.__itemDetailInfo

    @itemDetailInfo.setter
    def itemDetailInfo(self, itemDetailInfo):
         self.__itemDetailInfo = itemDetailInfo

    @property
    def itemStockState(self):
         return self.__itemStockState

    @itemStockState.setter
    def itemStockState(self, str):
         self.__itemStockState = str

    def excute(self):
        self.__driver.get(self.__costcoPath)
        time.sleep(5)
        self.searchItemId()
        self.searchItemTitle()
        self.searchItemPrice()
        self.searchSaveImgs()
        self.searchItemStockState()
        self.searchItemDetailInfo()
        return self

    def quit(self):
        self.__driver.quit()
        return self

    def searchItemId(self):
        try:
            self.__itemId = self.__driver.find_element_by_xpath('//*[@id="globalMessages"]/div[3]/div[3]/p/span').text
        except NoSuchElementException:
            time.sleep(2)
            self.__itemId = self.__driver.find_element_by_xpath('//*[@id="globalMessages"]/div[3]/div[3]/p/span').text

    def searchItemTitle(self):
        self.__itemTitle = self.__driver.find_element_by_xpath('// *[ @ id = "globalMessages"]/div[3]/div[3]/h1').text

    def searchItemPrice(self):
        try:  # 할인 하는지 체크
            self.__itemPrice = self.__driver.find_element_by_css_selector('.product-price-container .product-price-detail .price-after-discount .you-pay-value').text.replace(',','').replace('원','')
            print('할인함')
        except NoSuchElementException:
            self.__itemPrice = self.__driver.find_element_by_css_selector('.product-price-container .product-price-detail .price-original .notranslate').text.replace(',', '').replace('원','')
            print('할인하지 않음')

    # 판매중인지 매진된 상태인지 체크
    def searchItemStockState(self):
        # 판매 상태 ("쇼핑카트에 담기", "품절" )
        try:
            # 판매중
            stockState = self.__driver.find_element_by_xpath('//*[@id="addToCartButton"]').text
        except NoSuchElementException:
            # 품절
            stockState = self.__driver.find_element_by_xpath('//*[@id="addToCartForm"]/button').text
        print(stockState)
        self.__itemStockState = stockState

    #     이미지 찾기 및 이미지 다운로드
    def searchSaveImgs(self):
        thumbNails = self.__driver.find_elements_by_css_selector(
            '#globalMessages > div.product-page-container > div.product-gallery.visible-tablet-landscape.visible-desktop.col-xs-12.col-sm-12.col-md-6.col-tab-6 > div > div.gallery-carousel-wrapper > div > div.owl-wrapper-outer > div > div')
        thumbNailLength = len(thumbNails)
        thumbNailPath = []
        Utills.movingTop(self.__driver.find_element_by_xpath('//*[@id="globalMessages"]/div[3]/div[2]/div/div[2]'))
        imgFolder = '/Users/tak/tak/python/crawling-dev/src/smartstore/costcoitemimg/' + self.itemId
        Utills.createFolder(imgFolder)
        for i in range(thumbNailLength):
            thumbNails[i].click()
            time.sleep(10)
            src = self.__driver.find_element_by_xpath(
                '//*[@id="globalMessages"]/div[3]/div[2]/div/div[1]/div[1]/div/div[' + str(
                    i + 1) + ']/div/div/div/img').get_attribute('src')
            downloadPath = imgFolder + '/' + str(i) + '.jpg'
            urllib.request.urlretrieve(src, downloadPath)
            Utills.imgResize(downloadPath, 1000, 1000) # 이미지 리사이징
            thumbNailPath.append(downloadPath)

        self.__itemImgs = thumbNailPath

    #     상품상세 설명 및 스펙
    def searchItemDetailInfo(self):
        html = self.__driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        itemDetailInfo = []
        itemDetailInfo.append(soup.select('#pdp-tabs > div')[0])
        itemDetailInfo.append(soup.select('#pdp-tabs > div')[1])
        self.__itemDetailInfo = itemDetailInfo

    def stockCheck(str):
        stockCheck = {
             '쇼핑카트에 담기': 'sale',
             '품절': 'sold out'
        }
        return stockCheck.get(str)




