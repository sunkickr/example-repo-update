# Create template of deployment to be copied with
astro deployment inspect $DEPLOYMENT_ID --template > deployment-template.yaml # autmatically creates deployment-template.yaml file

# Add name to deployment template file
sed -i "s|  name:.*|  name: $NEW_DEPLOYMENT_NAME|g" deployment-template.yaml

# Create new deploymeent preview based on the deployment template file
astro deployment create --deployment-file deployment-template.yaml

# Deploy new code to the deployment preview 
astro deploy -n $NEW_DEPLOYMENT_NAME