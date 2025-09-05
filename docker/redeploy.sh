cd /opt

rm -rf /opt/docker

git clone https://github.com/chang432/ai_bookclub.git

mv ai_bookclub/docker ./

rm -rf ai_bookclub

chmod +x docker/start_cloud.sh

chmod +x docker/start_cloud_helper.sh

bash docker/start_cloud.sh