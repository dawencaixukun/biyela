/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.18-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: health_platform
-- ------------------------------------------------------
-- Server version	10.11.18-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ai_suggestion_record`
--

DROP TABLE IF EXISTS `ai_suggestion_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_suggestion_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `summary_type` varchar(50) DEFAULT '阶段运动总结',
  `workout_count` int(11) DEFAULT 0,
  `total_duration` int(11) DEFAULT 0,
  `total_burned` decimal(6,1) DEFAULT 0.0,
  `ai_content` text NOT NULL,
  `disclaimer` varchar(255) DEFAULT '本建议由大模型根据运动数据分析生成，仅供日常健身管理参考，不作为医疗诊断依据。',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ai_suggestion_record_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_suggestion_record`
--

LOCK TABLES `ai_suggestion_record` WRITE;
/*!40000 ALTER TABLE `ai_suggestion_record` DISABLE KEYS */;
INSERT INTO `ai_suggestion_record` VALUES
(1,2,'周度运动综合分析',5,185,1580.0,'### 📋 近期个人运动与健康概况\n在过去的 7 天里，您共坚持打卡 **5** 次，累计运动时长达 **185** 分钟，累计消耗能量约 **1580.0** kcal。您主要的运动项目为：户外慢跑(1次)、力量训练(1次)、动感单车(1次)、自由泳(1次)、高强度跳绳(1次)。整体锻炼节奏保持得非常不错，展现了良好的自我管理习惯。\n\n### ⚖️ 身体体征与目标进度\n您当前身高 175.00cm，体重 68.50kg，计算得出 BMI 为 **22.4**（处于 **正常标准** 区间），目标体重为 65.00kg。\n正在推进的运动计划包括：本月户外累计跑量 已完成 35.2/50.0公里；阶段减脂达标目标 已完成 68.5/65.0公斤；每周抗阻训练打卡 已完成 8.0/12.0次。建议继续按既定节奏稳步推进。\n\n### 💡 针对性运动与生活建议\n1. **张弛有度，注意恢复**：您的运动频次较为积极，高强度训练之间建议安排 1 天的主动休息日或低强度瑜伽拉伸，让骨骼肌纤维得到充分超量恢复。\n2. **合理搭配有氧与抗阻**：慢跑、单车等有氧运动有助于消耗热量提升耐力，建议穿插哑铃、深蹲等抗阻力量动作，保护基础代谢率，避免减脂过程中的瘦体重流失。\n3. **规律水合与营养供给**：根据您的体重测算，每日推荐饮水量约为 2398 ml。运动前后少量多次补水，运动后 30-45 分钟内适量补充优质蛋白（如蛋清、酸奶、瘦肉）与复合碳水。','本建议由大模型根据运动数据分析生成，仅供日常健身管理参考，不作为医疗诊断依据。','2026-09-29 11:14:47'),
(2,2,'周度运动综合分析',5,185,1580.0,'### 📋 近期个人运动与健康概况\n在过去的 7 天里，您共坚持打卡 **5** 次，累计运动时长达 **185** 分钟，累计消耗能量约 **1580.0** kcal。您主要的运动项目为：户外慢跑(1次)、力量训练(1次)、动感单车(1次)、自由泳(1次)、高强度跳绳(1次)。整体锻炼节奏保持得非常不错，展现了良好的自我管理习惯。\n\n### ⚖️ 身体体征与目标进度\n您当前身高 175.00cm，体重 68.50kg，计算得出 BMI 为 **22.4**（处于 **正常标准** 区间），目标体重为 65.00kg。\n正在推进的运动计划包括：本月户外累计跑量 已完成 35.2/50.0公里；阶段减脂达标目标 已完成 68.5/65.0公斤；每周抗阻训练打卡 已完成 8.0/12.0次。建议继续按既定节奏稳步推进。\n\n### 💡 针对性运动与生活建议\n1. **张弛有度，注意恢复**：您的运动频次较为积极，高强度训练之间建议安排 1 天的主动休息日或低强度瑜伽拉伸，让骨骼肌纤维得到充分超量恢复。\n2. **合理搭配有氧与抗阻**：慢跑、单车等有氧运动有助于消耗热量提升耐力，建议穿插哑铃、深蹲等抗阻力量动作，保护基础代谢率，避免减脂过程中的瘦体重流失。\n3. **规律水合与营养供给**：根据您的体重测算，每日推荐饮水量约为 2398 ml。运动前后少量多次补水，运动后 30-45 分钟内适量补充优质蛋白（如蛋清、酸奶、瘦肉）与复合碳水。','本建议由大模型根据运动数据分析生成，仅供日常健身管理参考，不作为医疗诊断依据。','2026-09-29 11:18:50');
/*!40000 ALTER TABLE `ai_suggestion_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `body_metrics`
--

