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
