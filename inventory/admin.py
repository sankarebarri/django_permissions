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

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(GuardedModelAdmin):
    list_display = ('name',)

    def has_module_permission(self, request):
        # return super().has_module_permission(request)
        if super().has_module_permission(request):
            return True
        
    def get_queryset(self, request):
        return super().get_queryset(request)
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True

