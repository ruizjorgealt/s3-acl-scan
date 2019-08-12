```
  ____        _     _ _         ___  _     _           _     ____                                  
 |  _ \ _   _| |__ | (_) ___   / _ \| |__ (_) ___  ___| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
 | |_) | | | | '_ \| | |/ __| | | | | '_ \| |/ _ \/ __| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 |  __/| |_| | |_) | | | (__  | |_| | |_) | |  __/ (__| |_   ___) | (_| (_| | | | | | | |  __/ |   
 |_|    \__,_|_.__/|_|_|\___|  \___/|_.__// |\___|\___|\__| |____/ \___\__,_|_| |_|_| |_|\___|_|   
                                        |__/                                                       
                                        
```

# s3-acl-scan
Python script that scans all of your S3 objects for public access. Public access are those objects who have been given 

## How to use
In order to properly run this script, ensure that you have setup your AWS programmatic access on your local system or ensure that you are running the script in an EC2 environment with the proper AMI role.

Then you can simply run the python in your CLI in the following manner:

` $ python3 s3-acl-scan.py `

### Compatibility
Python v3.6
Boto 3

### Backlog
- [ ] Scan objects in multiple AWS accounts
