1.
clone the file.

2. 
open the command line in the file and input:
python -m pip install --upgrade pip  

3.
then input:

pip install -t lib -r requirements.txt

4.
creat a project in google cloud 

5. 
create a bucket in your project,see:
https://cloud.google.com/storage/

6.
open storage.py and change '{Your bucket id}' into the ‘bucket id’ you create before.

7.
Get your google map api key, see:
https://cloud.google.com/maps-platform/

8.
open files /tempaletes/poly_map.html and action.html change {your key} into your google map key.

9.
Input gcloud app deploy in the commond line under the file which contains .yaml

10.
open the application web.