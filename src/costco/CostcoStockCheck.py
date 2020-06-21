import os
import time
import pandas as pd
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException

from src.costco.CostcoItem import CostcoItem
from src.telegram.MyTelegram import MyTelegram as myTelegram
from src.utills import Utills

# 코스트코 물거의 재고와 가격변동을 체크 하기위한 클래스
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

        changePriceItems = []
        changeStockItems = []
        deleteItems = []  # 삭제된 상품에대한 정보를 담고있
        for i in range(urlLen):  # 반복문을 돌면서 각각 url에 접근하여 정보를 갱신한다.
            itemUrl = urlCsv['itemUrl'].iloc[i]

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

            try: # 상품 페이지 없어짐
                self.__driver.find_element_by_xpath('//*[@id="globalMessages"]/div[2]/div/div')
                deleteItemInfo = CostcoItem()
                deleteItemInfo.itemUrl = itemUrl
                if itemUrl in stockUrlMap:
                    itemIndex = stockUrlMap[itemUrl]
                    itemInfo = stockCsv.iloc[itemIndex]
                    deleteItemInfo.itemId = itemInfo['itemId']
                    deleteItemInfo.itemTitle = itemInfo['itemTitle']

                deleteItems.append(deleteItemInfo)
                continue
            except NoSuchElementException:
                print('page not error')


            # url 변경됐는지 체크(redirect)
            # if

            # url 변경된 부분 없음
            itemInfo = CostcoItem(self.__driver)
            itemInfo.itemUrl = itemUrl
            itemInfo.searchItemId()
            itemInfo.searchItemTitle()
            itemInfo.searchItemPrice()
            itemInfo.searchItemStockState()

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

                if str(itemInfo.itemStockState) != str(beforeItemInfo['stockState']):  # 재고 변동이 있음
                    beforeItemInfo.itemStockState = itemInfo.itemStockState
                    beforeItemInfo.stockState = itemInfo.itemStockState

                    print(beforeItemInfo.itemStockState)
                    print(beforeItemInfo.stockState)

                    stockCheckitemInfo = CostcoItem()
                    stockCheckitemInfo.itemId = beforeItemInfo['itemId']
                    stockCheckitemInfo.itemTitle = beforeItemInfo['itemTitle']
                    stockCheckitemInfo.itemUrl = beforeItemInfo['itemUrl']
                    changeStockItems.append(stockCheckitemInfo)
                    len(changeStockItems)

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