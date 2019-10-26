# Deploy a cloud function for Downloading Logs from FTP:

## Use the below command to add the function to google cloud
```
gcloud functions deploy get_hltv_demos_from_ftp --runtime python37 --trigger-http --region asia-east2
```

## Add Passive connection support for GCE
- Create PassivePortRange

  ```
  sudo nano /etc/pure-ftpd/conf/PassivePortRange
  ```
  
- Add the following in the file and save it (Ctrl-X and then y and Enter)

  ```
  29799 29899
  ```
  
- Create MaxClientsNumber

  ```
  sudo nano /etc/pure-ftpd/conf/MaxClientsNumber
  ```
  
- Add the following in the file and save it (Ctrl-X and then y and Enter)

  ```
  50
  ```
  
- Restart the FTP Server

  ```
  sudo service pure-ftpd restart
  ```
