from rest_framework import serializers
from .models import Person, Resource, Account, Permission


class PersonSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    accounts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = '__all__'
    
    def get_accounts_count(self, obj):
        return obj.accounts.count()


class ResourceSerializer(serializers.ModelSerializer):
    accounts_count = serializers.SerializerMethodField()
    resource_type_display = serializers.CharField(source='get_resource_type_display', read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'
    
    def get_accounts_count(self, obj):
        return obj.accounts.count()


class PermissionSerializer(serializers.ModelSerializer):
    is_valid = serializers.ReadOnlyField()
    permission_type_display = serializers.CharField(source='get_permission_type_display', read_only=True)
    permission_scope_display = serializers.CharField(source='get_permission_scope_display', read_only=True)
    
    class Meta:
        model = Permission
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    person_name = serializers.CharField(source='person.full_name', read_only=True)
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True)
    account_status_display = serializers.CharField(source='get_account_status_display', read_only=True)
    
    class Meta:
        model = Account
        fields = '__all__'


class AccountDetailSerializer(AccountSerializer):
    person = PersonSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)
    
    class Meta:
        model = Account
        fields = '__all__'


class PersonDetailSerializer(PersonSerializer):
    accounts = AccountSerializer(many=True, read_only=True)
    
    class Meta:
        model = Person
        fields = '__all__'


class ResourceDetailSerializer(ResourceSerializer):
    accounts = AccountSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    """Serializer for complex query operations"""
    
    entities = serializers.ListField(
        child=serializers.ChoiceField(choices=['person', 'resource', 'account', 'permission']),
        required=False,
        help_text="List of entities to include in query"
    )
    
    filters = serializers.DictField(
        required=False,
        help_text="Filter conditions as key-value pairs"
    )
    
    relationships = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text="List of relationship conditions"
    )
    
    fields = serializers.DictField(
        required=False,
        help_text="Fields to include for each entity"
    )
    
    ordering = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of fields to order by"
    )
    
    limit = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=1000,
        default=100,
        help_text="Maximum number of results to return"
    )
    
    offset = serializers.IntegerField(
        required=False,
        min_value=0,
        default=0,
        help_text="Number of results to skip"
    )