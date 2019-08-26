/*
SQLyog Ultimate v9.63 
MySQL - 5.7.27-0ubuntu0.16.04.1 : Database - heatmap
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

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
    ('db448855c7a011e9878e00163e1caaa2','高陵区',NULL,0,'db448840c7a011e9878e00163e1caaa2');

/*Data for the table `t_province_dict` */

insert  into `t_province_dict`(`province_uuid`,`province_name`,`province_type`) values
    ('db448841c7a011e9878e00163e1caaa2','陕西省','0');

/*Data for the table `t_property_dict` */

insert  into `t_property_dict`(`property_uuid`,`property_name`,`property_type`) values
    ('db448857c7a011e9878e00163e1caaa2','住宅',0),
    ('db448858c7a011e9878e00163e1caaa2','商铺',0),
    ('db448859c7a011e9878e00163e1caaa2','写字楼',0);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
