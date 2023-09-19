Run front-end
Open the terminal and go to the folder ./frontend,

install package
sudo apt update
install Node.js and npm:
sudo apt install nodejs
sudo apt install npm
you can check if it’s success by 
npm -v 
npm install

run code
npm run dev:ssr
then the frontend can be run at ‘http://localhost:8887’

Run back-end
Open the terminal and under the project root directory,
install modules
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt-get install libmysqlclient-dev
pip3 install mysql-connector-python flask Flask-MySQLdb Flask-CORS requests openai 

run code
python3 app.py