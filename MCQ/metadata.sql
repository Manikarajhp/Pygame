create database MCQTEST; 
USE MCQTEST;
CREATE TABLE USERS (ID int8 primary KEY auto_increment, USER_NAME VARCHAR(30), USER_PASSWORD VARCHAR(10),USER_MAIL VARCHAR(30));
DESC USERS;
INSERT INTO USERS (USER_NAME,USER_PASSWORD,USER_MAIL) VALUES("MANIKARAJ","HELLO@123","mainkaraj333@gmail.com");
SELECT * FROM USERS;
TRUNCATE TABLE USERS;
DELETE FROM USERS WHERE ID = 1;

CREATE TABLE TESTS (ID VARCHAR(10) primary KEY, USER_ID int8 , TEST_TITLE VARCHAR(20), TEST_DESCRIPTION varchar(50), START_TIME VARCHAR(20), END_TIME VARCHAR(20));
DESC TESTS;
ALTER TABLE QUESTIONS DROP FOREIGN KEY USER_ID;
ALTER TABLE TESTS DROP COLUMN USER_ID;
INSERT INTO TESTS (ID,USER_ID) VALUES('ABCDEF',2);
DELETE FROM TESTS WHERE ID = 'JDNFWG';
SELECT * FROM TESTS;
DROP TABLE TESTS;
TRUNCATE TABLE TESTS;

CREATE TABLE QUESTIONS (ID int8 primary KEY auto_increment, TEST_ID VARCHAR(10), QUESTION VARCHAR(100), OPTION1 VARCHAR(10), OPTION2 VARCHAR(10), OPTION3 VARCHAR(10), OPTION4 VARCHAR(10), CORRECT VARCHAR(10), SCORE INT8, NEG_SCORE INT8);
DESC QUESTIONS;
SELECT * FROM QUESTIONS;
INSERT INTO QUESTIONS (QUESTION,OPTION1,OPTION2,OPTION3,OPTION4,CORRECT,SCORE,NEG_SCORE) VALUES("I HAVE 2 WHEELS?","CAR","BIKE","TRAIN","BUS","BIKE",1,-1);
DROP DATABASE mcqtest;
