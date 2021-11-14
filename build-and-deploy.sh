#! /bin/bash

export PROJECT_ID=acm-hackathon-332023
export REGION=us-west1
export CONNECTION_NAME=acm-hackathon-332023:us-west2:clean-data

gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/updatedb \
  --project $PROJECT_ID

gcloud run deploy updatedb \
  --image gcr.io/$PROJECT_ID/updatedb \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNECTION_NAME \
  --project $PROJECT_ID