# Implementasi Aplikasi Wordpress MySQL Cluster dan Redis Cluster NoSQL ( Untuk Sistem Cache )
# 1. Model Arsitektur 
Berikut ini desain arsitektur yang saya gunakan pada MySQL Cluster dan Redis Cluster NoSQL.
Terdapat 4 node beserta keterangan tiap informasinya.

| No | IP Address | Hostname | Deskripsi |
| --- | --- | --- | --- |
| 1 | 192.168.33.10 | manager | Sebagai Node Manager dan Redis Master |
| 2 | 192.168.33.11| clusterdb1 | Sebagai Server 1 dan Node 1 dan Redis Slave 1 |
| 3 | 192.168.33.12 | clusterdb2 | Sebagai Server 2 dan Node 2 dan Redis Slave 2 |
| 4 | 192.168.33.13 | proxy | Sebagai Load Balancer (ProxySQL)|

#### 2. Untuk Evaluasi Tugas Akhir ini saya memanfaatkan aplikasi WordPress yang telah di kerjakan sebelumnya pada Evaluasi Tengah Semester, dan menambahkan Sistem Cache Redis Cluster NoSQL. Untuk tahap-tahap melakukan install MySQL dapat di lihat di [Tugas 1 Implementasi MySQL Cluster](https://github.com/daratursina/BDT/tree/master/TUGAS%201). 

#### 3. Tahap selanjutnya untuk menginstall WordPress dapat di lihat pada [ETS WordPress](https://github.com/daratursina/BDT/blob/master/ETS/README.md)

#### 4. Untuk tahap install redis dapat di lihat pada [Implementasi Redis](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/README.md)


##### Terlebih dahulu mengaktifkan Redis Cache, pada gambar dibawah ini Redis Cache sudah diaktifkan
![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/tidakatif.PNG)

##### Pastikan kembali telah melakukan konfigurasi dengan benar, maka akan muncul seperti di bawah ini : 

![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/redisdiwordpress.PNG)


##### 3. Terakhir untuk mengecek apakah Redis berjalan dengan baik pada WordPress yaitu :
## Test Failover Redis
`````
redis-cli monitor
OK -> jika berhasil 
`````
![SS](https://github.com/daratursina/BDT/blob/master/EAS%20BDT/SS/monitor.PNG)

### 5. Referensi : 
#### https://websiteforstudents.com/setup-wordpress-to-use-redis-caching-on-ubuntu-17-04-17-10/
#### https://geekflare.com/digitalocean-wordpress/
#### https://www.techandme.se/install-redis-cache-on-your-wordpress/
#### https://www.digitalocean.com/community/tutorials/how-to-configure-secure-updates-and-installations-in-wordpress-on-ubuntu
#### https://www.digitalocean.com/community/tutorials/how-to-configure-redis-caching-to-speed-up-wordpress-on-ubuntu-14-04




