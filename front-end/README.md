# Front End Branch  

## Environment:
1. Manually create venv with requirements.txt. Activate the virtual environment
```
source venv/bin/activate
```

## Useful commands to deploy flask  
1. enable gunicorn service
```
sudo systemctl daemon-reload
sudo systemctl start app
sudo systemctl enable app
```

2. start the Nginx service  
Can go to the Public IP address of EC2 on the browser to see the default nginx landing page
```
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Other commands
1. stop gunicorn (killp doesn't work)  
```
sudo systemctl stop app
```
2. check if app running
```
curl localhost:8000/render
```

Reference: https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7