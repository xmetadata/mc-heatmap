/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 5.7.27-0ubuntu0.16.04.1 : Database - heatmap
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE `heatmap`;

/*Data for the table `t_city_dict` */

insert  into `t_city_dict`(`city_uuid`,`city_name`,`city_type`,`province_uuid`) values 
('db448840c7a011e9878e00163e1caaa2','西安市','0','db448841c7a011e9878e00163e1caaa2');

/*Data for the table `t_district_dict` */

insert  into `t_district_dict`(`district_uuid`,`district_name`,`district_range`,`district_type`,`city_uuid`) values 
('db448842c7a011e9878e00163e1caaa2','曲江新区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448843c7a011e9878e00163e1caaa2','经济技术开发区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448844c7a011e9878e00163e1caaa2','长安区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448845c7a011e9878e00163e1caaa2','浐灞生态区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448846c7a011e9878e00163e1caaa2','灞桥区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448847c7a011e9878e00163e1caaa2','碑林区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448848c7a011e9878e00163e1caaa2','国际港务区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448849c7a011e9878e00163e1caaa2','鄠邑区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44884ac7a011e9878e00163e1caaa2','莲湖区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44884bc7a011e9878e00163e1caaa2','未央区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44884cc7a011e9878e00163e1caaa2','新城区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44884dc7a011e9878e00163e1caaa2','雁塔区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44884ec7a011e9878e00163e1caaa2','国家民用航天产业基地',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44884fc7a011e9878e00163e1caaa2','周至县',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448850c7a011e9878e00163e1caaa2','阎良区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448851c7a011e9878e00163e1caaa2','西咸新区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448852c7a011e9878e00163e1caaa2','临潼区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448853c7a011e9878e00163e1caaa2','蓝田县',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448854c7a011e9878e00163e1caaa2','高新技术开发区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448855c7a011e9878e00163e1caaa2','高陵区',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44885ec7a011e9878e00163e1caaa2','城东',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db44885fc7a011e9878e00163e1caaa2','城南',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448860c7a011e9878e00163e1caaa2','城西',NULL,0,'db448840c7a011e9878e00163e1caaa2'),
('db448861c7a011e9878e00163e1caaa2','城北',NULL,0,'db448840c7a011e9878e00163e1caaa2');

/*Data for the table `t_housingtype_dict` */

insert  into `t_housingtype_dict`(`housetype_uuid`,`housetype_name`,`housetype_type`,`spider_map`) values 
('db448872c7a011e9878e00163e1caaa2','一室',0,'334'),
('db448873c7a011e9878e00163e1caaa2','两室',0,'335'),
('db448874c7a011e9878e00163e1caaa2','三室',0,'336'),
('db448875c7a011e9878e00163e1caaa2','四室',0,'337'),
('db448876c7a011e9878e00163e1caaa2','四室以上',0,'338'),
('db448877c7a011e9878e00163e1caaa2','其他',0,'339'),
('db448878c7a011e9878e00163e1caaa2','跃层',0,'341'),
('db448879c7a011e9878e00163e1caaa2','错层',0,'384'),
('db44887ac7a011e9878e00163e1caaa2','独立开间',0,'340');

/*Data for the table `t_options_data` */

insert  into `t_options_data`(`uuid`,`opt_key`,`opt_value`,`remark`,`createtime`,`updatetime`) values 
('db448856c7a011e9878e00163e1caaa2','cookie','creiscity20161021=BdZX6Uc2x9HTBwxX533sIR5/NnMBowYHe/QISo+2L5mFkS6DS+bDekhnJ9w1WiFwJ2CNwnnE2dStkMutOeFwj/4q4uw8lP4ZAGT+a/wJ7e0Nnnba/ftQeeCek75BvN6Jgkw+YninJ11ViiqIj+NAxdZpk8j8iQ2j6gYZap/88KMiiTeqiy8MBe+XR2QqJFkxVv5SaZruLjeObFtyIhamj2yNdqmxcqdwNh2A6Jof50dht9lfxTpY8dlu7NnTBi0Tr2/0MMOMzDWI/yhETCO8ng+vt38KqH4rWMDwvLhGjn7ygT37xQlQB32V5FT1rgldO0HvDRxFEGZ/DKAkPGmrtT0V/pbMfN8lPcPwAQuaPlGMP8dsdHmBgfkPZN3WV12oMT7MvFnQz5E=; creiscitytemplate20161021=l9F9ERDRGyOaEE2vD4YXVeb3+9xt9ppkMOtwJUlaT7cNIs/+B4W6icpm/ILqD3uEGCkYlFOQJ0t6l6zvHfZ17zivN++tdjou4m81O/k9Ds/HE0Ltklu+3TemnkDGQt23t0m8qdTvcF2grmbe2lXy3XsLAr2V/BL4vWMPQznz3llVpAz8uCU2wA7eHD40jZ+8; global_cookie=qqund9ac5llkf8umza4erd25q10jzfkobyi; unique_cookie=U_qqund9ac5llkf8umza4erd25q10jzfkobyi*2; creisenterprisetemplate20161125=1; creisland20161122=7W/Y8L/hSwlQaIEcR1dLwzYDQjPo9FC8BAgcHCtez6EfX4acMZyJepymx/M8FWGaVFncjNUtuqyyDiQek8cI+DMRioQxftxfEZZG181vTNHRFtUu6fuqbPQfQ+3lG462Se20MZm0DHs/Fm88Yty8rxyB/DdrNcpbi6xpbreJli0=; creisuser2016=CLON3QqFdkMBluzHc9Sndf0rZTLfVGEhMfOGYPNrJ4v0SjmvbIGzIVY4xzn5/qBUR9AkL0JEk10DSsIoXlwhxcyp7Nd8B5yLc1uV8E+1lfgz5tNtDDNAiEVuKOKDWxBuC+RooWrOCZoDWT18fWkcs+W9j7+MsNPJX0WLLIJbzkM7zNTuQ2w0jwz66P3i367Bral8bl/tXh6s4CLn70tGf8yYZlajd37C+o4gND7NwP6Ge76mKqty1i/l9QF/0ZopRXTSgheR7/FevTRuniD6SE3AFgFzrLd62TbHOVrC0dWCR/r8vLx1eyOjjJAxGB43CHa8sefdxqYcOGQW8+cauldBVSYuBOc7As4ddzkKzCUtwfTW7CZRBIEKgen/Wmn1mNFiN/w34ap1+wegQEbiCgCyD1BiqkZojHhfLY0WkXnaWPhgC1esM0xbv2HFa2NFiShrKfpzj98Oq4R4nnsdqDojSmcpsz8CdpKGIsjr9S5zZRgrRV1MC0EhnBaVtST9JRfC5QsxqUXSTs/BWfxiZBQT6bCAmCYZ3cYGEjBsTQdf7Lk1IGCcYxa6WDTL8wHOavL9wtmuXXJ3Euv8beE5myOByJE2SN0/',NULL,NULL,NULL);

/*Data for the table `t_property_dict` */

insert  into `t_property_dict`(`property_uuid`,`property_name`,`property_type`) values 
('db448857c7a011e9878e00163e1caaa2','住宅',0),
('db448858c7a011e9878e00163e1caaa2','商铺',0),
('db448859c7a011e9878e00163e1caaa2','写字楼',0);

/*Data for the table `t_province_dict` */

insert  into `t_province_dict`(`province_uuid`,`province_name`,`province_type`) values 
('db448841c7a011e9878e00163e1caaa2','陕西省','0');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
