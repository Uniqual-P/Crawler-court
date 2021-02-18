/*
 Navicat Premium Data Transfer

 Source Server         : spiderpython_dev
 Source Server Type    : MySQL
 Source Server Version : 50633
 Source Host           : 106.75.65.54:7749
 Source Schema         : spiderpython_dev

 Target Server Type    : MySQL
 Target Server Version : 50633
 File Encoding         : 65001

 Date: 18/02/2021 22:57:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_sp_courtnotice
-- ----------------------------
DROP TABLE IF EXISTS `t_sp_courtnotice`;
CREATE TABLE `t_sp_courtnotice` (
  `id` bigint(64) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `court` varchar(200) DEFAULT NULL COMMENT '法院',
  `forum` varchar(200) DEFAULT NULL COMMENT '法庭',
  `open_date` varchar(50) DEFAULT NULL COMMENT '开庭日期',
  `open_date_ori` varchar(50) DEFAULT NULL COMMENT '开庭日期，未清洗',
  `case_code` varchar(100) DEFAULT NULL COMMENT '案号',
  `case_code_ori` varchar(100) DEFAULT NULL COMMENT '原始案号',
  `reason` varchar(500) DEFAULT NULL COMMENT '案由',
  `depart` varchar(200) DEFAULT NULL COMMENT '承办部门',
  `judge` varchar(100) DEFAULT NULL COMMENT '法官',
  `clerk` varchar(100) DEFAULT NULL COMMENT '书记员',
  `juryman` varchar(100) DEFAULT NULL COMMENT '陪审员',
  `trial_member` varchar(200) DEFAULT NULL COMMENT '审判成员',
  `is_open` varchar(50) DEFAULT NULL COMMENT '是否公开审理',
  `accuser` varchar(500) DEFAULT NULL COMMENT '原告',
  `defendant` varchar(500) DEFAULT NULL COMMENT '被告',
  `litigant` varchar(500) DEFAULT NULL COMMENT '当事人',
  `result` varchar(500) DEFAULT NULL COMMENT '宣判情况',
  `purpose` varchar(200) DEFAULT NULL COMMENT '法庭用途',
  `is_annul` varchar(50) DEFAULT NULL COMMENT '是否撤销',
  `content` text COMMENT '公告内容',
  `area_name` varchar(50) DEFAULT NULL COMMENT '区域名称',
  `area_code` varchar(50) DEFAULT NULL COMMENT '区域编码',
  `crawl_id` varchar(50) DEFAULT NULL COMMENT '爬网ID',
  `crawl_time` datetime DEFAULT NULL COMMENT '爬取时间',
  `url` varchar(1024) DEFAULT NULL COMMENT '来源url',
  `url_id` bigint(64) DEFAULT NULL COMMENT '100001为外部开庭公告文件导入',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `text` text COMMENT 'origin json text',
  `excel_name` varchar(100) DEFAULT NULL COMMENT 'excelname',
  `publish_date` varchar(50) DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_t_sp_courtnotice_crawl_id` (`crawl_id`),
  KEY `idx_sp_courtnotice_area_code` (`area_code`),
  KEY `idx_sp_courtnotice_crawl_time` (`crawl_time`) USING BTREE,
  KEY `idx_sp_courtnotice_open_date` (`open_date`) USING BTREE,
  KEY `idx_sp_courtnotice_url_id` (`url_id`) USING BTREE,
  KEY `idx_sp_courtnotice_case_code` (`case_code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=19818 DEFAULT CHARSET=utf8 COMMENT='开庭公告爬网表';

SET FOREIGN_KEY_CHECKS = 1;
