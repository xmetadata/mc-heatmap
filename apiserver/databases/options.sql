/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 8.0.15 : Database - heatmap
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE `heatmap`;

/*Data for the table `t_options_data` */

insert  into `t_options_data`(`uuid`,`opt_key`,`opt_value`,`remark`,`createtime`,`updatetime`) values 
('db44887dc7a011e9878e00163e1caaa2','cookie','creiscity20161021=BdZX6Uc2x9HTBwxX533sIR5/NnMBowYHe/QISo+2L5mFkS6DS+bDekhnJ9w1WiFwJ2CNwnnE2dStkMutOeFwj/4q4uw8lP4ZAGT+a/wJ7e0Nnnba/ftQeeCek75BvN6Jgkw+YninJ11ViiqIj+NAxdZpk8j8iQ2j6gYZap/88KMiiTeqiy8MBe+XR2QqJFkxVv5SaZruLjeObFtyIhamj2yNdqmxcqdwNh2A6Jof50dht9lfxTpY8dlu7NnTBi0Tr2/0MMOMzDWI/yhETCO8ng+vt38KqH4rWMDwvLhGjn7ygT37xQlQB32V5FT1rgldO0HvDRxFEGZ/DKAkPGmrtT0V/pbMfN8lPcPwAQuaPlGMP8dsdHmBgfkPZN3WV12oMT7MvFnQz5E=; creiscitytemplate20161021=l9F9ERDRGyOaEE2vD4YXVeb3+9xt9ppkMOtwJUlaT7cNIs/+B4W6icpm/ILqD3uEGCkYlFOQJ0t6l6zvHfZ17zivN++tdjou4m81O/k9Ds/HE0Ltklu+3TemnkDGQt23t0m8qdTvcF2grmbe2lXy3XsLAr2V/BL4vWMPQznz3llVpAz8uCU2wA7eHD40jZ+8; global_cookie=qqund9ac5llkf8umza4erd25q10jzfkobyi; unique_cookie=U_qqund9ac5llkf8umza4erd25q10jzfkobyi*2; creisenterprisetemplate20161125=1; creisland20161122=7W/Y8L/hSwlQaIEcR1dLwzYDQjPo9FC8BAgcHCtez6EfX4acMZyJepymx/M8FWGaVFncjNUtuqyyDiQek8cI+DMRioQxftxfEZZG181vTNHRFtUu6fuqbPQfQ+3lG462Se20MZm0DHs/Fm88Yty8rxyB/DdrNcpbi6xpbreJli0=; creisuser2016=CLON3QqFdkMBluzHc9Sndf0rZTLfVGEhMfOGYPNrJ4v0SjmvbIGzIVY4xzn5/qBUR9AkL0JEk10DSsIoXlwhxcyp7Nd8B5yLc1uV8E+1lfgz5tNtDDNAiEVuKOKDWxBuC+RooWrOCZoDWT18fWkcs+W9j7+MsNPJX0WLLIJbzkM7zNTuQ2w0jwz66P3i367Bral8bl/tXh6s4CLn70tGf8yYZlajd37C+o4gND7NwP5fxMRsIVy5vNHMSZixNrDQ0o7lZNjb/Z6oaegAitD+Q6K9NFI0Dw9SuM1KLCxic0BlmnghRmFR5CI3rzqAnOcdSuYOfKVAPNOa/CNSWYkS0m8bdAbPMGO1Rx/ctjjIARAYylJpkseIJeL2uKIicRMiy8Al3hXw5erIT/FwjS1kwA5WcbJnehIDPMu2TDXgqSbidQLKD3OgBb6Fyo9j03eSYtmQrw/pIpXzMgzDH7w8d8Qh3Mi934tQpjGSfy2sUTS8OAKliUa0YsvWjUvr2t8HTPPWf0C/KU+bItVRyI6JXeZmvyM/Fbg9ea/GBOjUweEh4q/A8aCrvd8xv+GtvlUOLGG3r/qmp5jby10jTeUUpqdGHeu4RxZQ',NULL,NULL,NULL),
('db448899c7a011e9878e00163e1caaa2','spider_at','2019-01-01',NULL,NULL,NULL),
('db44889ac7a011e9878e00163e1caaa2','spider_status','0',NULL,NULL,NULL),
('db44889fc7a011e9878e00163e1caaa2','spider_args','{\"city\": [\"西安市:926123c5-6fc4-495e-8f9d-149c201ed933\"], \"stattype\" : [\"可售情况\", \"上市情况\", \"成交情况\"], \"property\": [\"普通住宅:2\", \"别墅:1\", \"公寓:12\", \"商业:8\", \"办公:15\"], \"arrange\" : {\"room\":[\"一室:334\", \"两室:335\", \"三室:336\", \"四室:337\", \"四室以上:338\", \"独立开间:339\", \"其他:340\", \"跃层:341\", \"错层:384\"], \"area\":[60, 180, 20], \"price\":[6000, 30000, 2000], \"amount\":[40, 300, 50]}}',NULL,NULL,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
