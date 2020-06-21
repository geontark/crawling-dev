import time
import urllib.request
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from src.utills import Utills
from src.consts.AbsolutePathConst import getAbsolutePath

class IkeaItem:
    # 웹 드라이버, 코스트코 상품 url
    def __init__(self, driver=None, ikeaPath=None):
        self.__itemId = ''
        self.__itemTitle = ''
        self.__itemPrice = ''
        self.__itemStockState = ''
        self.__itemUrl = ''
        self.__itemImgs = []
        self.__itemDetailInfo = []

        if driver is not None:
            self.__driver = driver
        if ikeaPath is not None:
            self.__ikeaPath = ikeaPath
            self.__itemUrl = ikeaPath

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
        self.__driver.get(self.__ikeaPath)
        time.sleep(5)
        self.searchItemId()
        self.searchItemTitle()
        self.searchItemPrice()
        self.searchSaveImgs()
        self.searchItemDetailInfo()
        return self

    def searchItemId(self):
        self.__itemId = self.__driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[2]/div[2]/span/span').text

    def searchItemTitle(self):
        self.__itemTitle = self.__driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[3]/div/div[1]/div/div[1]/h1/div[1]').text
        try:
            subTitle = self.__driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/div[2]/div[3]/div/div[1]/div/div[1]/h1/div[2]/span[1]').text
            self.__itemTitle += ' ' + subTitle
        except NoSuchElementException:
            print('subTitle NoSuch')

        try:
            itemMesure = self.__driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/div[2]/div[3]/div/div[1]/div/div[1]/h1/div[2]/span[2]').text
            self.__itemTitle += ' ' + itemMesure
        except NoSuchElementException:
            print('itemMesure NoSuch')

    def searchItemPrice(self):
        try:  # 할인 하는지 체크
            self.__itemPrice = self.__driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[1]/div/div[2]/div[3]/div/div[1]/div/div[2]/div/span/span[2]').text.replace(
                ',', '').replace('원', '')
        except NoSuchElementException:
            print('가격 에러')

    #     이미지 찾기 및 이미지 다운로드
    def searchSaveImgs(self):
            thumbNails = self.__driver.find_elements_by_css_selector(
                '#content > div > div > div > div.range-revamp-product__subgrid.product-pip.js-product-pip > div.range-revamp-product__left-top.range-revamp-product__grid-gap > div > div.range-revamp-media-grid__grid > div')

            thumbNailLength = len(thumbNails)
            thumbNailPath = []
            Utills.movingTop(
            self.__driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[2]/div[1]/div'))
            imgFolder = '/Users/tak/tak/python/crawling-dev/src/smartstore/ikeaitemimg/' + self.itemId
            Utills.createFolder(imgFolder)
            for i in range(thumbNailLength):
                # thumbNails[i].click()
                time.sleep(10)
                src = self.__driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div/div/div[2]/div[1]/div/div[1]/div[' + str(i +1) + ']/div/img').get_attribute('src')
                downloadPath = imgFolder + '/' + str(i) + '.jpg'
                urllib.request.urlretrieve(src, downloadPath)
                thumbNailPath.append(downloadPath)

            self.__itemImgs = thumbNailPath

    def searchItemDetailInfo(self):
        Utills.movingTop(self.__driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[2]/div[2]/div[2]'))

        self.__driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[2]/div[3]/div[1]/button').click()
        time.sleep(3)
        html = self.__driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        ikeaStylepath = getAbsolutePath('ikeaStyle')
        ikeaStyle = Utills.fileStrRead(ikeaStylepath)
        itemDetailInfo = []
        itemDetailInfo.append(str(ikeaStyle) + str(soup.select('#range-modal-mount-node > div > div:nth-child(3) > div > div.range-revamp-modal__content')[0]))
        self.__itemDetailInfo = itemDetailInfo

    def quit(self):
        self.__driver.quit()
        return self

# def excute():
#     webDriverPath = '/Users/tak/tak/python/crawling-dev/chromedriver'
#     ikeaPath = 'https://www.ikea.com/kr/ko/p/bolmen-toilet-brush-holder-black-90165421/'
#     driver = Utills.getChromeDriver(webDriverPath)
#     ikeaItem = IkeaItem(driver,ikeaPath).excute()
#     time.sleep(1000)

# excute()