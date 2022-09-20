        #Gets the instance state and checks to ensure it's

         resp = ec2.describe_instance_status(
            InstanceIds=[str(instance_id)],
            IncludeAllInstances=True)

         #print("Response = ",resp)

         instance_status = resp['InstanceStatuses'][0]['InstanceState']['Code']

         #print("Instance status =", instance_status)

         if instance_status == 80:
            #Try a dry run first to test permissions
            try:
                 ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
            except ClientError as e:
                 if 'DryRunOperation' not in str(e):
                     raise

            # Dry run succeeded, run start_instances without dryrun
            try:
                 response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
                 print(response)
            except ClientError as e:
                 print(e)