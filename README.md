# Appliance Monitoring

Team 19


### Commands to solve npm issue
Error: ReferenceError: TextEncoder is not defined

```
sudo chmod 666 /dev/ttyUSB0  
sudo npm cache clean -f
sudo npm install -g n
sudo npm install -g n --force
sudo -E env "PATH=$PATH" n stable
sudo n stable
```