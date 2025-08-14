from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, default='USA')
    postal_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "People"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['last_name', 'first_name']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('DATABASE', 'Database'),
        ('API', 'API'),
        ('FILE_STORAGE', 'File Storage'),
        ('APPLICATION', 'Application'),
        ('SERVICE', 'Service'),
        ('NETWORK', 'Network Resource'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    endpoint_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['resource_type', 'name']
        indexes = [
            models.Index(fields=['resource_type']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"


class Account(models.Model):
    ACCOUNT_STATUS = [
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('PENDING', 'Pending Approval'),
        ('EXPIRED', 'Expired'),
        ('LOCKED', 'Locked'),
    ]
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='accounts')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='accounts')
    username = models.CharField(max_length=100)
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS, default='ACTIVE')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ['person', 'resource', 'username']
        ordering = ['person', 'resource', 'username']
        indexes = [
            models.Index(fields=['person', 'resource']),
            models.Index(fields=['account_status']),
        ]
    
    def __str__(self):
        return f"{self.person.full_name} - {self.resource.name} ({self.username})"
    
    @property
    def is_active(self):
        if self.account_status != 'ACTIVE':
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True


class Permission(models.Model):
    PERMISSION_TYPES = [
        ('READ', 'Read'),
        ('WRITE', 'Write'),
        ('DELETE', 'Delete'),
        ('EXECUTE', 'Execute'),
        ('ADMIN', 'Administrator'),
        ('OWNER', 'Owner'),
    ]
    
    PERMISSION_SCOPE = [
        ('FULL', 'Full Access'),
        ('LIMITED', 'Limited Access'),
        ('CONDITIONAL', 'Conditional Access'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='permissions')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES)
    permission_scope = models.CharField(max_length=20, choices=PERMISSION_SCOPE, default='LIMITED')
    resource_path = models.CharField(max_length=500, blank=True, help_text="Specific path or pattern within the resource")
    granted_at = models.DateTimeField(default=timezone.now)
    granted_by = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='permissions_granted')
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    conditions = models.JSONField(default=dict, blank=True, help_text="JSON conditions for conditional permissions")
    
    class Meta:
        unique_together = ['account', 'permission_type', 'resource_path']
        ordering = ['account', 'permission_type']
        indexes = [
            models.Index(fields=['account', 'permission_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.account} - {self.get_permission_type_display()} ({self.get_permission_scope_display()})"
    
    @property
    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True