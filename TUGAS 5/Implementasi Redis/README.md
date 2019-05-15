# Implementasi Redis Cluster
## Pengertian Redis
### Redis ( Remote Dictionary Server)
Redis adalah proyek struktur data dalam memori yang menerapkan basis data nilai kunci terdistribusi di dalam memori dengan daya tahan opsional. Redis mendukung berbagai jenis struktur data abstrak, seperti string, daftar, peta, set, set diurutkan, HyperLogLogs, bitmap, stream, dan indeks spasial. Redis kini memberikan respons dalam waktu di bawah satu milidetik yang memungkinkan jutaan permintaan per detik untuk aplikasi real-time pada Permainan, Ad-Tech, Layanan Finansial, Layanan Kesehatan, dan IoT. Redis adalah pilihan populer untuk caching, manajemen sesi, permainan, papan peringkat, analisis real-time, geospasial, tumpangan berkendara, obrolan/perpesanan, streaming media, dan aplikasi pub/sub.

## 1.  Arsitektur 
Berikut pembagian arsitektur dan IP pada tiap-tiap cluster:

![SS](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/dara.PNG)

## 2. Instalasi
##### 2.1. Membuat file Vagrantfile, seperti dibawah ini:
`````
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.box = "bento/ubuntu-18.04"
    master.vm.network "private_network", ip: "192.168.33.10"

    # Opsional. Edit sesuai dengan nama network adapter di komputer
    # node.vm.network "public_network", bridge: "Intel(R) Dual Band Wireless-AC 3165"
      
    master.vm.provider "virtualbox" do |vb|
      vb.name = "master"
      vb.gui = false
      vb.memory = "2046"
    end

    # master.vm.provision "shell", path: "provision/bootstrap.sh", privileged: false
  end

  (1..2).each do |i|
    config.vm.define "slave#{i}" do |node|
      node.vm.hostname = "slave#{i}"
      node.vm.box = "bento/ubuntu-18.04"
      node.vm.network "private_network", ip: "192.168.33.1#{i}"

      # Opsional. Edit sesuai dengan nama network adapter di komputer
      # node.vm.network "public_network", bridge: "Intel(R) Dual Band Wireless-AC 3165"
      
      node.vm.provider "virtualbox" do |vb|
        vb.name = "slave#{i}"
        vb.gui = false
        vb.memory = "1024"
      end

      # node.vm.provision "shell", path: "provision/bootstrap.sh", privileged: false
    end
  end
end
`````
##### 2.2. Melakukan installasi package redis pada masing-masing node:
`````
sudo apt-get update 
sudo apt-get install build-essential tcl
sudo apt-get install libjemalloc-dev
`````
##### 2.3. Setelah itu melakukan install redis pada masing-masing node:
`````
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
make test
sudo make install
`````
##### 2.4. Melakukan Konfigurasi untuk firewall pada masing-masing node:
`````
sudo ufw allow 6379 #Port Redis
sudo ufw allow 26379 #Sentinel
sudo ufw allow from 192.168.33.10 #Master
sudo ufw allow from 192.168.33.11 #Slave1
sudo ufw allow from 192.168.33.12 #Slave2
`````
##### Setelah melakukan konfigurasi, terdapat file `````redis.conf````` dan `````sentinel.conf````` . Melakukan konfigurasi pada file tersebut di masing-masing node. Dan pastikan kembali tidak ada `````typo````` (kesalahan)

![SS](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/redis.png)
##### 2.5 Selanjutnya mengubah konfigurasi pada masing-masing node, yaitu pada file `````redis.conf````` : 
`````
# Untuk Master
protected-mode no
port 6379
dir .
logfile "/home/vagrant/redis-stable/redig.log" #output log
`````
`````
# Untuk Slave1 dan Slave2
protected-mode no
port 6379
dir .
slaveof 192.168.33.10 6379
logfile "/home/redis-stable/redig.log" #output log
`````
##### Pada slave1 dan slave2 di dalam file`````redis.conf````` terdapat `````slaveof 192.168.33.10 6379````` . Dimana IP tersebut menunjukkan IP master.

##### 2.6 Setelah mengubah file `````redis.conf````` , selanjutnya mengubah konfigurasi file `````sentinel.conf ````` pada masing-masing node: 
`````
protected-mode no
port 26379
logfile "/home/redis-stable/sentinel.log"
sentinel monitor mymaster 192.168.33.10 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
`````
##### Setelah selesai melakukan konfigurasi, selanjutnya menjalankan redis:
###### Sebelum menjalankan redis maka, harus menjalankan `````redis-server````` yang berada pada folder `````src`````, dengan cara :
`````
src/redis-server redis.conf &
src/redis-server sentinel.conf --sentinel &
`````
##### Melakukan status pengecekan redis:
`````
ps -ef | grep redis
``````
##### Hasil dari tampilan status pengecekan redis sebagai berikut:

![SS](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/master1.PNG)

![SS](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/slave1.PNG)

![SS](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/slave2.PNG)

##### Selanjutnya melakukan ping ke masing-masing node:
`````
redis-cli -h [ip address] ping #masukkan ip address masing-masing node
`````
##### Hasil dari tampilan bahwa tiap node berhasil melakukan ping:

![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/pongmaster.PNG)

![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/slave1pong.PNG)

![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/slave2pong.PNG)

##### Mengecek masing-masing node telah tereplikasi dengan baik:
`````
redis-cli
`````
###### Pada master
![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/replicationmaster.PNG)

###### Pada slave1
![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/replicationslave1.PNG)

###### Pada slave2
![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/replicationslave2.PNG)

## 3. Fail Over
##### Mematikan salah node dengan sintak sebagai berikut:
`````
redis-cli -p 6379 DEBUG sleep 30
`````
![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/matikanmaster.PNG)

###### Ketika salah satu node dimatikan, maka node slave akan menjadi master 

![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/slave1master.PNG)

![Hasil](https://github.com/daratursina/BDT/blob/master/TUGAS%205/Implementasi%20Redis/SS/slave2master.PNG)

##### Meskipun salah satu node dimatikan(pada kasus ini yang dimatikan adalah master), redis tetap berjalan dengan baik.

## Referensi
#### https://medium.com/@amila922/redis-sentinel-high-availability-everything-you-need-to-know-from-dev-to-prod-complete-guide-deb198e70ea6
#### https://stackoverflow.com/questions/42857551/could-not-connect-to-redis-at-127-0-0-16379-connection-refused-with-homebrew
#### https://www.concretepage.com/questions/598
