from django.contrib import admin
from .models import Person, Resource, Account, Permission


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['last_name', 'first_name']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource_type', 'endpoint_url', 'is_active', 'created_at']
    list_filter = ['resource_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'endpoint_url']
    ordering = ['resource_type', 'name']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('name', 'resource_type', 'description', 'endpoint_url')
        }),
        ('Configuration', {
            'fields': ('metadata',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


class PermissionInline(admin.TabularInline):
    model = Permission
    extra = 1
    fields = ['permission_type', 'permission_scope', 'resource_path', 'is_active', 'expires_at']
    readonly_fields = ['granted_at']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['person', 'resource', 'username', 'account_status', 'is_active', 'created_at']
    list_filter = ['account_status', 'resource__resource_type', 'created_at']
    search_fields = ['person__first_name', 'person__last_name', 'person__email', 'username', 'resource__name']
    ordering = ['person', 'resource', 'username']
    date_hierarchy = 'created_at'
    inlines = [PermissionInline]
    
    fieldsets = (
        ('Account Information', {
            'fields': ('person', 'resource', 'username')
        }),
        ('Status', {
            'fields': ('account_status', 'last_accessed', 'expires_at')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['account', 'permission_type', 'permission_scope', 'resource_path', 'is_valid', 'granted_at']
    list_filter = ['permission_type', 'permission_scope', 'is_active', 'granted_at']
    search_fields = ['account__person__first_name', 'account__person__last_name', 
                     'account__resource__name', 'resource_path']
    ordering = ['account', 'permission_type']
    date_hierarchy = 'granted_at'
    
    fieldsets = (
        ('Permission Details', {
            'fields': ('account', 'permission_type', 'permission_scope', 'resource_path')
        }),
        ('Grant Information', {
            'fields': ('granted_by', 'granted_at', 'expires_at')
        }),
        ('Conditions', {
            'fields': ('conditions', 'is_active'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['granted_at']
    
    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True
    is_valid.short_description = 'Valid'
