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
        'name': 'creisuser2016',
        'value': 'CLON3QqFdkOEuQIOcii4V84eROTUg8PMmj2UfTl8MeKqx6oKeeOHiXqLFksDP11AgPexjbTCfx/xX3mz2o0puufejkII1EoNZ1TOxM5pT9V265zqyyZTZeCYEzhkDSwjM7rD7XkZoDIfPUGvqe/GXb7pgM1zfHlDDSwyOVrVSA7l+UxhlvfpjBunyUisQDVETLMWPAY0H47T3iF0icNnDOckhUCqKm3GRrn89E6pZX5lWidH97KMJoGWuqVb1N62OAsdeihMeQZqW4fM3sX8+w2XRzI0M1cbl1FNkxZQxmMX5Bm2Xq+poy/38AjQF+HvhKXJAfC24Y1S8E+G0iznHWNSpzoMrKtG1M4vBcANosumMcNFlwA12fd0SNfyi0VkW95F1pqgkDGBtwatG+AF7unD4grf/BJH9q9YDXSoA8NMk5Nkdk6GGFUMNwzq/w/733gCjcLiLms0I8hv5KFLXcJteHpQjHgQ1K4l9uZuNaJ6ObPvuGJGc9ZKkl4kRl5DJ85wO3x0t502Eh6mL5RvLoZguB2gT1HcHbtA3XUQdLbtDJDK49y/wLu9nQXXYYJsiD+9vddjzKO3ah0a07fEXRWwpIfoZOoy',
        'domain': '.creis.fang.com',
        'path': '/',
    },
    # {
    #     'name': 'creiscity20161021',
    #     'value': 'BdZX6Uc2x9HTBwxX533sIR5/NnMBowYHe/QISo+2L5mFkS6DS+bDekhnJ9w1WiFwJ2CNwnnE2dStkMutOeFwj/4q4uw8lP4ZAGT+a/wJ7e0Nnnba/ftQeeCek75BvN6Jgkw+YninJ11ViiqIj+NAxdZpk8j8iQ2j6gYZap/88KMiiTeqiy8MBe+XR2QqJFkxVv5SaZruLjeObFtyIhamj2yNdqmxcqdwNh2A6Jof50dht9lfxTpY8dlu7NnTBi0Tr2/0MMOMzDWI/yhETCO8ng+vt38KqH4rWMDwvLhGjn7ygT37xQlQB32V5FT1rgldO0HvDRxFEGZ/DKAkPGmrtT0V/pbMfN8lPcPwAQuaPlGMP8dsdHmBgfkPZN3WV12oMT7MvFnQz5E=',
    #     'domain': '.creis.fang.com',
    #     'path': '/',
    # },
    # {
    #     'name': 'creiscitytemplate20161021',
    #     'value': 'l9F9ERDRGyOaEE2vD4YXVeb3+9xt9ppkMOtwJUlaT7cNIs/+B4W6icpm/ILqD3uEGCkYlFOQJ0t6l6zvHfZ17zivN++tdjou4m81O/k9Ds/HE0Ltklu+3TemnkDGQt23t0m8qdTvcF2grmbe2lXy3Z0RxdpzNk/qaffNOOAijHXYvkI7V0/kkadk5YNoFzax',
    #     'domain': '.creis.fang.com',
    #     'path': '/',
    # },
]

STATTYPES = ['成交情况', '上市情况', '可售情况']
