import os
import time
import pandas as pd
from datetime import datetime
from src.costco.CostcoItem import CostcoItem
from src.telegram.MyTelegram import MyTelegram as myTelegram


# import TelegramConst

#  코스트코 웹사이트에 등록되어 있는 상품의 가격과 재고 상태가 변경돠었는지 아닌지를 체크하고, 텔레그램으로 보내주는 작업을한다
# 사용방법
# 1. def telegramSend 내부에 toekn 값과 chatId 값을 자신의 텔레그램에서 알맞게 값을 부여한다
# 2. def job(): 내부에 webDriverPath에 자신의 크롬 브라우저 버전에 알맞는 크롬 브라우저 드라이버를 다운받고, 그 드라이버 경로를 저장한다.
# 3. schedule.every().day.at("11:30").do(job) 에 매일 몇시에 가격과 재고 변동을 체크할것인지 넣는다.
# 4. 터미널에서 실행 -> python3 check.py

# 가격 변동 플래그 값들
# stay(가격그대로), changed(가격변동됨)
# 재고 변동 플래그 값들
# sale(판매중), sold out(품절)

# 재고 상태 파싱한 데이터 기반으로 재고 상태 알아냄
from src.utills import Utills

# csv의 column 값   --> 'itemId', 'itemTitle', 'beforePrice', 'currentPrice', 'priceState','stockState', 'itemUrl'
# def job(): # 매일 실행하는 job
#     filePath = './costco_items/state'
#     fileName = '/result.csv'
#
#     Utills.createFolder(filePath)
#     Utills.createCsvFile(filePath + fileName)
#
#     webDriverPath = '/Users/tak/tak/python/cost-crawling/src/chromedriver'
#
#     itemInfo = getCsvFile(filePath + fileName)
#     priceChangeIndexList = [] # 상품 가격이 변한 index
#     stockChangeIndexList = [] # 재고 상태가 변한 index
#     deleteItemIndexList = [] # 삭제된 index
#
#     for i in itemInfo.index:
#         pageUrl = itemInfo.loc[i, 'itemUrl']
#         print('---url--- ' + pageUrl)
#
#         driver = getChromeDriver(webDriverPath)
#         driver.get(pageUrl)
#         # 해당 경로가 없어졌으면 하위로직 생략함
#         if driver.current_url == 'https://www.costco.co.kr/Kirkland-Signature/c/KirklandSignature':
#             deleteItemIndexList.append(i)
#             continue
#         elif driver.current_url != pageUrl: # 경로 변경된 경우 변경된 경로로 수정함
#             itemInfo.loc[i, 'itemUrl'] = driver.current_url
#         time.sleep(1)
#
#         # csv파일에 상품 아이디값 있는지 체크 (상품 아이디 값이 없을 때 상품 아이디값을 넣어준다)
#         if itemInfo.loc[i, 'itemId'] == '':
#             itemInfo.loc[i, 'itemId'] = driver.find_element_by_css_selector('.product-title-container .product-code .notranslate').text.strip()
#
#         # csv파일에 상품명이 있는지 체크 (상품명 없을 때 상품 아이디값을 넣어준다)
#         if itemInfo.loc[i, 'itemTitle'] == '':
#             itemInfo.loc[i, 'itemTitle'] = driver.find_element_by_css_selector('.product-page-container .product-title-container .product-name').text
#
#         # 할인 하는지 하지 않은지 체
#         normalPrice = -1
#         try:  # 할인 하는지 체크
#             normalPrice = driver.find_element_by_css_selector('.product-price-container .product-price-detail .price-after-discount .you-pay-value').text.replace(',', '')
#             print('할인함')
#         except NoSuchElementException:
#             normalPrice = driver.find_element_by_css_selector('.product-price-container .product-price-detail .price-original .notranslate').text.replace(',', '')
#             print('할인하지 않음')
#         normalPrice = normalPrice.replace('원', '')
#
#         if itemInfo.loc[i, 'currentPrice'] == '': # 가격 정보가 없을 때
#             itemInfo.loc[i, 'beforePrice'] = normalPrice
#             itemInfo.loc[i, 'currentPrice'] = normalPrice
#             itemInfo.loc[i, 'priceState'] = "stay"
#         elif normalPrice != itemInfo.loc[i, 'currentPrice']: # 가격 변동 생김
#             priceChangeIndexList.append(i)
#             itemInfo.loc[i, 'beforePrice'] = itemInfo.loc[i, 'currentPrice']
#             itemInfo.loc[i, 'currentPrice'] = normalPrice
#             itemInfo.loc[i, 'priceState'] = "changed"
#         else: # 가격이 변동되지 않음
#             print('가격변동 없음')
#             itemInfo.loc[i, 'priceState'] = "stay"
#
#         # 판매 상태 ("쇼핑카트에 담기", "품절" )
#         stockState = driver.find_element_by_css_selector('#addToCartForm .btn').text
#         if itemInfo.loc[i, 'stockState'] == '': # 재고 정보 없을 때
#             itemInfo.loc[i, 'stockState'] = stockCheck(stockState)
#         elif itemInfo.loc[i, 'stockState'] != stockCheck(stockState): # 재고 상태 변함
#             itemInfo.loc[i, 'stockState'] = stockCheck(stockState)
#             stockChangeIndexList.append(i)
#         else: # 재고 그대로
#             print('재고상태 그대로')
#
#         time.sleep(1)
#         driver.quit()
#
#     # 메새지 작성하기
#     # 가격 변동 메시지 작성
#     priceMessage = ''
#     if len(priceChangeIndexList) == 0:
#         priceMessage = '\n가격 변동 사항이 없습니다.'
#     else:
#         stockMessage = '\n가격 변동 사항이 있습니다.'
#         for i in priceChangeIndexList:
#             priceMessage += '\n\n-----가격 변동' + str(i+1) + '번째 상품----'
#             priceMessage += '\n아이템 이름\n' + itemInfo.loc[i, 'itemTitle']
#             priceMessage += '\n아이템 url\n' + itemInfo.loc[i, 'itemUrl']
#             priceMessage += '\n현재가격\n' + str(itemInfo.loc[i, 'currentPrice'])
#             priceMessage += '\n전가격\n' + str(itemInfo.loc[i, 'beforePrice'])
#
#     # 재고 변 메시지 작성
#     stockMessage = ''
#     if len(stockChangeIndexList) == 0:
#         stockMessage = '\n재고 변동 사항이 없습니다.'
#     else:
#         stockMessage = '\n재고 변동 사항이 있습니다.'
#         for j in stockChangeIndexList:
#             stockMessage += ('\n\n-----재고 변동' + str(j+1) + '번째 상품----')
#             stockMessage += '\n아이템 이름\n' + itemInfo.loc[j, 'itemTitle']
#             stockMessage += '\n아이템 url\n' + itemInfo.loc[j, 'itemUrl']
#             stockMessage += '\n아이템 재고 상태\n' + itemInfo.loc[j, 'stockState']
#
#     # 삭제된 상품 알림
#     deleteItemsMessage = ''
#     if len(deleteItemIndexList) == 0:
#         deleteItemsMessage = '\n삭제된 상품이 없습니다.'
#     else:
#         deleteItemsMessage = '\n삭제된 상품이 있습니다.'
#         for j in deleteItemIndexList:
#             deleteItemsMessage += ('\n\n-----삭제된 ' + str(j+1) + '번째 상품----')
#             deleteItemsMessage += '\n아이템 이름\n' + itemInfo.loc[j, 'itemTitle']
#             deleteItemsMessage += '\n아이템 url\n' + itemInfo.loc[j, 'itemUrl']
#
#     # 텔레그램 봇에 메시지 전송
#     # telegramSend(priceMessage)
#     # telegramSend(stockMessage)
#     # telegramSend(deleteItemsMessage)
#
#     # csv 최신정보로 파일로 수
#     itemInfo.to_csv(filePath + fileName)
#     # 현재 시간으로 csv 파일 생성
#     filePath = str(filePath) + str(datetime.today()) +'.csv'
#     itemInfo.to_csv(filePath)

