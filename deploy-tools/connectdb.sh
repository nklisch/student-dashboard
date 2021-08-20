if [[ -z $1 ]] || [[ -z $2 ]]; then
  echo "Usage:   # ${0} <cs-dept-username> <cs-dept-machine-name>"
  echo "Example: # ${0} nklisch olympia"
else
  ssh -4 -L 3306:faure.cs.colostate.edu:3306 ${1}@${2}.cs.colostate.edu
fi