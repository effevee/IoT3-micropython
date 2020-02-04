# IoT3-micropython

steps to sync a new local machine from existing repo on github :
1) install git from https://git-scm.com
2) make directory for repository
3) change into directory
4) git init
5) git remote add origin https://github.com/effevee/IoT3-micropython
6) git remote -v
7) git pull origin master 

steps to upload changes from local machine to repo on github :
1) make your changes
2) git status
3) git add (filename) or git add .
4) git status
5) git commit -m "(commit message)"
6) git push origin master

steps to download changes from repo on github to local machine :
1) change into directory for repository
2) git pull origin master