# 2분에 한번씩 실행
# schedule.every(10).minutes.do(job)
# job()

# 매일 11:30 에 실행
# schedule.every().day.at("11:30").do(job)

# 무한루프를 돌면서 스케줄을 유지
# while 1:
#     schedule.run_pending()
#     time.sleep(1)

class CostcoStockCheck:
    __csvPath = './costco_items/state/'
    __itemUrlFile = 'itemUrls.csv'
    __itemStockFile = 'result.csv'

    def __init__(self, driver):
        self.__driver = driver

    def excute(self):
        urlCsv = self.loadUrlCsvFile()
        stockCsv = self.loadStockCsvFile()

        if len(urlCsv) == 0:
            return

        stockCsvLen = len(stockCsv)
        stockUrlMap = {}
        for i in range(stockCsvLen):
            itemUrl = stockCsv['itemUrl'].iloc[i]
            stockUrlMap[itemUrl] = i

        urlLen = len(urlCsv['itemUrl'])
        resultCsv = self.createStockCsvFile()
        for i in range(urlLen): # 반복문을 돌면서 각각 url에 접근하여 정보를 갱신한다.
            itemUrl = urlCsv['itemUrl'].iloc[i]

            deleteItems = [] # 삭제된 상품에대한 정보를 담고있
            self.__driver.get(itemUrl)
            time.sleep(5)
            #  현재 url이 삭제됨(더이상 상품 판매를 하지 않음을 의미하는 url)
            if self.__driver.current_url == 'https://www.costco.co.kr/Kirkland-Signature/c/KirklandSignature':
                deleteItemInfo = CostcoItem()
                deleteItemInfo.itemUrl = itemUrl
                if itemUrl in stockUrlMap: # 이미 상품정보에 등록되어 있는 url이면 아이템 정보를 변수에 저장함
                    itemIndex = stockUrlMap[itemUrl]
                    itemInfo = stockCsv.iloc[itemIndex]
                    deleteItemInfo.itemId = itemInfo['itemId']
                    deleteItemInfo.itemTitle = itemInfo['itemTitle']
                    deleteItems.append(deleteItemInfo)
                continue

            # url 변경됐는지 체크(redirect)
            # if

            # url 변경된 부분 없음
            itemInfo = CostcoItem(self.__driver)
            itemInfo.itemUrl = itemUrl
            itemInfo.searchItemId()
            itemInfo.searchItemTitle()
            itemInfo.searchItemPrice()
            itemInfo.searchItemStockState()

            changePriceItems = []
            changeStockItems = []
            # 상품 정보가 이미 등록되어 있는 경우 가격 변동이 있는지, 재고 변동이 있는지 체크한다
            if itemUrl in stockUrlMap:
                # resultCsv
                # ,itemId,itemTitle,beforePrice,currentPrice,priceState,stockState,itemUrl
                beforeItemInfo = stockCsv.iloc[stockUrlMap[itemUrl]].copy()
                print('---beforeItemInfo---')
                beforePrice = beforeItemInfo['currentPrice']

                # 가격 변동 확인하기
                if int(itemInfo.itemPrice) != int(beforeItemInfo['currentPrice']): # 가격 변동이 있음
                    beforeItemInfo['currentPrice'] = itemInfo.itemPrice
                    beforeItemInfo['priceState'] = 'change'
                    itemInfo = CostcoItem()
                    itemInfo.itemId = beforeItemInfo['itemId']
                    itemInfo.itemTitle = beforeItemInfo['itemTitle']
                    itemInfo.itemUrl = beforeItemInfo['itemUrl']
                    changePriceItems.append(itemInfo)
                else: # 가격 변동 없음
                    beforeItemInfo['priceState'] = 'stay'

                # 재고 변동 확인하기
                if itemInfo.itemStockState != beforeItemInfo['stockState']:  # 재고 변동이 있음
                    beforeItemInfo.itemStockState = itemInfo.itemStockState
                    itemInfo = CostcoItem()
                    itemInfo.itemId = beforeItemInfo['itemId']
                    itemInfo.itemTitle = beforeItemInfo['itemTitle']
                    itemInfo.itemUrl = beforeItemInfo['itemUrl']
                    changeStockItems.append(itemInfo)

                # 정보 하단에 추가로 넣기
                resultCsv.loc[len(resultCsv)] = [
                    beforeItemInfo.itemId,
                    beforeItemInfo.itemTitle,
                    beforeItemInfo.beforePrice,
                    beforeItemInfo.currentPrice,
                    beforeItemInfo.priceState,
                    beforeItemInfo.stockState,
                    beforeItemInfo.itemUrl
                ]

            else:   # 상품 정보가 등록되어 있지 않은 경우 신규 등록을 함
                # 새로운 행 추가하기
                insertRow = {}
                insertRow['itemId'] = itemInfo.itemId
                insertRow['itemTitle'] = itemInfo.itemTitle
                insertRow['beforePrice'] = itemInfo.itemPrice
                insertRow['currentPrice'] = itemInfo.itemPrice
                insertRow['itemUrl'] = itemInfo.itemUrl
                insertRow['priceState'] = 'stay'
                insertRow['stockState'] = itemInfo.itemStockState
                resultCsv.loc[len(resultCsv)] = [
                    itemInfo.itemId,
                    itemInfo.itemTitle,
                    itemInfo.itemPrice,
                    itemInfo.itemPrice,
                    'stay',
                    itemInfo.itemStockState,
                    itemInfo.itemUrl
                ]

        resultCsv.to_csv(self.__csvPath + self.__itemStockFile)
        # 현재 시간으로 csv 파일 생성
        resultCsv.to_csv(self.__csvPath + str(datetime.today()) + '.csv')

        #     텔레그램 전송
        deleteMessage = ''
        if len(deleteItems) != 0:
            deleteMessage += '\n--------------------\n'
            deleteMessage += '\n삭제된 아이템 갯수 : ' + str(len(deleteItems))
            for deleteItem in deleteItems:
                deleteMessage += '\n아이템 아이디 : ' + str(deleteItem.itemId)
                deleteMessage += '\n아이템 타이틀 : ' + str(deleteItem.itemTitle)
                deleteMessage += '\n아이템 url : ' + str(deleteItem.itemUrl)
                deleteMessage += '\n'
        else:
            deleteMessage = '\nurl이 삭제된 상품이 없습니다\n'

        changePriceMessage = ''
        if len(changePriceItems) != 0:
            changePriceMessage += '\n--------------------\n'
            changePriceMessage += '\n가격변동된 아이템 갯수 : ' + str(len(changePriceItems))
            for changePriceItem in changePriceItems:
                changePriceMessage += '\n아이템 아이디 : ' + str(changePriceItem.itemId)
                changePriceMessage += '\n아이템 타이틀 : ' + str(changePriceItem.itemTitle)
                changePriceMessage += '\n아이템 url : ' + str(changePriceItem.itemUrl)
                changePriceMessage += '\n'
        else:
            changePriceMessage = '\n 가격이 변동된 상품이 없습니다\n'

        changeStockMessage = ''
        if len(changeStockItems) != 0:
            changeStockMessage += '\n--------------------\n'
            changeStockMessage += '\n판매 상태 변동된 아이템 갯수 : ' + str(len(changeStockItems))
            for changeStockItem in changeStockItems:
                changeStockMessage += '\n아이템 아이디 : ' + str(changeStockItem.itemId)
                changeStockMessage += '\n아이템 타이틀 : ' + str(changeStockItem.itemTitle)
                changeStockMessage += '\n아이템 url : ' + str(changeStockItem.itemUrl)
                changeStockMessage += '\n'
        else:
            changeStockMessage = '\n 판매상태 변동된 상품이 없습니다\n'

        # 텔레그램에 메신저 전송하기
        myTelegram.telegramSend(deleteMessage)
        myTelegram.telegramSend(changePriceMessage)
        myTelegram.telegramSend(changeStockMessage)

        self.__driver.quit()

    def readCsvFile(self, path):
        return pd.read_csv(path, index_col=0)

    # urlcsv파일에서 중복된 url 제거하기
    def deleteDuplicateUrl(self, itemUrls):
        itemUrlMap = {}
        length = len(itemUrls)
        for i in itemUrls.index:
            url = itemUrls.loc[length - i - 1, 'url']
            if url in itemUrlMap:
                itemUrls.drop(length - i - 1)
                print('중복 삭제')
            else:
                print('저장')
                itemUrlMap[url] = i
            return itemUrls

    # url csv 파일 생성하기
    def createUrlCsvFile(self):
        pd.DataFrame({'itemUrl': [], \
                      }).to_csv(self.__csvPath + self.__itemUrlFile)

    # result csv 파일 생성하기
    def createStockCsvFile(self):
        return pd.DataFrame({'itemId': [], \
                      'itemTitle': [], \
                      'beforePrice': [], \
                      'currentPrice': [], \
                      'priceState': [], \
                      'stockState': [], \
                      'itemUrl': [], \
                      })

        #   아이템별url 저장해둔 csv 파일 읽어옴
    def loadUrlCsvFile(self):
        Utills.createFolder(self.__csvPath)
        if os.path.isfile(self.__csvPath + self.__itemUrlFile) == False:  # itemUrl.csv 파일이 없으면 파일 생성
            self.createUrlCsvFile()

        itemUrls = self.readCsvFile(self.__csvPath + self.__itemUrlFile)
        # 중복된 url 제거하기 후 다시 저장
        # self.deleteDuplicateUrl(itemUrls).to_csv(self.__csvPath + self.__itemUrlFile)
        itemUrls.to_csv(self.__csvPath + self.__itemUrlFile)
        return self.readCsvFile(self.__csvPath + self.__itemUrlFile)

    def loadStockCsvFile(self):
        Utills.createFolder(self.__csvPath)
        if os.path.isfile(self.__csvPath + self.__itemStockFile) == False: # result.csv 파일이 없으면 파일 생성
            self.createStockCsvFile().to_csv(self.__csvPath + self.__itemStockFile)
        return self.readCsvFile(self.__csvPath + self.__itemStockFile)

    def stockState(self, str):
        stockState = {
            '쇼핑카트에 담기': 'sale',
            '품절': 'sold out'
        }
        return stockState(str)