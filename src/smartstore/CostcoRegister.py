import time
from selenium.webdriver.common.keys import Keys
from src.consts.SmartStoreAuthConst import smartStoreAuthConst
import src.utills.Utills as Utills

# 스마트 스토어 상품 등록하기
# 로그인후 상품 정보 자동등록 -> 상세페이지까지 입력후 완료됨

# 사용법
# driver = Utills.getChromeDriver(webDriverPath)
# store = SmartStoreItemRegister(driver)
# store.itemId = costcoItem.itemId
# store.priceMarginRate = 1.08  # 8% 마진
# store.itemTitle = costcoItem.itemTitle
# store.itemPrice = costcoItem.itemPrice
# store.itemImgs = costcoItem.itemImgs
# store.itemDetailInfo = costcoItem.itemDetailInfo
# store.excute()

class SmartStoreItemRegister:
    def __init__(self, driver):
        self.__driver = driver
        self.__itemId = ''
        self.__itemTitle = ''
        self.__itemPrice = ''
        self.__imgs = []
        self.__itemDetailInfo = []
        self.__priceMarginRate = ''
        self.__itemAvailableStock = 20

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
    def itemAvailableStock(self):
        return self.__itemAvailableStock

    @itemAvailableStock.setter
    def itemAvailableStock(self, str):
        self.__itemAvailableStock = str

    @property
    def itemImgs(self):
        return self.__itemImgs

    @itemImgs.setter
    def itemImgs(self, imgs):
        self.__itemImgs = imgs

    @property
    def itemPrice(self):
        return self.__itemPrice

    @itemPrice.setter
    def itemPrice(self, price):
        self.__itemPrice = price

    @property
    def priceMarginRate(self):
        return self.__priceMarginRate

    @priceMarginRate.setter
    def priceMarginRate(self, rate):
        self.__priceMarginRate = rate

    @property
    def itemDetailInfo(self):
        return self.__itemDetailInfo

    @itemDetailInfo.setter
    def itemDetailInfo(self, itemDetailInfo):
        self.__itemDetailInfo = itemDetailInfo

    #     스마트스토어 로그인 -> 상품 등록페이지로 이동 -> 상품 정보 및 아미지 등록 -> 배달 정보 입력 -> 아이템 상세 페이지 입력 -> 완료
    def excute(self):
        self.login()
        self.moveAddPage()
        self.setItemInfo()
        self.setImgs()
        self.setDeleveryOption()
        self.setItemDetailInfo()
        return self

    # 로그인
    def login(self):
        startStoreLoginPath = 'https://sell.smartstore.naver.com/#/login'
        self.__driver.get(startStoreLoginPath)
        time.sleep(5)
        idText = smartStoreAuthConst('id')
        pwText = smartStoreAuthConst('pw')
        idInput = self.__driver.find_element_by_css_selector('#loginId')
        pwInput = self.__driver.find_element_by_css_selector('#loginPassword')
        idInput.send_keys(idText)
        pwInput.send_keys(pwText)
        self.__driver.find_element_by_css_selector('#loginButton').click()
        time.sleep(4)

    # 상품 등록 페이지로 이동
    def moveAddPage(self):
        smartStoreregisterPath = 'https://sell.smartstore.naver.com/#/products/create'
        self.__driver.get(smartStoreregisterPath)
        time.sleep(4)

    # 이미지 등록
    def setImgs(self):
        if len(self.itemImgs) != 0:
            Utills.movingTop(self.__driver.find_element_by_xpath('//*[@id="productForm"]/ng-include/ui-view[10]'))
            # main 이미지
            self.__driver.find_element_by_css_selector("#representImage .btn-add-img").send_keys(Keys.ENTER)
            time.sleep(3)
            self.__driver.switch_to.window(self.__driver.window_handles[0])
            self.__driver.find_element_by_css_selector("input[type='file']").send_keys(self.itemImgs[0])
            time.sleep(10)
            # sub 이미지
            self.__driver.find_element_by_css_selector("#optionalImages .btn-add-img").send_keys(Keys.ENTER)
            time.sleep(3)
            optionalImgs = "\n ".join(self.itemImgs)
            self.__driver.find_element_by_css_selector("input[type='file']").send_keys(optionalImgs)
            time.sleep(20)

    #     배송 옵션 설정
    def setDeleveryOption(self):
        self.__driver.switch_to.window(self.__driver.window_handles[0])
        Utills.movingTop(self.__driver.find_element_by_xpath(
            '//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div/div/div/a')).send_keys(Keys.ENTER)  # 배송창 탭 열기
        time.sleep(1)
        Utills.movingTop(self.__driver.find_element_by_xpath(
            '//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div[2]/div/div[1]/div/div/div[1]/div/label[1]')).click()  # 배송여부 -> 배송
        Utills.movingTop(self.__driver.find_element_by_xpath(
            '//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/label[1]')).click()  # 배송방법 -> 택배
        Utills.movingTop(self.__driver.find_element_by_xpath(
            '//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div[2]/div/ng-include/div/div[1]/div/div/div[1]/div[1]/div/label[1]')).click()  # 배송속성 -> 일반배송
        Utills.movingTop(self.__driver.find_element_by_xpath(
            '//*[@id="productForm"]/ng-include/ui-view[16]/div[1]/div[2]/div/div[6]/div/div[1]/div[1]/div/label[2]')).click()  # 묶음 배송 -> 불가(개별계산)

    #     마진 퍼센트를 붙인 가격을 계산하
    def calMarginPrice(self):
        price = int(self.itemPrice.replace('원', '').replace(',', ''))
        priceMarginRate = float(self.priceMarginRate)
        marginPrice = price * priceMarginRate
        return int(round(marginPrice,-2))   # 백원단위까지 표

    #  상품 기본 정보 입력 (상품이름, 가격, 재고)
    def setItemInfo(self):
        self.__driver.find_element_by_css_selector(
            '.input-content .form-section-sub .form-group input[name="product.name"]').send_keys(
            self.itemTitle)
        self.__driver.find_element_by_css_selector(
            '.input-content .form-section-sub .form-group input[name="product.salePrice"]').send_keys(
            self.calMarginPrice())
        self.__driver.find_element_by_css_selector(
            '.input-content .form-section-sub .form-group input[name="product.stockQuantity"]').send_keys(
            self.itemAvailableStock)

    #     상품 상세 정보 입력
    def setItemDetailInfo(self):
        self.__driver.find_element_by_css_selector('.seller-product-detail .content .btn-area button').send_keys(Keys.ENTER)
        time.sleep(10)
        windows = self.__driver.window_handles
        self.__driver.switch_to.window(windows[1])
        # 상품 상세정보1 입력
        style1 = '<style> a{text-decoration:"none" !important;}</style>'   # a태그 밑줄 지움
        self.writeDetailInfo(style1 + str(self.itemDetailInfo[0]))

        # 이미지 등록
        if len(self.itemImgs) != 0:
            self.__driver.switch_to.window(windows[1])
            self.__driver.find_element_by_xpath('//*[@id="one-editor"]/div/div[1]/div/header/div[1]/ul/li[1]/button').click()
            time.sleep(3)
            imgs = "\n ".join(self.itemImgs)
            self.__driver.switch_to.window(self.__driver.window_handles[1])
            self.__driver.find_element_by_css_selector("input[type='file']").send_keys(imgs)

        # 상세정보2(스펙) 입력
        self.writeDetailInfo(style1 + str(self.itemDetailInfo[1]))
        time.sleep(10)
        # 상품상세 등록하기
        self.__driver.find_element_by_css_selector('.header-editor button').send_keys(Keys.ENTER)
        time.sleep(1)
        self.__driver.switch_to.window(windows[0])

    def writeDetailInfo(self, infoTag):
        self.__driver.find_element_by_css_selector('.se-shopping-html-toolbar-button.se-document-toolbar-custom-button.se-text-icon-toolbar-button').send_keys(Keys.ENTER)
        time.sleep(10)
        self.__driver.find_element_by_css_selector('#textarea').click()
        self.__driver.find_element_by_css_selector('#textarea').send_keys('<br>' + str(infoTag).replace('\t', "") + '<br>')
        self.__driver.find_element_by_css_selector('.seller-btn-area button').send_keys(Keys.ENTER)
        time.sleep(5)