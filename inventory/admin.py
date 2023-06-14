from django.contrib import admin
from django.http.request import HttpRequest
from . models import Product

# admin.site.register(Product)


class ReadOnlyMixin:
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True

@admin.register(Product)
class ProductAdmin(ReadOnlyMixin, admin.ModelAdmin):
    list_display = ("name", )

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