projectName=$1
currentLocation=$2

emptyProjectLocation=$3
#emptyProjectLocation='/home/bill/MC-Projects/ProjectToCopyFrom'


cp -a $emptyProjectLocation $currentLocation/$projectName
