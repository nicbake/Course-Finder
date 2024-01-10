# UoG  McGill Course/Subject Finder and Graph Maker

A program to search and filter course offerings at the University of Guelph.
Graphs majors and programs for University of Guelph, and subjects for McGill.

## Getting Started

### Dependencies

* Node 14 or higher
* Python 3.9 or higher
    * sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

## Installation and setup of React and Flask

1. Navigate to the directory named `webapp`
2. Run `npm install` to install dependencies for the node program 
3. Run `npm run build` to create a build for the NGINX server to serve
4. Naviate to the directory named `flask-api`
5. Run `pip3 install -r requirements.txt` to install Python dependencies

## Installation and setup of NGINX and Flask

1. While in the repo directory, run the install script to install NGINX
2. Navigate to the etc folder - `cd /etc`
3. Obtain the hostname - `cat /hostname`
4. Open an editor to copy the hostname into /etc/hosts - `sudo nano hosts`
    - Important to use sudo in order to be able to write
5. Copy the ip address of the localhost and write your hostname alongside it
    - (e.g.) 127.0.0.1    localhost
             127.0.0.1    your_hostname
6. Navigate to the sites-available folder - `cd /etc/nginx/sites-available`
7. Create a file called flask-api - `sudo nano flask-api`
8. Copy the following into the file - 
```
server {
    server_name 131.104.49.106;
    root /home/sysadmin/sprint-1/webapp/build;
    index index.html;
   
    location / {
        try_files $uri /index.html;
    }

    location /api {
        include uwsgi_params;
        uwsgi_pass unix:/home/sysadmin/sprint-1/flask-api/flask-api.sock;
    }
}
```
9. Navigate to `/etc/systemd/system`
10. Create and open a file called flask-api.service - `sudo nano flask-api.service`
11. Copy the follwing into the file -
```
[Unit]
Description="uWSGI server instance for flask-api"
After=network.target

[Service]
User=sysadmin
Group=sysadmin
WorkingDirectory=/home/sysadmin/sprint-1/flask-api/
Environment=FLASK_ENV=test
ExecStart=/home/sysadmin/.local/bin/uwsgi --ini /home/sysadmin/sprint-1/flask-api/app.ini

[Install]
WantedBy=multi-user.target
```
11. Run `sudo ufw allow 'Nginx Full'`
12. Run `sudo systemctl nginx start` and `sudo systemctl flask-api start` to run the nginx server and Flask API.

## HTTPS/SSL setup
1. Create a configuration snippet file - `sudo nano /etc/nginx/snippets/self-signed.conf`
2. Add the following to the configuration file
```
ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
```
3. Create a second configuration snippet that points to the newly generated SSL key and certificate. - `sudo nano /etc/nginx/snippets/ssl-params.conf`
4. Add the following to the configuration file
```
ssl_protocols TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_dhparam /etc/ssl/certs/dhparam.pem;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
ssl_session_timeout 10m;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off; # Requires nginx >= 1.5.9
# ssl_stapling on; # Requires nginx >= 1.3.7
# ssl_stapling_verify on; # Requires nginx => 1.3.7
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```
5. Generate the dhparam.pem file. This command will take some time - `sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048`
6. Open the server block in sites-available - `sudo nano /etc/nginx/sites-available/flask-api`
7. Paste this into the file
```
server {
    listen 443 ssl;
    listen [::]:443 ssl;    

    include snippets/self-signed.conf;
    include snippets/ssl-params.conf;

    server_name 131.104.49.106;
    root /home/sysadmin/sprint-1/webapp/build;
    index index.html;
   
    location / {
        try_files $uri /index.html;
    }

    location /api {
        include uwsgi_params;
        uwsgi_pass unix:/home/sysadmin/sprint-1/flask-api/flask-api.sock;
    }

}

server {
    server_name 131.104.49.106;

    return 302 https://$server_name$request_uri;
}
```

## Authors

* Farid Hamid
* Harsh Topiwala
* Jainil Patel
* Lourenco Velez
* Nicholas Baker
