## Implementasi Cassandra dengan menggunakan Single-Node
Node yang digunakan yaitu hanya satu 
![Hasil](TABEL.png)

#### Langkah awal membuat file Vagrantfile, dimana isi dari Vagrantfile sebagai berikut : 
`````
Vagrant.configure("2") do |config|
  config.vm.define "cassandra" do |cassandra|
    cassandra.vm.hostname = "cassandra"
    cassandra.vm.box = "ubuntu/xenial64"
    cassandra.vm.network "private_network", ip: "192.168.33.10"

      # Opsional. Edit sesuai dengan nama network adapter di komputer
      # node.vm.network "public_network", bridge: "Intel(R) Dual Band Wireless-AC 3165"
      
    cassandra.vm.provider "virtualbox" do |vb|
      vb.name = "cassandra"
      vb.gui = false
      vb.memory = "1024"
    end

    # cassandra.vm.provision "shell", path: "provision/bootstrap.sh", privileged: false
  end
end
`````
Setelah itu seperti biasa "Vagrant up" pada node yang telah dibuat (cassandra) dan melakukan "Vagrant ssh cassandra"
#### Kemudian Install Java Virtual Machine
Sebelum melakukan install java, diperlukan beberapa package agar dapat melakukan creating repository.
##### 1. install proprerties-common untuk dapat menambahkan add repository, dengan sintaks :
`````
# apt-get update digunakan untuk mengupdate package yang sudah ada
sudo apt-get update
# install lib for add apt 
sudo apt-get install software-properties-common
`````
##### 2. Menambahkan repository baru untuk java
`````
# add repository java
sudo add-apt-repository ppa:webupd8team/java
# apt-get update untuk repository java yang baru agar repository yang baru ikut terupdate
sudo apt-get update
`````
###### apt-get update dilakukan agara package yang sudah ada terupdate dengan baik, kemudian melakukan instalasi propeties common agar bisa melakukan add-repository.
Berikut hasil tampilan jika berhasil melakukan step yang diatas
