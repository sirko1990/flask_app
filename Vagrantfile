Vagrant.configure(2) do |config|

   config.vm.box = "ubuntu/trusty64"
   config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64/versions/14.04/providers/virtualbox.box"

   config.vm.network "private_network", ip: "192.168.50.4"
   config.vm.network "forwarded_port", guest: 80, host: 8899
   config.vm.network "forwarded_port", guest: 9988, host: 9988
   config.vm.synced_folder ".", "/vagrant", :mount_options => ["dmode=777","fmode=777"]

   config.vm.provider "virtualbox" do |vb|
    # vb.gui = true
     vb.memory = "2048"
   end

   config.vm.provision "shell" do |s|
      s.path = "provision/bootstrap.sh"
   end
end