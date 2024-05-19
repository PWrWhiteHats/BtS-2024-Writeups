# generate a base64 encoded password for the apps
PWD="$(dd if=/dev/urandom bs=12 count=1 | base64)" 
FLAG=$(cat /flag)

echo "Password: $PWD"

PASSWORD=$PWD FLAG=$FLAG gunicorn -b 0.0.0.0:5000 --certfile=cert_forum.crt --keyfile=cert_forum.key --ca-certs=ca.crt -w 1 forum-app:app & 
PASSWORD=$PWD FLAG=$FLAG gunicorn -b 0.0.0.0:5001 --certfile=cert_image.crt --keyfile=cert_image.key --ca-certs=ca.crt -w 1 image-app:app &
socat TCP-LISTEN:8888,reuseaddr,fork EXEC:'python3 -m mitm'
