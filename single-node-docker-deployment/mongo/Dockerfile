FROM mongo

COPY run.sh /root
RUN mkdir -p /home/mongo/mongoLog
RUN chmod 0777 /root/run.sh
VOLUME /data/db
CMD cd /home/mongo/mongoLog && nohup mongod & \
    sleep 5 && \
    ./root/run.sh && sleep 100000


EXPOSE 27017


  mongo:
    image: mongo:5.0.2
    restart: always
    environment:
      - MONGO_INITDB_ROOT_USERNAME=fedn_admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    ports:
      - 6534:6534
    command: mongod --port 6534

  mongo-express:
    image: mongo-express:latest
    restart: always
    depends_on:
      - "mongo"
    environment:
      - ME_CONFIG_MONGODB_SERVER=mongo
      - ME_CONFIG_MONGODB_PORT=6534
      - ME_CONFIG_MONGODB_ADMINUSERNAME=fedn_admin
      - ME_CONFIG_MONGODB_ADMINPASSWORD=password
      - ME_CONFIG_BASICAUTH_USERNAME=fedn_admin
      - ME_CONFIG_BASICAUTH_PASSWORD=password
    ports:
      - 8081:8081