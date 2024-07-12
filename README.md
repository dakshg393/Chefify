<<<<<<< HEAD
in env file the secreate key 
in
=======
In .env file i add secrate key


when i deploy this web app on aws i make .env and assign secrete key for setting (Remember this )

"to activate vrtual env go to Recipe-Management-system and cd source myenv/bin/activate"

"for aws deploy  git bash cmd for  login and connect"
ssh -i your-key.pem ubuntu@your-aws-instance-ip


"gunicorn is used when the port is runing on and by any chance it will stop and exit and gunicorn again run it (means gunicorn autometicaly pass cmd python manage.py runserver when it stops) TO activate ganicoern we use this cmd "
sudo nano /etc/systemd/system/gunicorn.socket