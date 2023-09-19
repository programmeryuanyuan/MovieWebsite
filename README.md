# Installation and Prerequisites

> TESTED ON UBUNTU 20.04 LTS

I will assume that you are trying to run our program on a fresh Ubuntu operating system.
First download our package to your laptop.
Then unzip the package named gogogo.zip
(if not, you can rename it )
```
unzip filename.zip
```
then go into the folder
```
cd filename
```
## Run back-end
Open the terminal and under the project root directory,
### install modules
```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt-get install libmysqlclient-dev
pip3 install mysql-connector-python flask Flask-MySQLdb Flask-CORS requests openai
```
### run code
```
python3 app.py
```


## Run front-end
Open the terminal and go to the folder ./frontend,

### install package

```
sudo apt update
```
install Node.js and npm:
```
sudo apt install nodejs
sudo apt install npm
```
you can check if it’s success by
```
npm -v
```
then you can install the package *
```
npm install
```
run code
```
npm run dev:ssr
```
then the frontend can be run at ‘<http://localhost:8887>’

if not success, might because of the npm version error, run below command
```
sudo apt install curl
npm install serialize-javascript
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

close and reopen the terminal, run below command
```
nvm install 14.17.0
nvm use 14.17.0
```
then install the package(the step with *) and run the code
