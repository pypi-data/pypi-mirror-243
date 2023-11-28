# msgraph-py

## Description

Python package with functions for easily interacting with the most common endpoints in Microsoft Graph API.
Authentication and token refresh is done in the background after environment variables are set.

Latest published version of this package can be found at [pypi.org/project/msgraph-py](https://pypi.org/project/msgraph-py/)

### List of available functions

#### `msgraph.identity`
- `get_user()`
- `get_user_risk()`
- `revoke_refresh_tokens()`
- `list_auth_methods()`
- `delete_auth_method()`
- `reset_strong_auth()`

#### `msgraph.groups`
- `get_group()`
- `list_group_members()`
- `add_group_member()`
- `remove_group_member()`

#### `msgraph.devices`
- `get_device()`
- `delete_device()`

#### `msgraph.mail`
- `send_mail()`

## Getting Started

1. Create an app registration in Azure AD with the necessary Graph application permissions for the functions you intend to use:  
[Authentication and authorization steps](https://learn.microsoft.com/en-us/graph/auth-v2-service?tabs=http#authentication-and-authorization-steps)

2. Install the package:  
`$ python3 -m pip install msgraph-py`

3. Configure environment variables:
    * If used within a Django project, `msgraph-py` will by default first attempt to load the following variables from the project's `settings.py`:

        ```python
        # project/settings.py

        AAD_TENANT_ID = ""
        AAD_CLIENT_ID = ""
        AAD_CLIENT_SECRET = ""
        ```

    * Alternatively you will need to set the following key-value pairs in `os.environ`:

        ```python
        import os

        os.environ["AAD_TENANT_ID"] = ""
        os.environ["AAD_CLIENT_ID"] = ""
        os.environ["AAD_CLIENT_SECRET"] = ""
        ```

> **Warning &#9888;&#65039;**  
> You should **never** store sensitive credentials or secrets in production code or commit them to your repository. Always load them at runtime from a secure location or from a local file excluded from the repository.

## Examples

### Get a single user by objectId or userPrincipalName
```python
from msgraph import get_user

user = get_user("user@example.com")
```

### Get a list of users using advanced query parameters

```python
from msgraph import get_user

filtered_users = get_user(
    filter="startsWith(department, 'sales')",
    select=[
        "displayName",
        "department",
        "createdDateTime",
    ],
    orderby="createdDateTime desc",
    all=True,
)
```

### Send e-mail with attachments

```python
from msgraph import send_mail

send_mail(
    sender_id="noreply@example.com",
    recipients=[
        "john.doe@example.com",
        "jane.doe@example.com",
    ],
    subject="Mail from Graph API",
    body="<h1>Content of the mail body</h1>",
    is_html=True,
    priority="high",
    attachments=[
        "/path/to/file1.txt",
        "/path/to/file2.docx",
    ],
)
```

## References and documentation

- [Authentication and authorization basics](https://learn.microsoft.com/en-us/graph/auth/auth-concepts)
- [Use query parameters to customize responses](https://learn.microsoft.com/en-us/graph/query-parameters)
- [User resource type - Properties](https://learn.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties)
- [Azure AD authentication methods API overview](https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview)
