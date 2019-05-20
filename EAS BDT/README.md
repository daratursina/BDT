# Implementasi Aplikasi Wordpress MySQL Cluster dan Redis Cluster NoSQL ( Untuk Sistem Cache )
# 1. Model Arsitektur 
Berikut ini desain arsitektur yang saya gunakan pada MySQL Cluster dan Redis Cluster NoSQL.
Terdapat 4 node beserta keterangan tiap informasinya.

| No | IP Address | Hostname | Deskripsi |
| --- | --- | --- | --- |
| 1 | 192.168.33.11 | manager | Sebagai Node Manager dan Redis Master |
| 2 | 192.168.33.12 | clusterdb1 | Sebagai Server 1 dan Node 1 dan Redis Slave 1 |
| 3 | 192.168.33.13 | clusterdb2 | Sebagai Server 2 dan Node 2 |
| 4 | 192.168.33.14 | proxy | Sebagai Load Balancer (ProxySQL)|

#### 1. Untuk Evaluasi Tugas Akhir ini saya memanfaatkan aplikasi WordPress yang telah di kerjakan sebelumnya pada Evaluasi Tengah Semester, dan menambahkan Sistem Cache Redis Cluster NoSQL. Untuk tahap-tahap melakukan install MySQL dapat di lihat di [Tugas 1 Implementasi MySQL Cluster](https://github.com/daratursina/BDT/tree/master/TUGAS%201). 

#### 2. Tahap selanjutnya untuk menginstall WordPress dapat di lihat pada [ETS WordPress](https://github.com/daratursina/BDT/blob/master/ETS/README.md)

#### 3. Tahap berikutnya untuk menginstall Sistem Cache Redis pada WordPress
## STEP I
##### 1. Install package pada manager,clusterdb1, dan proxy
`````
sudo apt-get install software-properties-common 
`````

##### 2. Install Repository pada manager, clusterdb1, dan proxy
`````
sudo add-apt-repository ppa:chris-lea/redis-server
`````
##### 3. Install redis pada pada manager dan proxy
`````
sudo apt-get update
sudo apt-get install redis-server php-redis 
`````
Catatan : Disini pada clusterdb1 saya hanya menginstall `````sudo apt-get install php-redis`````
##### 4. Melakukan verifikasi redis pada manager dan proxy
`````
redis-server --version
`````
## STEP II
##### 1. Melakukan file konfigurasi pada manager dan proxy
`````
sudo nano /etc/redis/redis.conf
`````
##### 1.1 Pada isi file `````redis.conf````` melakukan uncomment pada `````maxmemmory````` dan `````eviction policy`````
pada manager dan proxy yaitu : 
`````maxmemory 256mb`````
`````maxmemory-policy allkeys-lfu`````

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/max.PNG)
![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/policy.PNG)

##### 2. Melakukan restart redis server pada manager dan proxy
`````
sudo systemctl restart redis-server
`````
## STEP III
##### 1. Menambahkan konfigurasi pada proxy terlebih dahulu masuk ke : 
`````
sudo nano /var/www/html/wp-config.php
`````
##### 2. Lalu menambahkan `````WordPress unique Keys dan Salts section`````:
`````
define( 'WP_CACHE_KEY_SALT', 'example.com' );  // tidak harus 'example.com'
define( 'WP_CACHE', true );
`````
Catatan : Setelah berhasil melakukan `````sudo systemctl restart redis-server`````.
Selanjutnya melakukan tes koneksi dengan sintak : 
`````
redis-cli
`````
Tes `````redis-cli````` pada manager
![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/max.PNG)

Tes `````redis-cli````` pada proxy
![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/max.PNG)

##### 3. Terakhir untuk mengecek apakah Redis berjalan dengan baik pada WordPress yaitu :
`````
redis-cli monitor
OK -> jika berhasil 
`````





