# Deploy a cloud function for log management:

## Use the below command to add the function to google cloud
```
gcloud functions deploy log_manager --runtime python37 --trigger-resource <YOUR_TRIGGER_BUCKET_NAME> --trigger-event google.storage.object.finalize --region asia-east2
```
