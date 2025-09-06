# Deploys webapp assets into external volume of specified instance to be served to users. 

REMOTE_ENDPOINT="178.156.178.248"

PARTITION_PATH="/mnt/HC_Volume_103317681"

cd frontend

npm run build

find ./dist -type f -name "*.js" -exec sed -i '' "s/localhost/${REMOTE_ENDPOINT}/g" {} +

ssh root@"$REMOTE_ENDPOINT" "rm -rf ${PARTITION_PATH}/webapp"

scp -r dist/* root@"$REMOTE_ENDPOINT":"${PARTITION_PATH}/webapp"

find ./dist -type f -name "*.js" -exec sed -i '' "s/${REMOTE_ENDPOINT}/localhost/g" {} +