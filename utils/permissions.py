from models import PermissionMapping
def has_permission(account, permission):
    return PermissionMapping.select().where(PermissionMapping.account == account, PermissionMapping.permission == permission, PermissionMapping.channel == "*").count() > 0
