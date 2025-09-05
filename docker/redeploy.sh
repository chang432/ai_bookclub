rm -f /opt/redeploy.sh

cd /opt

mv docker/redeploy.sh ./redeploy.sh

chmod +x ./redeploy.sh

rm -rf /opt/docker

git clone https://github.com/chang432/ai_bookclub.git

mv ai_bookclub/docker ./

rm -rf ai_bookclub

cd docker

chmod +x start_cloud.sh

chmod +x start_cloud_helper.sh

bash start_cloud.sh