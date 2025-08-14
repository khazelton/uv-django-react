export interface Person {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  date_of_birth?: string;
  address?: string;
  city?: string;
  state?: string;
  country: string;
  postal_code?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  full_name: string;
  accounts_count?: number;
  accounts?: Account[];
}

export interface Resource {
  id: number;
  name: string;
  resource_type: 'DATABASE' | 'API' | 'FILE_STORAGE' | 'APPLICATION' | 'SERVICE' | 'NETWORK';
  description?: string;
  endpoint_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  metadata?: Record<string, any>;
  accounts_count?: number;
  resource_type_display?: string;
  accounts?: Account[];
}

export interface Account {
  id: number;
  person: number | Person;
  resource: number | Resource;
  username: string;
  account_status: 'ACTIVE' | 'SUSPENDED' | 'PENDING' | 'EXPIRED' | 'LOCKED';
  created_at: string;
  updated_at: string;
  last_accessed?: string;
  expires_at?: string;
  metadata?: Record<string, any>;
  is_active: boolean;
  person_name?: string;
  resource_name?: string;
  permissions?: Permission[];
  account_status_display?: string;
}

export interface Permission {
  id: number;
  account: number;
  permission_type: 'READ' | 'WRITE' | 'DELETE' | 'EXECUTE' | 'ADMIN' | 'OWNER';
  permission_scope: 'FULL' | 'LIMITED' | 'CONDITIONAL';
  resource_path?: string;
  granted_at: string;
  granted_by?: number;
  expires_at?: string;
  is_active: boolean;
  conditions?: Record<string, any>;
  is_valid: boolean;
  permission_type_display?: string;
  permission_scope_display?: string;
}

export interface QueryFilter {
  entities: ('person' | 'resource' | 'account' | 'permission')[];
  filters: {
    person?: Record<string, any>;
    resource?: Record<string, any>;
    account?: Record<string, any>;
    permission?: Record<string, any>;
  };
  relationships: {
    from: string;
    to: string;
    condition?: Record<string, any>;
  }[];
  fields?: Record<string, any>;
  ordering?: string[];
  limit?: number;
  offset?: number;
}

export interface QueryResult {
  results: {
    persons?: Person[];
    resources?: Resource[];
    accounts?: Account[];
    permissions?: Permission[];
  };
  count: {
    persons?: number;
    resources?: number;
    accounts?: number;
    permissions?: number;
  };
  query: QueryFilter;
}