from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import Person, Resource, Account, Permission
import random


class Command(BaseCommand):
    help = 'Populates the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Persons
        persons = []
        person_data = [
            {'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@example.com', 'city': 'New York', 'country': 'USA'},
            {'first_name': 'Jane', 'last_name': 'Doe', 'email': 'jane.doe@example.com', 'city': 'Los Angeles', 'country': 'USA'},
            {'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice.j@example.com', 'city': 'Chicago', 'country': 'USA'},
            {'first_name': 'Bob', 'last_name': 'Wilson', 'email': 'bob.wilson@example.com', 'city': 'Houston', 'country': 'USA'},
            {'first_name': 'Emma', 'last_name': 'Brown', 'email': 'emma.brown@example.com', 'city': 'Phoenix', 'country': 'USA'},
            {'first_name': 'Michael', 'last_name': 'Davis', 'email': 'michael.d@example.com', 'city': 'Philadelphia', 'country': 'USA'},
            {'first_name': 'Sarah', 'last_name': 'Miller', 'email': 'sarah.miller@example.com', 'city': 'San Antonio', 'country': 'USA'},
            {'first_name': 'David', 'last_name': 'Garcia', 'email': 'david.garcia@example.com', 'city': 'San Diego', 'country': 'USA'},
        ]
        
        for data in person_data:
            person, created = Person.objects.get_or_create(
                email=data['email'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'city': data['city'],
                    'country': data['country'],
                    'phone': f'+1-555-{random.randint(1000, 9999):04d}',
                    'address': f'{random.randint(100, 9999)} Main Street',
                    'state': random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'AZ']),
                    'postal_code': f'{random.randint(10000, 99999):05d}',
                    'is_active': True
                }
            )
            persons.append(person)
            if created:
                self.stdout.write(f'  Created person: {person.full_name}')
        
        # Create Resources
        resources = []
        resource_data = [
            {'name': 'Customer Database', 'resource_type': 'DATABASE', 'description': 'Main customer data warehouse'},
            {'name': 'Analytics API', 'resource_type': 'API', 'description': 'REST API for analytics data', 'endpoint_url': 'https://api.analytics.example.com'},
            {'name': 'File Storage S3', 'resource_type': 'FILE_STORAGE', 'description': 'AWS S3 bucket for documents', 'endpoint_url': 'https://s3.amazonaws.com/company-docs'},
            {'name': 'HR System', 'resource_type': 'APPLICATION', 'description': 'Human Resources management system'},
            {'name': 'Email Service', 'resource_type': 'SERVICE', 'description': 'Corporate email service', 'endpoint_url': 'https://mail.example.com'},
            {'name': 'VPN Gateway', 'resource_type': 'NETWORK', 'description': 'Corporate VPN access point', 'endpoint_url': 'https://vpn.example.com'},
            {'name': 'Development Database', 'resource_type': 'DATABASE', 'description': 'Development environment database'},
            {'name': 'Billing API', 'resource_type': 'API', 'description': 'Payment processing API', 'endpoint_url': 'https://api.billing.example.com'},
        ]
        
        for data in resource_data:
            resource, created = Resource.objects.get_or_create(
                name=data['name'],
                defaults={
                    'resource_type': data['resource_type'],
                    'description': data['description'],
                    'endpoint_url': data.get('endpoint_url', ''),
                    'is_active': True,
                    'metadata': {'environment': random.choice(['production', 'staging', 'development'])}
                }
            )
            resources.append(resource)
            if created:
                self.stdout.write(f'  Created resource: {resource.name}')
        
        # Create Accounts
        accounts = []
        for person in persons[:6]:  # Give accounts to first 6 persons
            for i in range(random.randint(1, 3)):  # Each person gets 1-3 accounts
                resource = random.choice(resources)
                username = f'{person.first_name.lower()}.{person.last_name.lower()}{random.randint(1, 99)}'
                
                account, created = Account.objects.get_or_create(
                    person=person,
                    resource=resource,
                    username=username,
                    defaults={
                        'account_status': random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'SUSPENDED', 'PENDING']),
                        'last_accessed': timezone.now() - timedelta(days=random.randint(0, 30)),
                        'expires_at': timezone.now() + timedelta(days=random.randint(30, 365)) if random.random() > 0.5 else None,
                        'metadata': {'department': random.choice(['IT', 'Sales', 'Marketing', 'Engineering', 'HR'])}
                    }
                )
                if created:
                    accounts.append(account)
                    self.stdout.write(f'  Created account: {account}')
        
        # Create Permissions
        permission_types = ['READ', 'WRITE', 'DELETE', 'EXECUTE', 'ADMIN', 'OWNER']
        permission_scopes = ['FULL', 'LIMITED', 'CONDITIONAL']
        
        for account in accounts:
            num_permissions = random.randint(1, 4)
            used_types = set()
            
            for _ in range(num_permissions):
                perm_type = random.choice([pt for pt in permission_types if pt not in used_types])
                used_types.add(perm_type)
                
                permission, created = Permission.objects.get_or_create(
                    account=account,
                    permission_type=perm_type,
                    defaults={
                        'permission_scope': random.choice(permission_scopes),
                        'resource_path': f'/{random.choice(["data", "api", "admin", "reports"])}/{random.choice(["*", "read", "write", "manage"])}',
                        'granted_by': random.choice(persons) if random.random() > 0.3 else None,
                        'expires_at': timezone.now() + timedelta(days=random.randint(30, 365)) if random.random() > 0.7 else None,
                        'is_active': random.random() > 0.1,
                        'conditions': {'ip_range': '192.168.1.0/24'} if random.random() > 0.8 else {}
                    }
                )
                if created:
                    self.stdout.write(f'    Created permission: {permission}')
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write(f'  Persons: {Person.objects.count()}')
        self.stdout.write(f'  Resources: {Resource.objects.count()}')
        self.stdout.write(f'  Accounts: {Account.objects.count()}')
        self.stdout.write(f'  Permissions: {Permission.objects.count()}')