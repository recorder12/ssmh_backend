json_file=$1    # full path of data json file
flask_ip_port=$2    # http://056c-64-98-208-143.ngrok.io
curl -X POST -H "Content-Type: application/json" -d @${json_file} ${flask_ip_port}/search
