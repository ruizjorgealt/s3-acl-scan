import boto3
import logging
import csv

# -- Login Info -- #
LOG_FILENAME = 'scan.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)

def main():

    # -- CSV Object Instantiation (OOP) and Preparation -- #
    csv_dir = 'object_permissions.csv'
    csv = open(csv_dir, "w")
    columnTitleRow = "accountID, region, bucket, object, uri, permissions, storageClass\n"
    csv.write(columnTitleRow)

    # -- AWS Profiles -- #
    profile = ["profile1"]
    for p in profile:
        session=boto3.session.Session(profile_name=p)
        
    # -- Call Scanner Function -- #
    scanner(session, csv)

def write2csv(csv,a_acctid,a_region,a_bucket,a_object,a_uri,a_permission,a_strclass):
    row = a_acctid + ',' + a_region + ',' + a_bucket + ',' + a_object + ',' + a_uri + ',' + a_permission + ',' + a_strclass + '\n'
    csv.write(row)
    logging.info(a_object + " - WRITTEN TO CSV")

def scanner(session, csv):
    # -- S3 Object Instantiation (OOP) -- #
    s3 = session.client('s3')
    sts = session.client("sts")
    tmp_acctID = sts.get_caller_identity().get('Account')

    #----------------#
    # Get S3 Buckets #
    #----------------#

    # Get list of all buckets
    all_buckets=s3.list_buckets()

    # For every bucket in your bucket list
    for bucket in all_buckets['Buckets']:
        # -- Get Individual Bucket Name -- #
        tmp_bucket = bucket['Name']

        # -- Get Bucket Region -- #
        region = s3.get_bucket_location(
            Bucket=tmp_bucket
        )
        tmp_region = region['LocationConstraint']

        #---------------------------------#
        # Paginator for 1,000 Reply Limit #
        #---------------------------------#
        paginator = s3.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=tmp_bucket)

        #-----------------------------#
        # Check Objects in S3 Buckets #
        #-----------------------------#
        
        # # Get all objects in a bucket
        # all_objects = s3.list_objects_v2(
        #     Bucket=bucket['Name']
        # )

        # For every objects in a bucket
        try:
            for page_object in page_iterator:
                for pged_object in page_object['Contents']:

                    # -- Get object name and storage class -- #
                    tmp_object = pged_object['Key']
                    tmp_strclass = pged_object['StorageClass']
                    # a_obj = a_obj.encode('ascii', 'ignore').decode('ascii')

                    # Get ACL of individual objects
                    object_acl = s3.get_object_acl(
                        Bucket=tmp_bucket,
                        Key=tmp_object,
                    )

                    #-----------------------------#
                    # Write Public Objects to CVS #
                    #-----------------------------#

                    # For every granted permission in the ACL
                    for acl in object_acl['Grants']:
                        try:
                            if acl['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                                a_uri = acl['Grantee']['URI']
                                a_permission = acl['Permission']
                                write2csv(csv,tmp_acctID,tmp_region,tmp_bucket,tmp_object,a_uri,a_permission,tmp_strclass)
                            elif acl['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
                                a_uri = acl['Grantee']['URI']
                                a_permission = acl['Permission']
                                write2csv(csv,tmp_acctID,tmp_region,tmp_bucket,tmp_object,a_uri,a_permission,tmp_strclass)
                            elif acl['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/s3/LogDelivery':
                                a_uri = acl['Grantee']['URI']
                                a_permission = acl['Permission']
                                write2csv(csv,tmp_acctID,tmp_region,tmp_bucket,tmp_object,a_uri,a_permission,tmp_strclass)
                        except:
                            # pass
                            logging.info(tmp_object + " - HAS A GRANTEE WITH NO URI ATTRIBUTE KEY!")
        except:
            # pass
            logging.info(tmp_bucket + " - IS EMPTY!")

if __name__=='__main__':
    main()