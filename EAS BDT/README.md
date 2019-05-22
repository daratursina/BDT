# Implementasi Aplikasi Wordpress MySQL Cluster dan Redis Cluster NoSQL ( Untuk Sistem Cache )
# 1. Model Arsitektur 
Berikut ini desain arsitektur yang saya gunakan pada MySQL Cluster dan Redis Cluster NoSQL.
Terdapat 4 node beserta keterangan tiap informasinya.

| No | IP Address | Hostname | Deskripsi |
| --- | --- | --- | --- |
| 1 | 192.168.33.10 | manager | Sebagai Node Manager dan Redis Master |
| 2 | 192.168.33.11| clusterdb1 | Sebagai Server 1 dan Node 1 dan Redis clusterdb1 |
| 3 | 192.168.33.12 | clusterdb2 | Sebagai Server 2 dan Node 2 dan Redis clusterdb2 |
| 4 | 192.168.33.13 | proxy | Sebagai Load Balancer (ProxySQL)|

#### 2. Untuk Evaluasi Tugas Akhir ini saya memanfaatkan aplikasi WordPress yang telah di kerjakan sebelumnya pada Evaluasi Tengah Semester, dan menambahkan Sistem Cache Redis Cluster NoSQL. Untuk tahap-tahap melakukan install MySQL dapat di lihat di [Tugas 1 Implementasi MySQL Cluster](https://github.com/daratursina/BDT/tree/master/TUGAS%201). 

#### 3. Tahap selanjutnya untuk menginstall WordPress dapat di lihat pada [ETS WordPress](https://github.com/daratursina/BDT/blob/master/ETS/README.md)

#### 4. Untuk tahap install redis dapat di lihat pada [Implementasi Redis](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/README.md)


##### 5. Konfigurasi Redis Cache pada Wordpress
##### 5.1. Install Plugin `````Redis Object Cache`````

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/pasangsekarang.PNG)

##### Berikut ini tampilan sistem Cache pada WordPress sebelum dilakukan konfigurasi

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/Capture.PNG)

##### 5.2 Melakukan konfigurasi pada `````wp.config-php`````
`````
sudo nano wp.wonfig-php
`````
Isi dari konfigurasi yaitu : 

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/u.PNG)

###### Dan berikut ini tampilan Sistem Cache pada WordPress setelah dilakukan konfigurasi

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/setelahconfigwp.PNG)

##### 3. Terakhir untuk mengecek apakah Redis berjalan dengan baik pada WordPress yaitu :
## Test Failover Redis
`````
redis-cli monitor
OK -> jika berhasil 
`````

##### Telah berhasil menjalankan redis

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/redisokee.PNG)

##### Ketika mengomentar salah satu post

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/baruu.PNG)

##### Ketika mengakses salah satu post
![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/update.PNG)

### 5. Referensi : 
#### https://websiteforstudents.com/setup-wordpress-to-use-redis-caching-on-ubuntu-17-04-17-10/
#### https://geekflare.com/digitalocean-wordpress/
#### https://www.techandme.se/install-redis-cache-on-your-wordpress/
#### https://www.digitalocean.com/community/tutorials/how-to-configure-secure-updates-and-installations-in-wordpress-on-ubuntu
#### https://www.digitalocean.com/community/tutorials/how-to-configure-redis-caching-to-speed-up-wordpress-on-ubuntu-14-04




