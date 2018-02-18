projectName=$1
currentLocation=$2

emptyProjectLocation='/home/bill/MC-Projects/ProjectToCopyFrom'

cp -a $emptyProjectLocation $currentLocation/$projectName
