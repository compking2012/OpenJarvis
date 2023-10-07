# OpenJarvis
An open smart speech assistant just like the Jarvis in Iron Man

Dependencies:
pip install -r requirements.txt

Train model:
rasa train --domain skills
rasa train --domain skills --num-threads 12

Start action server:
rasa run actions --actions skills

Shell:
rasa shell
