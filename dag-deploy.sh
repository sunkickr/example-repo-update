OUTPUT=$(git diff main... --name-only)

function get_dag_and_regular_deploy {
    DAGS_DEPLOY=FALSE
    REGULAR_DEPLOY=FALSE
    local IFS=$'\n'
    local lines=($1)
    local i
    for (( i=0; i<${#lines[@]}; i++ )) ; do
        if [[ "${lines[$i]}" == *"dags/"* ]]
        then
            DAGS_DEPLOY=TRUE
        else
            REGULAR_DEPLOY=TRUE
        fi
    done
}

get_dag_and_regular_deploy "$OUTPUT"

echo $DAGS_DEPLOY
echo $REGULAR_DEPLOY

