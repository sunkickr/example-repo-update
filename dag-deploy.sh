# Set Deployment API key credentials as environment variables
export ASTRONOMER_KEY_ID="<your-api-key-id>"
export ASTRONOMER_KEY_SECRET="<your-api-key-secret>"

# Install the latest version of Astro CLI
curl -sSL install.astronomer.io | sudo bash -s

# Determine if only dags have changes 
OUTPUT=$(git diff main... --name-only)
DAGS_DEPLOY=FALSE
REGULAR_DEPLOY=FALSE
local IFS=$'\n'
local lines=($OUTPUT)
local i
for (( i=0; i<${#lines[@]}; i++ )) ; do
    if [[ "${lines[$i]}" == *"dags/"* ]]
    then
        DAGS_DEPLOY=TRUE
    else
        REGULAR_DEPLOY=TRUE
    fi
done

# If only DAGs changed do a DAG Deploy
if [ $DAGS_DEPLOY == TRUE && $REGULAR_DEPLOY == FALSE ]
then
    astro deploy --dags
fi

# If any other files changed do a Regular Deploy
if [ $REGULAR_DEPLOY == TRUE ]
then
    astro deploy
fi