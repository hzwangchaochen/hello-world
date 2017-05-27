today=`date "+%Y-%m-%d-%H-%M-%S"`
echo $today
mkdir /Users/build_leiting/temp_wcc/$today
cd /Users/build_leiting/LX6/trunk/Client/Assets/Res 
svn revert -R /Users/build_leiting/LX6/trunk/Client/Assets/Res
svn st | awk '{print $2}'|xargs -J {} mv {} /Users/build_leiting/temp_wcc/$today
#svn st | awk '{print $2}'|xargs svn delete --force
svn up
