import time
from bs4 import BeautifulSoup
import src.consts.AbsolutePathConst as absolutePathConst
import src.utills.Utills as Utills

class VvicItem:
    # 웹 드라이버, 코스트코 상품 url
    def __init__(self, driver=None, vvicPath=None):
        # self.__itemId = ''
        # self.__itemTitle = ''
        # self.__itemPrice = ''
        # self.__itemStockState = ''
        # self.__itemUrl = ''
        # self.__itemImgs = []
        # self.__itemDetailInfo = []
        self.__itemSizes = []

        if driver is not None:
            self.__driver = driver
        if vvicPath is not None:
            self.__vvicPath = vvicPath
            self.__itemUrl = vvicPath

    @property
    def itemId(self):
        return self.__itemId

    @itemId.setter
    def itemId(self, itemId):
        self.__itemId = itemId

    @property
    def itemTitle(self):
        return self.__itemTitle

    @itemTitle.setter
    def itemTitle(self, itemTitle):
        self.__itemTitle = itemTitle

    @property
    def itemSize(self):
        return self.__itemSize

    @itemSize.setter
    def itemSize(self, itemSizse):
        self.__itemSize = str


    def excute(self):
        self.__driver.get(self.__vvicPath)
        time.sleep(5)
        self.searchItemDetailImgs()
        # self.searchItemId()
        # self.searchItemTitle()
        # self.searchItemSizes()

    def searchItemId(self):
        self.__itemId = self.__driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[1]/div[1]/dl[1]/dd[1]/div[2]/font/font').text

    def searchItemTitle(self):
        self.__itemId = self.__driver.find_element_by_xpath(
            '/html/body/div[6]/div[1]/div[1]/div[1]/div[1]/strong').text

    #     도매가 위안
    def searchWholesalePrice(self):
        self.__itemPrice = self.__driver.find_element_by_xpath(
            '/html/body/div[6]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/span/strong[2]').text

    # 사이즈
    def searchItemSizes(self):
        html = self.__driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sizesStr = soup.select('#j-buy > dd:nth-child(3) > div.value.goods-choice.goods-choice-size.goods-choice-size__height > ul > div > li .selectSize')
        size = []
        for sizeStr in sizesStr:
            size.append(sizeStr.text)
        self.__itemSize = size

    def searchItemDetailImgs(self):
        html = self.__driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        detailImgs = soup.select(
            '#info > div:nth-child(1) > div.d-content')
        print(detailImgs)

def excute():
    webDriverPath = absolutePathConst.getAbsolutePath('chromDriver')
    driver = Utills.getChromeDriver(webDriverPath)
    vvicPath = 'https://www.vvic.com/item/20893402'



    # # 이케아 정보 크롤링
    # ikeaItem = IkeaItem(driver, ikeaPath).excute()
    # ikeaItem.quit()

    vvicItem = VvicItem(driver,vvicPath)
    vvicItem.excute()


excute()

    # # 디테일 설명
    # def searchDetailInfo(self):
    #     html = self.__driver.page_source
    #     soup = BeautifulSoup(html, 'html.parser')
    #     imgs = soup.select('#info > div:nth-child(1) > div.d-content img')
    #     for img in imgs:
    #         img.attr

        # itemDetailInfo = []
        # itemDetailInfo.append(soup.select('#pdp-tabs > div')[0])
        # itemDetailInfo.append(soup.select('#pdp-tabs > div')[1])
        # self.__itemDetailInfo = itemDetailInfo

        # soup

        # self.__itemPrice = self.__driver.find_element_by_xpath(
        #     '/html/body/div[6]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/span/strong[2]').text

        # #info > div:nth-child(1) > div.d-content > p:nth-child(3) > img:nth-child(1)
        # //*[@id="info"]/div[1]/div[2]/p[1]/img[1]
        # //*[@id="info"]/div[1]/div[2]/p[1]/img[1]
        # //*[@id="info"]/div[1]/div[2]/p[1]/img[2]


        # //*[@id="info"]/div[1]/div[2]/p[8]/img[2]
        # //*[@id="info"]/div[1]/div[2]/p[8]/img[3]