### Model Level Permissions


# from django.contrib import admin
# # from django.http.request import HttpRequest
# from django.contrib.auth.admin import UserAdmin
# from . models import Product
# from django.contrib.auth.models import User, Group

# admin.site.register(Product)
# admin.site.unregister(User)
# admin.site.unregister(Group)

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser

#         if not is_superuser:
#             form.base_fields['username'].disabled = True
#             form.base_fields['is_superuser'].disabled = True
#             form.base_fields['user_permissions'].disabled = True
#             form.base_fields['groups'].disabled = True
#         return form

# class ReadOnlyAdminMixin:
    
#     def has_add_permission(self, request):
#         return False
    
#     def has_change_permission(self, request, obj=None):
#         # Checks if user has permission and not a superuser
#         # if request.user.has_perm('inventory.change_product') and request.user.is_superuser==False:
#         #     return False
#         # return True
#         if request.user.has_perm('inventory.change_product'):
#             return True
#         return False
    
#     def has_delete_permission(self, request, obj=None):
#         return False
    
#     def has_view_permission(self, request, obj=None):
#         return True

# @admin.register(Product)
# class ProductAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
#     list_display = ("name", )

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser

    #     if not is_superuser:
    #         form.base_fields['name'].disabled = True
    #     return form



    ## This should be implemented without the get_form above ##
    # def has_add_permission(self, request):
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    # def has_view_permission(self, request, obj=None):
    #     return True



### Object Level Permissions --> django-guardian
from django.contrib import admin
from .models import Product
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(GuardedModelAdmin):
    list_display = ('name',)

    def has_module_permission(self, request):
        # return super().has_module_permission(request)
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()
        
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data
    
    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return True
    
    def get_model_objects(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'edit', 'delete']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

    ### This works on the second layer -- The list of model objects
    # def has_view_permission(self, request, obj=None):
    #     return True
    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'view')
    
    # def has_change_permission(self, request, obj=None):
    #     return True
    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'change')
    
    # def has_delete_permission(self, request, obj=None):
    #     return True
    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'delete')

