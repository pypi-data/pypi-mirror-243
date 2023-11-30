/*
SHOWQUERY	= False
  -- Dave Skura, 2022
DB_TYPE		= MySQL
DB_USERNAME	= dave
DB_USERPWD  = 4165605869
DB_HOST		= localhost
DB_PORT		= 3306
DB_NAME		= atlas

ARGV1=blurky
ARGV2=bam
ARGV3=bluooey
*/

SELECT 'SCRIPT{ARGV1}' as ARGV1,
	'SCRIPT{ARGV2}' as ARGV2,
	'SCRIPT{ARGV3}' as ARGV3
;

DROP TABLE IF EXISTS test_table;

CREATE TABLE test_table (
name varchar(25),
age integer
);

INSERT INTO test_table (name,age) VALUES 
('dave',50),
('frank',75),
('Billyjoe',45);

SELECT *
FROM test_table ;

DELETE FROM test_table
WHERE name = 'dave';

DROP TABLE test_table;




