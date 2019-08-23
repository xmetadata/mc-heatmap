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

PROJECT_SYNC = {
    'statistic_type': [
        '成交情况',
        '上市情况',
        '可售情况'
    ],
    'statistic_url': 'https://creis.fang.com/city/PropertyStatistics/DetailsAjax',
    'url_header': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://creis.fang.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': '',
        },
    'url_payload': {
            "sTypeName": "",
            "sCityID": "926123c5-6fc4-495e-8f9d-149c201ed933",
            "sDealDataTableType": "week",
            "dBeginDate": "2019-06-23",
            "dEndDate": "2019-08-22",
            "sPropertyDistrictIds": "1230,1231,1232,1233,1234,99,1236,759,760,1237,761,2109,2110,2111,2112,2113,2114,2115,2116,2196",
            "sPropertyTypeIds": "2,1,12,8,15,5,20,7,10,3,9,46",
            "sBoardIds": "",
            "sRoomTypeIds": "334,335,336,337,338,339,340,341,384",
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
            "iPageSize": "15",
            "fixStatus": ""
        }
}

PROJECT_ATTR = {
    'statistic_type' : [
        '住宅',
        '商铺',
        '写字楼'
    ],
    'statistic_url': 'https://creis.fang.com/city/Property/GetPropertySearchInterface/',
    'url_header': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://creis.fang.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Cookie': '',
        },
    'url_payload': {
        "urlParams": {
                "sPropertyName": "",
                "sBuildcyc": "住宅,别墅,经济适用房",
                "sSaleDateBegin": "",
                "sSaleDateEnd": "",
                "sDeveloper": "",
                "sDistrictID": "1230,1231,1232,1233,1234,99,1236,759,760,1237,761,2109,2110,2111,2112,2113,2114,2115,2116,2196",
                "fPriceBegin": "",
                "fPriceEnd": "",
                "sCityZongID": "",
                "iCityBoradID": "",
                "sLivinDateBegin": "",
                "sLivinDateEnd": "",
                "sEnterpriseName": "",
                "sStatusID": "0,1,2",
                "sFIXSTATTUS": "1,2",
                "fPurposeAreaBegin": "",
                "fPurposeAreaEnd": "",
                "BuildCategory": "",
                "sColumns": "sAvgPrice,sDeveloper,sSaleTelphone,sStatus,sBuildcyc,sCHARACTER,BuildCategory,sFIXSTATTUS,sCityZone,sDistrict,sAddress,sSaleDate,sLivinDate,fGroundArea,fPurposeArea,fDimension,fVirescenceRate,sPropertyFee,sPropertyManage,sSaleCard,sTotalDoor",
                "sSortColumn": "housestatussaledate",
                "sStationId": "",
                "sProjectFeature": "",
                "sSortType": "0",
                "pageCount": "15",
                "iPageIndex": "1",
                "sCompleteStartDate": "",
                "sCompleteEndDate": ""
            },
            "proids": "",
            "type": "house"
        }
}

PROJECT_INFO = {

}