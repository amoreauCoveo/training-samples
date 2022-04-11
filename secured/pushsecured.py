from coveopush import CoveoPush
from coveopush import Document
from coveopush import CoveoPermissions
from coveopush import CoveoConstants
import json

# The settings of your source and organization
settings = {
    "sourceId": "your-source-id",
    "orgId": "your-org-id",
    "apiKey": "your-api-key"
}

# Define push so we know where to send
push = CoveoPush.Push(settings["sourceId"], settings["orgId"], settings["apiKey"])

securityProvider = 'Techzample Security'

cascading = {
    "Email Security Provider": {
        "name": "Email Security Provider",
        "type": "EMAIL"
    }
}

push.AddSecurityProvider(securityProvider, "EXPANDED", cascading)

with open('securedcontent.json', encoding='utf-8') as json_file:
    items = json.load(json_file)
    itemsToPush = []
    for item in items:
        doc = Document(item['documentId'])
        doc.Title = item['title']
        doc.SetData(item['data'])
        # Add Metadata
        doc.AddMetadata("contenttype", item['contenttype'])
        doc.AddMetadata("workemail", item['workemail'])
        doc.AddMetadata("fullname", item['fullname'])
        doc.AddMetadata("manager", item['manager'])
        doc.AddMetadata("worktitle", item['worktitle'])
        doc.AddMetadata("workdepartment", item['workdepartment'])
        doc.AddMetadata("workteam", item['workteam'])
        doc.AddMetadata("office", item['office'])
        doc.AddMetadata("reviewdate", item['date'])

        # Creating the permission set
        permissionSet = CoveoPermissions.DocumentPermissionSet('First')
        permissionSet.AllowAnonymous = False

        # Iterating through the permissions to add the right ones
        for email in item['permissions'][0]['allowedPermissions']:
            if (email['identityType'] == 'User'):
                permissionSet.AddAllowedPermissions(CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.User, securityProvider, email['identity']))
            if (email['identityType'] == 'Group'):
                permissionSet.AddAllowedPermissions(CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.Group, securityProvider, email['identity']))
        for email in item['permissions'][0]['deniedPermissions']:
            if (email['identityType'] == 'User'):
                permissionSet.AddDeniedPermissions(CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.User, securityProvider, email['identity']))
            if (email['identityType'] == 'Group'):
                permissionSet.AddDeniedPermissions(CoveoPermissions.PermissionIdentity(CoveoConstants.Constants.PermissionIdentityType.Group, securityProvider, email['identity']))
            
        doc.Permissions.append(permissionSet)

        itemsToPush.append(doc)

    # We want to update the status of the source when pushing date
    updateSourceStatus = True
    # We don't want to clear all documents from the source before pushing new data
    deleteOlder = False
    
    push.AddDocuments(itemsToPush, [], updateSourceStatus, deleteOlder)