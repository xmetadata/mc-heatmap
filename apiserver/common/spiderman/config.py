# -*- coding: UTF-8 -*-
import logging

logging.basicConfig(level=logging.INFO,
                    filename='spiderman.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )
logger = logging.getLogger('spiderman')

STATDELTA = 10

DBSERVER = {
    'host': '47.103.36.82',
    'username': 'root',
    'password': 'Aa888888',
    'database': 'heatmap',
}

COOKIES = [
    {
        'name': 'creiscity20161021',
        'value': 'BdZX6Uc2x9HTBwxX533sIR5/NnMBowYHe/QISo+2L5mFkS6DS+bDekhnJ9w1WiFwJ2CNwnnE2dStkMutOeFwj/4q4uw8lP4ZAGT+a/wJ7e0Nnnba/ftQeeCek75BvN6Jgkw+YninJ11ViiqIj+NAxdZpk8j8iQ2j6gYZap/88KMiiTeqiy8MBe+XR2QqJFkxVv5SaZruLjeObFtyIhamj2yNdqmxcqdwNh2A6Jof50dht9lfxTpY8dlu7NnTBi0Tr2/0MMOMzDWI/yhETCO8ng+vt38KqH4rWMDwvLhGjn7ygT37xQlQB32V5FT1rgldO0HvDRxFEGZ/DKAkPGmrtT0V/pbMfN8lPcPwAQuaPlGMP8dsdHmBgfkPZN3WV12oMT7MvFnQz5E=',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'creiscitytemplate20161021',
        'value': 'l9F9ERDRGyOaEE2vD4YXVeb3+9xt9ppkMOtwJUlaT7cNIs/+B4W6icpm/ILqD3uEGCkYlFOQJ0t6l6zvHfZ17zivN++tdjou4m81O/k9Ds/HE0Ltklu+3TemnkDGQt23t0m8qdTvcF0um+cgpZYdhJbI997FBFB0a01r1k6tZSx4WsKbvVz2vcWixfJ3VxiV',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'global_cookie',
        'value': 'qc4jc3bxtb48x51bwwavzz86420k2hk0h45',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'creisuser2016',
        'value': 'CLON3QqFdkNy/6qhvJC74wmFOh/m4FLe7DUTiCqVsj3ZS+aShNsGx5GYfhipoayh/j3GsnEWTmiAFgZObNLC0QxrShHt7kVGNQtZae2+MzZ12dT5Yf929pLuYma57uCo0nJGWqzh4Ufg+S0KZFu/hcYucGo7AqhMja4jIQ9LQSIHTHz5iQQDCPhxWj9KnIrnmxGI6eKy4KoRrGyQSoFNT0czJbfDxnE8njY2Bi/ynp7AZPuYJ1dUiRbNnZYuRmI/crWoeQVMRur9l2+k258F/LffkDS7ZiUGyDwGuorYHqSQYBL+i0gdyjhu6Kpy5SqSC5fd3DuoTHJJTkz18ZGrbJIRibvC2oDlsE3ytx6leK5E7TK4qzYkg4i0yBRqeb9fkWoXKea+AVHeUqhOxBp9RYrQKiVFlIQxndSwOZK9/habXTO/hTLTMXpPANWkCOTcfAIonGwQvrV0qpdcn9jjNzZG9T8Qdp7nP+P0o3AbQKW474x1XhhB8EZkIjuok/fle0DwwxOkazjAUHfJ4be8ZyPjTSNGJCSB',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'rememberme_cn_data',
        'value': 'C14BCDE30B25A9B657B493C9E3B2D9B77A12FEFCF828333A30B1211ADA9D5CF4F577F4CCC9FF0BBBA0874040AFD7D2FCEB575BB70E2B74ED3F35B505D19700933AAD65E523173158DDBDCA91A8272BF66AF7A1B3CA37AFE8196095F806382259DF975A45989D4904DCDBEB5DBBF7E7EC081BDC389EF454ED7453026D6BD509614CD3936FEB3274B9',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'creis_city_user',
        'value': '1547ECF83A7B5C1142DF2F3D0361DA8F783406EBBC1D29F04E916A438E97B8BF7856E7EB84885FBCD694A0C6C1BE7FC9B13F7ECD48D85B03E92F901621265CC5D8CEF534F690ABB50FDE7489B67B1D6FD293F1573A585430528C0A4E8D2F1992D3D7A3C50FBD2AE8468CDFB692492305969EB3A6D0A3891D3BE19DBE9619246049ECD918BE6E3FF8EC5C2D1366746A8A7E44BF7359668CCBC79021B7C0D219A24E55E0BD676C71FECFE48116504729A4014F9C823461F7E974086CACAA364AB5DC3648D166A9567F0BDAE52BF2AC8A9F3C3E4FDCB2DF306C6BF0FCBB7B4111B40EDF666B4F8CDA35A871073DA8BE7BD7264E27F63784F1E0F2983FDC1794E573',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'creis_city_theme_color',
        'value': '1|red',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'IsLoginTodayForExpireDate',
        'value': '2019106',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'IsClickIknowForExpireDate',
        'value': '1',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    {
        'name': 'unique_cookie',
        'value': 'U_qc4jc3bxtb48x51bwwavzz86420k2hk0h45*20',
        'domain': '.creis.fang.com',
        'path': '/',
    }
]

STATTYPES = ['成交情况', '上市情况', '可售情况']
