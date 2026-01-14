APP_ACTIONS = [
    {
        "app_action_id" : 1,
        "name"          : "Export List", 
        "rank"          : 1,
    }, 
    {
        "app_action_id" : 2,
        "name"          : "Print List", 
        "rank"          : 2,
    }, 
    {
        "app_action_id" : 3,
        "name"          : "Index", 
        "rank"          : 3,
    }, 
    {
        "app_action_id" : 4,
        "name"          : "Add", 
        "rank"          : 4,
    }, 
    {
        "app_action_id" : 5,
        "name"          : "View", 
        "rank"          : 5,
    }, 
    {
        "app_action_id" : 6,
        "name"          : "Edit", 
        "rank"          : 6,
    }, 
    {
        "app_action_id" : 7,
        "name"          : "Delete", 
        "rank"          : 7,
    }, 
    {
        "app_action_id" : 8,
        "name"          : "Activate", 
        "rank"          : 8,
    }, 
    {
        "app_action_id" : 9,
        "name"          : "Deactivate", 
        "rank"          : 9,
    }, 
    {
        "app_action_id" : 10,
        "name"          : "Print Application", 
        "rank"          : 10,
    }, 
]

APP_MODULES = [
    {
        "app_module_id" : 1, 
        "name"          : "Dashboard", 
        "rank"          : 1,
        "actions"       : [3],
    }, 
    {
        "app_module_id" : 2, 
        "name"          : "My Applications", 
        "rank"          : 2,
        "actions"       : [3, 4, 5, 7, 10],
    }, 
    {
        "app_module_id" : 3, 
        "name"          : "For Approvals", 
        "rank"          : 3,
        "actions"       : [1, 2, 3, 4, 10],
    }, 
    {
        "app_module_id" : 4, 
        "name"          : "Offices", 
        "rank"          : 4,
        "actions"       : [3, 4, 5, 6],
    }, 
    {
        "app_module_id" : 5, 
        "name"          : "Positions", 
        "rank"          : 5,
        "actions"       : [3, 4, 5, 6],
    }, 
    {
        "app_module_id" : 6, 
        "name"          : "Users", 
        "rank"          : 6,
        "actions"       : [3, 4, 5, 6, 8, 9], 
    }, 
    {
        "app_module_id" : 7, 
        "name"          : "User Types",
        "rank"          : 7,
        "actions"       : [3, 4, 5, 6],
    }, 
]
