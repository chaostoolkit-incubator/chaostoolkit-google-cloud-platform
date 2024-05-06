## The `chaosgcp.iam.controls.policy` control to Manage temporary, 
## time-bound IAM roles for the specified project and members.
The  ChaosGCP IAM Policy Control  allows you to manage temporary, 
time-bound IAM roles for a specified project and members. This control grants
specified IAM roles to the provided members, with an expiration time determined
by the given parameter. It can be used to grant and revoke IAM roles
to/from specified members before and after an experiment, respectively.
This control can be used to improve the security of Chaos Toolkit
experiments by ensuring that IAM roles are only granted for the
duration of the experiment.
The ChaosGCP IAM Policy Control is Python-based and designed 
to be used in conjunction with Chaos Toolkit experiments to
grant and revoke IAM roles .


### Prerequisites
* Before using the ChaosGCP IAM Policy Control, ensure the following:
1. Chaos Toolkit and ChaosGCP: Verify that both Chaos Toolkit and ChaosGCP 
are installed and configured correctly in your environment. 
These tools are essential for executing chaos experiments and managing 
IAM policies within your GCP projects.
2. Project Access: Ensure that you have the necessary access and permissions 
to the GCP project where you intend to apply the control. 
You should have the ability to create and modify IAM policies within the project. 
Refer : 
https://cloud.google.com/resource-manager/docs/access-control-proj#resourcemanager.projectIamAdmin
3. Caution in Production Environments: Exercise caution when using this 
control in production environments.
The control directly interacts with IAM policies, 
which can have significant implications for your project's security and access control.
Thoroughly test the control in a non-production environment before deploying it to production.
Note: The control uses policy version 3 due to the conditional nature of the expiry, 
which allows for more granular control over the expiration time of the granted IAM roles.

### Audit logs can be found in cloud logging for the mentioned project 
resource.type="project"
logName="projects/<yourprojectname>/logs/cloudaudit.googleapis.com%2Factivity"

### Handling IAM Propagation Delays
In some cases, even after setting the IAM propagation time to default 2
 minutes, the roles might not be propagated, potentially leading to 
 experiment failure based on the usage of those members. This could 
 indicate that propagation is not yet complete. To address this, the 
 user should consider increasing the propagation time to ensure that 
 the roles are fully propagated before proceeding with the experiment.


### Usage
To use the control, users must add it to their experiment definition in the "controls" section. The control accepts the following arguments:

* project_id: The ID of the project where the roles will be managed.
* roles: A list of IAM role names to grant/revoke.
* members: A list of members to grant/revoke roles to.
* iam_propogation_sleep_time_in_minutes: Optional (default: 2). 
The time to wait, in minutes, for IAM propagation to complete before the experiment starts.
* expiry_time_in_minutes: Optional (default: 10). 
The time, in minutes, after which the granted IAM roles expire. 
The roles will be revoked or expired when the experiment finishes
or when the expiry time is reached, whichever comes first. 
The iam_propogation_sleep_time_in_minutes is added to the expiry time 
to compensate for the propagation delay.


Define the control in your experiment json as below 
  ```json
    "controls": [
        {
            "name": "gcp-iampolicy-timebound",
            "provider": {
                "type": "python",
                "module": "chaosgcp.iam.controls.policy",
                "arguments": {
                    "project_id":"mysampleproject",
                    "roles": ["roles/storage.admin"],
                    "members": ["serviceAccount:dp-sa11@mysampleproject.iam.gserviceaccount.com"],
                    "expiry_time_in_minutes": 10
                }
            }
        }
    ]

