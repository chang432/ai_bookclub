rm -rf /opt/docker

cd /opt

git clone https://github.com/chang432/ai_bookclub.git

mv ai_bookclub/docker ./

rm -rf ai_bookclub

cd docker

chmod +x start_cloud.sh

chmod +x start_cloud_helper.sh

bash start_cloud.sh