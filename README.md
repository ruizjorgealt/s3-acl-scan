```
  ____        _     _ _         ___  _     _           _     ____                                  
 |  _ \ _   _| |__ | (_) ___   / _ \| |__ (_) ___  ___| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
 | |_) | | | | '_ \| | |/ __| | | | | '_ \| |/ _ \/ __| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 |  __/| |_| | |_) | | | (__  | |_| | |_) | |  __/ (__| |_   ___) | (_| (_| | | | | | | |  __/ |   
 |_|    \__,_|_.__/|_|_|\___|  \___/|_.__// |\___|\___|\__| |____/ \___\__,_|_| |_|_| |_|\___|_|   
                                        |__/                                                       
                                        
```

# s3-acl-scan
Python script that scans all of your S3 objects for public access. Public objects are objects that are available to the **All Users group** represented by the uri http://acs.amazonaws.com/groups/global/AllUsers. The script will perform a complete scan of all your objects and identify which objects have the grantee of http://acs.amazonaws.com/groups/global/AllUsers with the following permissions:

- READ
- READ_ACP
- WRITE_ACP

## How To Use
In order to properly run this script, ensure that you have setup your AWS programmatic access on your local system or ensure that you are running the script in an EC2 environment with the proper AMI role.

First you have to provide the name of your aws profile as configured in **.aws/config** and **.aws/credentials**
```
def main():
    profile = ["myProfileName"]
    for i in range(0,len(profile)):
        session=boto3.session.Session(profile_name=profile.pop(i))
```
You scan multiple AWS accounts, simply extend the list and add additional profiles

```
def main():
    profile = ["myProfileName", "dev", "production"]
    for i in range(0,len(profile)):
        session=boto3.session.Session(profile_name=profile.pop(i))
```

Then simply run the python script in your terminal:

` $ python3 s3-acl-scan.py `

Once the script performs a complete scan of all of your objects, it will generate a CVS file with objects that are public and accessible to the internet.

![cvs with public objects](https://jorgearuiz.net/wp-content/uploads/2019/08/csv-py.png)

### Compatibility

-Python v3.6
-Boto 3

### Backlog
- [ ] Scan objects in multiple AWS accounts

#### References

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
