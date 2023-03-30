# Front End Branch  

## Environment:
1. Manually create venv with requirements.txt. Activate the virtual environment
```
cd /home/ubuntu/MathSearch/front-end
source venv/bin/activate
```

## Current public IP
time: 5/29 3:12PM  
`http://54.209.133.135`

## Useful commands to deploy flask  
### 1. enable gunicorn service
```
sudo systemctl daemon-reload
sudo systemctl start MathSearch
sudo systemctl enable MathSearch
```

### 2. start the Nginx service  
Can go to the Public IP address of EC2 on the browser to see the default nginx landing page
```
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Other commands
### 1. start gunicorn - deployment to public
```
sudo systemctl start MathSearch
```

### 2. stop gunicorn - deployment to public
```
sudo systemctl stop MathSearch
```

### 3.  check if frontend work on local  

Option 1:
visit `127.0.0.1:5000/test`

Option 2:  
```
curl localhost:5000/test
```

Option 3:
```
gunicorn -b 127.0.0.1:5000 api:app
```
if get [ERROR] Connection in use: ('127.0.0.1', 5000), you need to stop public deployment to deploy to local, do sudo `systemctl stop MathSearch`

### 4. check gunicorn status - deployment to public
```
sudo systemctl status MathSearch
```

### 5. check nginx.conf syntax
```
sudo nginx -t
```

### 6. reload config
```
sudo service nginx restart
```


Reference:
- https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7 (https://www.youtube.com/watch?v=z5XiVh6v4uI)
- https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project
- https://medium.com/@shefaliaj7/hosting-react-fl:ask-mongodb-web-application-on-aws-part-4-hosting-web-application-b8e205c19e4


### Location of service files:
1. `/etc/systemd/system/MathSearch.service`
2. `/etc/nginx/sites-available/MathSearch.nginx`