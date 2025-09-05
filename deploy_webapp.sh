PARTITION_PATH="/mnt/HC_Volume_103317681"

cd frontend

npm run build

ssh root@178.156.178.248 "rm -rf ${PARTITION_PATH}/webapp"

scp -r dist/* root@178.156.178.248:/mnt/HC_Volume_103317681/webapp