from kxy.framework.context import kxy_roles
def IsSuperAdmin():
    return 'super_admin' in kxy_roles.get()