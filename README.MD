第一步：
下载文件


在文件夹输入
pip install -t lib -r requirements.txt


创建project 在google cloud 


创建一个bucket https://cloud.google.com/storage/

打开 storage.py 将'{Your bucket id}' 换成你的bucket id


创建google地图key https://cloud.google.com/maps-platform/
打开 tempaletes/poly_map.html 和 action.html 将 {your key} 换成你自己的key 



打开 commond line  输入 gcloud app deploy （有yaml 的目录下）