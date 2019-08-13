# -*- coding: UTF-8 -*-
import logging

logging.basicConfig(level=logging.INFO,
                    filename='synctask.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('synctask')

DB = {
    'host': '47.103.36.82',
    'username': 'root',
    'password': 'Aa888888',
    'database': 'heatmap',
}

POOLSIZE = 30

STATGAP = -10

CURRENT_PROJECT = {}

PROJECT_PAYLOAD = {
    "house": {
        "sPropertyName": "",
        "sBuildcyc": "",
        "sSaleDateBegin": "",
        "sSaleDateEnd": "",
        "sDeveloper": "",
        "sDistrictID": "",
        "fPriceBegin": "",
        "fPriceEnd": "",
        "sCityZongID": "",
        "iCityBoradID": "",
        "sLivinDateBegin": "",
        "sLivinDateEnd": "",
        "sEnterpriseName": "",
        "sStatusID": "",
        "sFIXSTATTUS": "",
        "fPurposeAreaBegin": "",
        "fPurposeAreaEnd": "",
        "BuildCategory": "",
        "sColumns": "sAvgPrice,sDeveloper,sSaleTelphone,sStatus,sBuildcyc,sCHARACTER,BuildCategory,sFIXSTATTUS,sCityZone,sDistrict,sAddress,sSaleDate,sLivinDate,fGroundArea,fPurposeArea,fDimension,fVirescenceRate,sPropertyFee,sPropertyManage,sSaleCard,sTotalDoor",
        "sSortColumn": "housestatussaledate",
        "sStationId": "",
        "sProjectFeature": "",
        "sSortType": "0",
        "pageCount": "100",
        "iPageIndex": "1",
        "sCompleteStartDate": "",
        "sCompleteEndDate": "",
    },
    "shop": {
        "sPropertyName": "",
        "sTypeName": "",
        "priceType": "0",
        "fPriceBegin": "",
        "fPriceEnd": "",
        "sDeveloper": "",
        "sDistrictID": "",
        "sSaleDateBegin": "",
        "sSaleDateEnd": "",
        "sPropertyManage": "",
        "sBusiness": "",
        "sCityZongID": "",
        "iCityBoradID": "",
        "fPurposeAreaBegin": "",
        "fPurposeAreaEnd": "",
        "sStatusID": "",
        "sFIXSTATTUS": "",
        "fAreaBegin": "",
        "fAreaEnd": "",
        "sColumns": "sAvgPrice,sDeveloper,sSaleTelphone,sStatus,sTypeName,sCHARACTER,sSaleDate,sFIXSTATTUS,sCityZone,sDistrict,sAddress,fGroundArea,fPurposeArea,fDimension,fVirescenceRate,sPropertyFee,sPropertyManage,sSaleCard",
        "sSortColumn": "shopdopendate",
        "sStationId": "",
        "sProjectFeature": "",
        "sSortType": "0",
        "pageCount": "100",
        "iPageIndex": "1",
        "sCompleteStartDate": "",
        "sCompleteEndDate": ""
    },
    "office": {
        "sPropertyName": "",
        "sTypeName": "",
        "priceType": "0",
        "fPriceBegin": "",
        "fPriceEnd": "",
        "sDeveloper": "",
        "sDistrictID": "",
        "sLiveDateBegin": "",
        "sLiveDateEnd": "",
        "sPropertyManage": "",
        "sBusiness": "",
        "sCityZongID": "",
        "iCityBoradID": "",
        "fPurposeAreaBegin": "",
        "fPurposeAreaEnd": "",
        "sStatusID": "",
        "sFIXSTATTUS": "",
        "sSaleDateBegin": "",
        "sSaleDateEnd": "",
        "sColumns": "sAvgPrice,sDeveloper,sSaleTelphone,sStatus,sTypeName,sCHARACTER,sSaleDate,sFIXSTATTUS,sCityZone,sDistrict,sAddress,fGroundArea,fPurposeArea,fDimension,fVirescenceRate,sPropertyFee,sPropertyManage,sSaleCard",
        "sSortColumn": "newofficesaledate",
        "sStationId": "",
        "sProjectFeature": "",
        "sSortType": "0",
        "pageCount": "100",
        "iPageIndex": "1",
        "sCompleteStartDate": "",
        "sCompleteEndDate": ""
    },
}

TEST_PAYLOAD = {
    "sTypeName": "成交情况",
    "sCityID": "926123c5-6fc4-495e-8f9d-149c201ed933",
    "sDealDataTableType": "week",
    "dBeginDate": "2019-01-01",
    "dEndDate": "2019-01-01",
    "sPropertyDistrictIds": "",
    "sPropertyTypeIds": "2",
    "sBoardIds": "",
    "sRoomTypeIds": "",
    "sCityZoneIds": "",
    "fRoomAreaBegin": "",
    "fRoomAreaEnd": "",
    "fRoomPriceBegin": "",
    "fRoomPriceEnd": "",
    "fRoomAmountBegin": "",
    "fRoomAmountEnd": "",
    "iTotalFloorBegin": "",
    "iTotalFloorEnd": "",
    "sPropertyName": "",
    "sOrderName": "dealnum",
    "sOrderType": "desc",
    "iPageIndex": "1",
    "iPageSize": "1"
}

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://creis.fang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Cookie': '',
}
