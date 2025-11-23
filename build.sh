docker stop myfriend-api && docker rm myfriend-api
docker rmi myfriend-api:1.0.3
docker build -t myfriend-api:1.0.3 .
docker run --restart=always -d --name myfriend-api --network=my_network -p 9801:9901 -v /data/logs/myfriend-api:/app/logs -e FLASK_ENV=mini -e SQLALCHEMY_DATABASE_URI='mysql+pymysql://myfriend:123456@ant-api.forwework.com:3306/sso' --add-host=ant-api.forwework.com:host-gateway myfriend-api:1.0.3
# ImportError: Error loading shared library libstdc++.so.6: No such file or directory (needed by /usr/lib/python3.6/site-packages/pandas/_libs/window/aggregations.cpython-36m-x86_64-linux-gnu.so)