DROP TABLE IF EXISTS `body_metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `body_metrics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `height` decimal(5,2) NOT NULL,
  `weight` decimal(5,2) NOT NULL,
  `bmi` decimal(4,1) NOT NULL,
  `systolic_bp` int(11) DEFAULT 120,
  `diastolic_bp` int(11) DEFAULT 80,
  `heart_rate` int(11) DEFAULT 72,
  `record_date` date NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_date` (`user_id`,`record_date`),
  CONSTRAINT `body_metrics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `body_metrics`
--

LOCK TABLES `body_metrics` WRITE;
/*!40000 ALTER TABLE `body_metrics` DISABLE KEYS */;
INSERT INTO `body_metrics` VALUES
(1,2,175.00,69.80,22.8,118,78,70,'2026-09-20','2026-09-26 01:36:35'),
(2,2,175.00,69.40,22.7,118,78,70,'2026-09-21','2026-09-26 01:36:35'),
(3,2,175.00,69.20,22.6,118,78,70,'2026-09-22','2026-09-26 01:36:35'),
(4,2,175.00,69.00,22.5,118,78,70,'2026-09-23','2026-09-26 01:36:35'),
(5,2,175.00,68.80,22.5,118,78,70,'2026-09-24','2026-09-26 01:36:35'),
(6,2,175.00,68.60,22.4,118,78,70,'2026-09-25','2026-09-26 01:36:35'),
(7,2,175.00,68.50,22.4,120,80,72,'2026-09-26','2026-09-26 01:36:35'),
(8,4,175.00,67.00,21.9,120,80,72,'2026-09-26','2026-09-26 01:54:26'),
(9,3,175.00,68.50,22.4,120,80,72,'2026-09-26','2026-09-26 10:32:57'),
(11,5,175.00,68.00,22.2,120,80,72,'2026-09-26','2026-09-26 10:33:44');
/*!40000 ALTER TABLE `body_metrics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diet_record`
--

DROP TABLE IF EXISTS `diet_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `diet_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `meal_type` varchar(20) NOT NULL,
  `food_name` varchar(100) NOT NULL,
  `calories` decimal(6,1) NOT NULL,
  `protein` decimal(5,1) DEFAULT 0.0,
  `carbs` decimal(5,1) DEFAULT 0.0,
  `fat` decimal(5,1) DEFAULT 0.0,
  `diet_date` date NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `diet_record_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diet_record`
--

LOCK TABLES `diet_record` WRITE;
/*!40000 ALTER TABLE `diet_record` DISABLE KEYS */;
INSERT INTO `diet_record` VALUES
(1,2,'早餐','全麦吐司2片 + 煮鸡蛋2个 + 美式黑咖啡',380.0,18.0,42.0,8.0,'2026-09-26','2026-09-26 01:36:35'),
(2,2,'午餐','香煎鸡胸肉150g + 紫米杂粮饭 + 清炒西兰花',640.0,46.0,65.0,12.0,'2026-09-26','2026-09-26 01:36:35');
/*!40000 ALTER TABLE `diet_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercise_plan`
--

DROP TABLE IF EXISTS `exercise_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `exercise_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `plan_type` varchar(50) NOT NULL,
  `target_val` decimal(6,1) NOT NULL,
  `current_val` decimal(6,1) DEFAULT 0.0,
  `unit` varchar(20) NOT NULL,
  `end_date` date DEFAULT NULL,
  `status` varchar(20) DEFAULT '进行中',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `exercise_plan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise_plan`
--

LOCK TABLES `exercise_plan` WRITE;
/*!40000 ALTER TABLE `exercise_plan` DISABLE KEYS */;
INSERT INTO `exercise_plan` VALUES
(1,2,'本月户外累计跑量','跑步',50.0,35.2,'公里','2026-10-11','进行中','2026-09-26 01:36:35'),
(2,2,'阶段减脂达标目标','减脂',65.0,68.5,'公斤','2026-10-26','进行中','2026-09-26 01:36:35'),
(3,2,'每周抗阻训练打卡','打卡',12.0,8.0,'次','2026-10-06','进行中','2026-09-26 01:36:35');
/*!40000 ALTER TABLE `exercise_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sport_dict`
--

DROP TABLE IF EXISTS `sport_dict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sport_dict` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `cal_per_min` decimal(4,1) NOT NULL,
  `category` varchar(30) DEFAULT '有氧运动',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sport_dict`
--

LOCK TABLES `sport_dict` WRITE;
/*!40000 ALTER TABLE `sport_dict` DISABLE KEYS */;
INSERT INTO `sport_dict` VALUES
(1,'户外慢跑',10.0,'有氧运动'),
(2,'动感单车',8.5,'有氧运动'),
(3,'力量训练',6.0,'抗阻无氧'),
(4,'自由泳',9.5,'有氧运动'),
(5,'高强度跳绳',11.5,'心肺HIIT'),
(6,'羽毛球',7.0,'球类竞技'),
(7,'瑜伽拉伸',4.0,'柔韧拉伸');
/*!40000 ALTER TABLE `sport_dict` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(100) NOT NULL,
  `real_name` varchar(50) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'USER',
  `gender` varchar(10) DEFAULT '男',
  `age` int(11) DEFAULT 24,
  `height` decimal(5,2) DEFAULT 175.00,
  `weight` decimal(5,2) DEFAULT 68.50,
  `target_weight` decimal(5,2) DEFAULT 65.00,
  `phone` varchar(20) DEFAULT NULL,
  `status` int(11) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES
(1,'admin','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','平台系统管理员','ADMIN','男',30,178.00,72.00,70.00,'13800000000',1,'2026-09-26 01:36:35','2026-09-26 01:36:35'),
(2,'user_alex','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','张健 (健身学员)','USER','男',24,175.00,68.50,65.00,'13911112222',1,'2026-09-26 01:36:35','2026-09-26 01:36:35'),
(3,'user_lisa','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','李悦 (减脂打卡)','USER','女',22,175.00,68.50,50.00,'13922223333',1,'2026-09-26 01:36:35','2026-09-26 10:32:57'),
(4,'','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','','USER','男',24,175.00,67.00,65.00,'',1,'2026-09-26 01:54:26','2026-09-26 01:54:26'),
(5,'没鸟','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','11','USER','男',24,175.00,68.00,65.00,'',1,'2026-09-26 10:33:44','2026-09-26 10:33:44');
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_notice`
--

DROP TABLE IF EXISTS `system_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `author` varchar(50) DEFAULT '系统管理员',
  `tag` varchar(20) DEFAULT '健康科普',
  `status` int(11) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_notice`
--

LOCK TABLES `system_notice` WRITE;
/*!40000 ALTER TABLE `system_notice` DISABLE KEYS */;
INSERT INTO `system_notice` VALUES
(1,'【健康科普】春夏季科学运动与水分电解质补充指南','运动前后需注意规律补水，每次训练建议间隔15-20分钟少量慢饮。剧烈运动超过45分钟推荐补充含电解质饮品。','系统管理员','健康科普',1,'2026-09-26 01:36:35'),
(2,'【平台公告】个人健康运动管理平台 2.0 正式上线','欢迎使用本平台！平台现已支持身体指标跟踪、运动打卡、饮食热量平衡与健身目标管理。如遇问题请联系管理员。','系统管理员','平台通知',1,'2026-09-26 01:36:35'),
(3,'【运动指南】科学减脂：关于热量赤字与蛋白质配比的解析','减脂的核心在于建立适度的热量赤字（300-500 kcal/天），同时保证每公斤体重1.6~2.0克优质蛋白质摄入，防止肌肉流失。','系统管理员','运动指南',1,'2026-09-26 01:36:35');
/*!40000 ALTER TABLE `system_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workout_record`
--

DROP TABLE IF EXISTS `workout_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `workout_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `sport_name` varchar(50) NOT NULL,
  `duration_min` int(11) NOT NULL,
  `calories_burned` decimal(6,1) NOT NULL,
  `distance_km` decimal(6,2) DEFAULT 0.00,
  `heart_rate` int(11) DEFAULT 0,
  `notes` varchar(255) DEFAULT NULL,
  `workout_date` date NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `workout_record_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout_record`
--

LOCK TABLES `workout_record` WRITE;
/*!40000 ALTER TABLE `workout_record` DISABLE KEYS */;
INSERT INTO `workout_record` VALUES
(1,2,'户外慢跑',35,360.0,5.20,142,'晨跑 5.2公里，配速稳定在 6分40秒','2026-09-26','2026-09-26 01:36:35'),
(2,2,'力量训练',45,230.0,0.00,128,'胸肌哑铃推举与器械夹胸','2026-09-25','2026-09-26 01:36:35'),
(3,2,'动感单车',40,320.0,14.50,150,'健身房单车晚课，跟骑节奏顺畅','2026-09-24','2026-09-26 01:36:35'),
(4,2,'自由泳',40,390.0,1.20,135,'室内恒温泳池自由泳 1200米','2026-09-23','2026-09-26 01:36:35'),
(5,2,'高强度跳绳',25,280.0,0.00,155,'间歇跳绳累计 2500 次','2026-09-22','2026-09-26 01:36:35'),
(6,2,'羽毛球',60,420.0,0.00,138,'与球友单打三局，心肺挑战极大','2026-09-21','2026-09-26 01:36:35'),
(7,3,'户外慢跑',30,300.0,4.50,140,'','2026-09-26','2026-09-26 10:32:52');
/*!40000 ALTER TABLE `workout_record` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-29 12:59:24
