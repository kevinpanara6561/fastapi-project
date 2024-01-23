super_user = {
    "name": "Super Admin",
    "email": "kevin.panara@aeonx.digital",
    "password": "1234567890",
}

operations = [
    {
        "name": "Roles",
        "index": "0",
        "sub_operations": [
            {
                "name": "List",
                "slug": "List Roles",
                "index": "0",
            },
            {
                "name": "Add",
                "slug": "Add Role",
                "index": "1",
            },
            {
                "name": "Edit",
                "slug": "Edit Role",
                "index": "2",
            },
            {
                "name": "Delete",
                "slug": "Delete Role",
                "index": "3",
            },
        ],
    },
    {
        "name": "Admin Users",
        "index": "1",
        "sub_operations": [
            {
                "name": "List",
                "slug": "List Admin Users",
                "index": "0",
            },
            {
                "name": "Add",
                "slug": "Add Admin User",
                "index": "1",
            },
            {
                "name": "Edit",
                "slug": "Edit Admin User",
                "index": "2",
            },
            {
                "name": "Delete",
                "slug": "Delete Admin User",
                "index": "3",
            },
            {
                "name": "Reset Password",
                "slug": "Reset Password",
                "index": "4",
            },
        ],
    },
]
