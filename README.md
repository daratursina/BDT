# BDT
# Implementasi Partisi
## Berikut ini tahap-tahap dalam melakukan Implementasi Partisi
1. Mengecek apakah plugin partition telah aktif 
Dengan menggunakan command "SHOW PLUGIN:"

`````
!<Hasil menunjukkan bahwa Partition telah aktif(SCREENSHOOT/Picture1)

`````

Setelah itu mengestrak database, database yang digunakan dari vertabelo (https://www.vertabelo.com/blog/technical-articles/everything-you-need-to-know-about-mysql-partitions)

2. Melakukan partititon yaitu dengan membuat tabel dan contoh insert data dan hasil querynya
3. Menambahkan insert pada tiap-tiap tabel yang akan di partisi dengan menggunakan Partition Type yaitu :                                         


a. Menambahkan Range Partition
  `````
  PARTITION BY RANGE COLUMNS (created){
         PARTITION oldlogs VALUES THAN (2015-01-01)
  PARTITION currentlogs VALUES LESS THAN (MAXVALUE)
  `````
  `````
  CREATE TABLE rc1 (
    a INT,
    b INT
)
PARTITION BY RANGE COLUMNS(a, b) (
    PARTITION p0 VALUES LESS THAN (5, 12),
    PARTITION p3 VALUES LESS THAN (MAXVALUE, MAXVALUE)
);
`````
b. Menambahkan List Partition
 `````
 CREATE TABLE serverlogs (
    serverid INT NOT NULL, 
    logdata BLOB NOT NULL,
    created DATETIME NOT NULL
)
PARTITION BY LIST (serverid)(
    PARTITION server_east VALUES IN(1,43,65,12,56,73),
    PARTITION server_west VALUES IN(534,6422,196,956,22)
);
`````
`````
CREATE TABLE serverlogs (
    servername VARCHAR(20) NOT NULL, 
    logdata BLOB NOT NULL,
    created DATETIME NOT NULL
)
PARTITION BY LIST COLUMNS (servername)(
    PARTITION server_east VALUES IN('northern_east','east_ny'),
    PARTITION server_west VALUES IN('west_city','southern_ca')
);
`````

c. Menambahkan Hash Partition
`````
CREATE TABLE serverlogs2 (
    serverid INT NOT NULL, 
    logdata BLOB NOT NULL,
    created DATETIME NOT NULL
)
PARTITION BY HASH (serverid)
PARTITIONS 10;
`````
`````
CREATE TABLE serverlogs2 (
    serverid INT NOT NULL, 
    logdata BLOB NOT NULL,
    created DATETIME NOT NULL
)
PARTITION BY LINEAR HASH (serverid)
PARTITIONS 10;
`````
d. Menambhakan Key Partition
`````
CREATE TABLE serverlogs4 (
    serverid INT NOT NULL, 
    logdata BLOB NOT NULL,
    created DATETIME NOT NULL,
    UNIQUE KEY (serverid)
)
PARTITION BY KEY()
PARTITIONS 10;
`````
`````
CREATE TABLE serverlogs6 (
    serverid INT NOT NULL, 
    logdata BLOB NOT NULL,
    created DATETIME NOT NULL
)
PARTITION BY LINEAR KEY(serverid)
PARTITIONS 10;
`````
4. Testing pada bagian "A Typical Use Case: Time Series Data"

    a. Menguji SELECT dengan menggunakan perintah EXPLAIN
`````
SELECT * FROM samplelogs WHERE created > '2016-01-01';
EXPLAIN test_measures
WHERE measure_timestamp >= '2016-01-01' AND DAYOFWEEK(measure_timestamp)
SELECT * FROM samplelogs PARTITION (currentlogs) WHERE created > '2016-01-01'

EXPLAIN SELECT *
FROM test_measures
WHERE measure_timestamp >= '2016-01-01 AND DAYOFWEEK(measure_timestamp)
`````


      b. Menguji Query Benchmark untuk masing-masing tabel


`````
ELECT SQL_NO_CACHE
    COUNT(*)
FROM
    vertabelo.measures
WHERE
    measure_timestamp >= '2016-01-01'
        AND DAYOFWEEK(measure_timestamp) = 1;
     
SELECT SQL_NO_CACHE
    COUNT(*)
FROM
    vertabelo.partitioned_measures
WHERE
    measure_timestamp >= '2016-01-01'
        AND DAYOFWEEK(measure_timestamp) = 1;
`````

````
ALTER TABLE `vertabelo`.`measures` 
DROP INDEX `measure_timestamp` ;
 
ALTER TABLE `vertabelo`.`partitioned_measures` 
DROP INDEX `measure_timestamp` ;
`````

  c. Menjalankan QUERY DELETE (bagian BIG DELETE)
  
`````
ALTER TABLE `vertabelo`.`measures` 
ADD INDEX `index1` (`measure_timestamp` ASC);
`````
`````
ALTER TABLE `vertabelo`.`partitioned_measures` 
ADD INDEX `index1` (`measure_timestamp` ASC);
`````
`````
DELETE
FROM vertabelo.measures
WHERE  measure_timestamp < '2015-01-01';
`````
`````
ALTER TABLE vertabelo.partitioned_measures 
DROP PARTITION to_delete_logs ;
`````
`````
DELETE
FROM vertabelo.measures
WHERE  measure_timestamp < '2016-01-01';
`````
`````
ALTER TABLE vertabelo.partitioned_measures DROP PARTITION prev_year_logs ;
`````
