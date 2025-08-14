from django.http import JsonResponse
from django.db.models import Q, Count, Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person, Resource, Account, Permission
from .serializers import (
    PersonSerializer, PersonDetailSerializer,
    ResourceSerializer, ResourceDetailSerializer,
    AccountSerializer, AccountDetailSerializer,
    PermissionSerializer, QuerySerializer
)


def ping(_request):
    """Simple ping endpoint for testing API connectivity."""
    return JsonResponse({"message": "pong"})


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filterset_fields = ['is_active', 'country', 'city']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PersonDetailSerializer
        return PersonSerializer
    
    @action(detail=True, methods=['get'])
    def accounts(self, request, pk=None):
        person = self.get_object()
        accounts = person.accounts.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filterset_fields = ['resource_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'resource_type']
    ordering = ['resource_type', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ResourceDetailSerializer
        return ResourceSerializer
    
    @action(detail=True, methods=['get'])
    def accounts(self, request, pk=None):
        resource = self.get_object()
        accounts = resource.accounts.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.select_related('person', 'resource').prefetch_related('permissions')
    serializer_class = AccountSerializer
    filterset_fields = ['account_status', 'person', 'resource']
    search_fields = ['username', 'person__first_name', 'person__last_name', 'resource__name']
    ordering_fields = ['created_at', 'username']
    ordering = ['person', 'resource', 'username']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AccountDetailSerializer
        return AccountSerializer
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        account = self.get_object()
        permissions = account.permissions.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def grant_permission(self, request, pk=None):
        account = self.get_object()
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.select_related('account__person', 'account__resource')
    serializer_class = PermissionSerializer
    filterset_fields = ['permission_type', 'permission_scope', 'is_active']
    search_fields = ['resource_path', 'account__username']
    ordering_fields = ['granted_at', 'permission_type']
    ordering = ['account', 'permission_type']


class QueryAPIView(APIView):
    """
    Complex query endpoint for query-by-example operations.
    Supports filtering across multiple entities and their relationships.
    """
    
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        entities = data.get('entities', ['person'])
        filters = data.get('filters', {})
        relationships = data.get('relationships', [])
        fields = data.get('fields', {})
        ordering = data.get('ordering', [])
        limit = data.get('limit', 100)
        offset = data.get('offset', 0)
        
        results = {}
        
        if 'person' in entities:
            persons = self._query_persons(filters, relationships, ordering)
            persons = persons[offset:offset+limit]
            person_serializer = PersonDetailSerializer if fields.get('person', {}).get('include_accounts') else PersonSerializer
            results['persons'] = person_serializer(persons, many=True).data
        
        if 'resource' in entities:
            resources = self._query_resources(filters, relationships, ordering)
            resources = resources[offset:offset+limit]
            resource_serializer = ResourceDetailSerializer if fields.get('resource', {}).get('include_accounts') else ResourceSerializer
            results['resources'] = resource_serializer(resources, many=True).data
        
        if 'account' in entities:
            accounts = self._query_accounts(filters, relationships, ordering)
            accounts = accounts[offset:offset+limit]
            account_serializer = AccountDetailSerializer if fields.get('account', {}).get('include_details') else AccountSerializer
            results['accounts'] = account_serializer(accounts, many=True).data
        
        if 'permission' in entities:
            permissions = self._query_permissions(filters, relationships, ordering)
            permissions = permissions[offset:offset+limit]
            results['permissions'] = PermissionSerializer(permissions, many=True).data
        
        return Response({
            'results': results,
            'count': self._get_counts(entities, filters, relationships),
            'query': data
        })
    
    def _query_persons(self, filters, relationships, ordering):
        queryset = Person.objects.all()
        
        if 'person' in filters:
            for key, value in filters['person'].items():
                if key == 'search':
                    queryset = queryset.filter(
                        Q(first_name__icontains=value) |
                        Q(last_name__icontains=value) |
                        Q(email__icontains=value)
                    )
                else:
                    queryset = queryset.filter(**{key: value})
        
        for rel in relationships:
            if rel.get('from') == 'person' and rel.get('to') == 'account':
                if rel.get('condition'):
                    queryset = queryset.filter(accounts__account_status=rel['condition'].get('status'))
        
        if ordering:
            queryset = queryset.order_by(*ordering)
        
        return queryset.distinct()
    
    def _query_resources(self, filters, relationships, ordering):
        queryset = Resource.objects.all()
        
        if 'resource' in filters:
            for key, value in filters['resource'].items():
                if key == 'search':
                    queryset = queryset.filter(
                        Q(name__icontains=value) |
                        Q(description__icontains=value)
                    )
                else:
                    queryset = queryset.filter(**{key: value})
        
        if ordering:
            queryset = queryset.order_by(*ordering)
        
        return queryset.distinct()
    
    def _query_accounts(self, filters, relationships, ordering):
        queryset = Account.objects.select_related('person', 'resource')
        
        if 'account' in filters:
            for key, value in filters['account'].items():
                queryset = queryset.filter(**{key: value})
        
        for rel in relationships:
            if rel.get('from') == 'account' and rel.get('to') == 'permission':
                if rel.get('condition'):
                    queryset = queryset.filter(permissions__permission_type=rel['condition'].get('type'))
        
        if ordering:
            queryset = queryset.order_by(*ordering)
        
        return queryset.distinct()
    
    def _query_permissions(self, filters, relationships, ordering):
        queryset = Permission.objects.select_related('account__person', 'account__resource')
        
        if 'permission' in filters:
            for key, value in filters['permission'].items():
                queryset = queryset.filter(**{key: value})
        
        if ordering:
            queryset = queryset.order_by(*ordering)
        
        return queryset.distinct()
    
    def _get_counts(self, entities, filters, relationships):
        counts = {}
        
        if 'person' in entities:
            counts['persons'] = self._query_persons(filters, relationships, []).count()
        if 'resource' in entities:
            counts['resources'] = self._query_resources(filters, relationships, []).count()
        if 'account' in entities:
            counts['accounts'] = self._query_accounts(filters, relationships, []).count()
        if 'permission' in entities:
            counts['permissions'] = self._query_permissions(filters, relationships, []).count()
        
        return counts