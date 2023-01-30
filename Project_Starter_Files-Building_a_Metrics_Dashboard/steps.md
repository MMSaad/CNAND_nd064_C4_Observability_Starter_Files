# Projects Steps

## 1. Up-and-running with vagrant
1. Rename Vagrantfile.sample to Vagrantfile
2. bring up Vagrant machine
```bash
vagrant up
```

## 2. Execute host script
```bash
sh install/host-install.sh
```

## 3. Execute guest script
```bash
vagrant ssh
chmod 700 guest-install.sh
./guest-install.sh
```
