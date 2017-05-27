folderName=$1
ssh -i /Users/build_leiting/jenkinsApp -p 32200 jenkinsApp@192.168.131.107 "mkdir -m 777 /var/www/LX6/$folderName"
