import React, { useState, useCallback } from 'react';
import {
  ReactFlow,
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  MarkerType,
  Handle,
  Position,
  NodeProps
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { User, Database, Key, Shield, Plus, Search, Trash2 } from 'lucide-react';
import { QueryFilter, QueryResult } from '../types';
import { getApiUrl } from '../config';

const EntityNode: React.FC<NodeProps> = ({ data, selected }) => {
  const getIcon = () => {
    switch (data.entityType) {
      case 'person':
        return <User size={20} />;
      case 'resource':
        return <Database size={20} />;
      case 'account':
        return <Key size={20} />;
      case 'permission':
        return <Shield size={20} />;
      default:
        return null;
    }
  };

  return (
    <div
      className={`entity-node ${selected ? 'selected' : ''}`}
      style={{
        padding: '10px 15px',
        borderRadius: '8px',
        border: `2px solid ${data.color || '#666'}`,
        backgroundColor: selected ? '#f0f8ff' : 'white',
        minWidth: '150px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}
    >
      <Handle type="source" position={Position.Right} />
      <Handle type="target" position={Position.Left} />
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {getIcon()}
        <div>
          <div style={{ fontWeight: 'bold', fontSize: '14px' }}>{data.label}</div>
          <div style={{ fontSize: '11px', color: '#666' }}>{data.entityType}</div>
        </div>
      </div>
      {data.filters && Object.keys(data.filters).length > 0 && (
        <div style={{ marginTop: '8px', fontSize: '11px', color: '#888' }}>
          {Object.entries(data.filters).map(([key, value]) => (
            <div key={key}>{key}: {String(value)}</div>
          ))}
        </div>
      )}
    </div>
  );
};

const nodeTypes = {
  entity: EntityNode
};

export const QueryBuilder: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedEntities, setSelectedEntities] = useState<Set<string>>(new Set());
  const [filters, setFilters] = useState<QueryFilter['filters']>({});
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showFilterPanel, setShowFilterPanel] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const onConnect = useCallback(
    (params: Connection) => {
      const newEdge = {
        ...params,
        markerEnd: {
          type: MarkerType.ArrowClosed,
        },
        style: { stroke: '#666', strokeWidth: 2 }
      };
      setEdges((eds) => addEdge(newEdge, eds));
    },
    [setEdges]
  );

  const addEntity = (entityType: 'person' | 'resource' | 'account' | 'permission') => {
    const colors = {
      person: '#4A90E2',
      resource: '#50C878',
      account: '#FFB347',
      permission: '#FF6B6B'
    };

    const newNode: Node = {
      id: `${entityType}-${Date.now()}`,
      type: 'entity',
      position: { x: Math.random() * 400 + 100, y: Math.random() * 300 + 100 },
      data: {
        label: entityType.charAt(0).toUpperCase() + entityType.slice(1),
        entityType,
        color: colors[entityType],
        filters: {}
      }
    };

    setNodes((nds) => [...nds, newNode]);
    setSelectedEntities((prev) => new Set([...prev, entityType]));
  };

  const removeEntity = (nodeId: string) => {
    setNodes((nds) => nds.filter((n) => n.id !== nodeId));
    setEdges((eds) => eds.filter((e) => e.source !== nodeId && e.target !== nodeId));
  };

  const updateNodeFilters = (nodeId: string, nodeFilters: Record<string, any>) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === nodeId
          ? { ...node, data: { ...node.data, filters: nodeFilters } }
          : node
      )
    );
  };

  const buildQuery = (): QueryFilter => {
    const query: QueryFilter = {
      entities: Array.from(selectedEntities) as QueryFilter['entities'],
      filters: {},
      relationships: []
    };

    nodes.forEach((node) => {
      const entityType = node.data.entityType;
      if (node.data.filters && Object.keys(node.data.filters).length > 0) {
        if (!query.filters[entityType]) {
          query.filters[entityType] = {};
        }
        Object.assign(query.filters[entityType], node.data.filters);
      }
    });

    edges.forEach((edge) => {
      const sourceNode = nodes.find((n) => n.id === edge.source);
      const targetNode = nodes.find((n) => n.id === edge.target);
      
      if (sourceNode && targetNode) {
        query.relationships.push({
          from: sourceNode.data.entityType,
          to: targetNode.data.entityType
        });
      }
    });

    return query;
  };

  const executeQuery = async () => {
    setIsLoading(true);
    try {
      const query = buildQuery();
      const response = await fetch(`${getApiUrl()}/api/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(query)
      });

      if (!response.ok) {
        throw new Error('Query failed');
      }

      const result = await response.json();
      setQueryResult(result);
    } catch (error) {
      console.error('Query error:', error);
      alert('Query failed. Please check your configuration.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearQuery = () => {
    setNodes([]);
    setEdges([]);
    setSelectedEntities(new Set());
    setFilters({});
    setQueryResult(null);
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '15px', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>
          <h2 style={{ margin: 0, marginBottom: '10px' }}>Visual Query Builder</h2>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <button
              onClick={() => addEntity('person')}
              style={{
                padding: '8px 12px',
                backgroundColor: '#4A90E2',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <Plus size={16} /> Add Person
            </button>
            <button
              onClick={() => addEntity('resource')}
              style={{
                padding: '8px 12px',
                backgroundColor: '#50C878',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <Plus size={16} /> Add Resource
            </button>
            <button
              onClick={() => addEntity('account')}
              style={{
                padding: '8px 12px',
                backgroundColor: '#FFB347',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <Plus size={16} /> Add Account
            </button>
            <button
              onClick={() => addEntity('permission')}
              style={{
                padding: '8px 12px',
                backgroundColor: '#FF6B6B',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <Plus size={16} /> Add Permission
            </button>
            <button
              onClick={executeQuery}
              disabled={isLoading || nodes.length === 0}
              style={{
                padding: '8px 12px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: isLoading || nodes.length === 0 ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                opacity: isLoading || nodes.length === 0 ? 0.6 : 1
              }}
            >
              <Search size={16} /> {isLoading ? 'Executing...' : 'Execute Query'}
            </button>
            <button
              onClick={clearQuery}
              style={{
                padding: '8px 12px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <Trash2 size={16} /> Clear
            </button>
          </div>
        </div>
        
        <div style={{ flex: 1, position: 'relative' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
            onNodeClick={(event, node) => {
              setSelectedNode(node.id);
              setShowFilterPanel(true);
            }}
            onNodeDoubleClick={(event, node) => {
              if (window.confirm(`Remove ${node.data.label}?`)) {
                removeEntity(node.id);
              }
            }}
          >
            <Controls />
            <Background />
          </ReactFlow>
        </div>
      </div>

      {showFilterPanel && selectedNode && (
        <FilterPanel
          nodeId={selectedNode}
          node={nodes.find(n => n.id === selectedNode)}
          onClose={() => setShowFilterPanel(false)}
          onUpdateFilters={updateNodeFilters}
        />
      )}

      {queryResult && (
        <ResultsPanel
          results={queryResult}
          onClose={() => setQueryResult(null)}
        />
      )}
    </div>
  );
};

interface FilterPanelProps {
  nodeId: string;
  node?: Node;
  onClose: () => void;
  onUpdateFilters: (nodeId: string, filters: Record<string, any>) => void;
}

const FilterPanel: React.FC<FilterPanelProps> = ({ nodeId, node, onClose, onUpdateFilters }) => {
  const [filters, setFilters] = useState<Record<string, any>>(node?.data.filters || {});

  const handleAddFilter = () => {
    const key = prompt('Enter filter field name:');
    if (key) {
      const value = prompt('Enter filter value:');
      if (value) {
        const newFilters = { ...filters, [key]: value };
        setFilters(newFilters);
        onUpdateFilters(nodeId, newFilters);
      }
    }
  };

  const handleRemoveFilter = (key: string) => {
    const newFilters = { ...filters };
    delete newFilters[key];
    setFilters(newFilters);
    onUpdateFilters(nodeId, newFilters);
  };

  return (
    <div style={{
      width: '300px',
      backgroundColor: 'white',
      borderLeft: '1px solid #ddd',
      padding: '20px',
      overflowY: 'auto'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h3>Filters for {node?.data.label}</h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px' }}>×</button>
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <button
          onClick={handleAddFilter}
          style={{
            padding: '6px 10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            width: '100%'
          }}
        >
          Add Filter
        </button>
      </div>

      {Object.entries(filters).map(([key, value]) => (
        <div key={key} style={{
          marginBottom: '10px',
          padding: '8px',
          backgroundColor: '#f8f9fa',
          borderRadius: '4px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <strong>{key}:</strong> {String(value)}
          </div>
          <button
            onClick={() => handleRemoveFilter(key)}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#dc3545'
            }}
          >
            <Trash2 size={14} />
          </button>
        </div>
      ))}
    </div>
  );
};

interface ResultsPanelProps {
  results: QueryResult;
  onClose: () => void;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({ results, onClose }) => {
  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      height: '300px',
      backgroundColor: 'white',
      borderTop: '2px solid #ddd',
      padding: '20px',
      overflowY: 'auto',
      boxShadow: '0 -2px 10px rgba(0,0,0,0.1)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h3>Query Results</h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '24px' }}>×</button>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
        {results.results.persons && results.results.persons.length > 0 && (
          <div>
            <h4>Persons ({results.count.persons})</h4>
            <ul style={{ maxHeight: '150px', overflowY: 'auto' }}>
              {results.results.persons.map(person => (
                <li key={person.id}>{person.full_name} - {person.email}</li>
              ))}
            </ul>
          </div>
        )}
        
        {results.results.resources && results.results.resources.length > 0 && (
          <div>
            <h4>Resources ({results.count.resources})</h4>
            <ul style={{ maxHeight: '150px', overflowY: 'auto' }}>
              {results.results.resources.map(resource => (
                <li key={resource.id}>{resource.name} ({resource.resource_type})</li>
              ))}
            </ul>
          </div>
        )}
        
        {results.results.accounts && results.results.accounts.length > 0 && (
          <div>
            <h4>Accounts ({results.count.accounts})</h4>
            <ul style={{ maxHeight: '150px', overflowY: 'auto' }}>
              {results.results.accounts.map(account => (
                <li key={account.id}>{account.username} - {account.account_status}</li>
              ))}
            </ul>
          </div>
        )}
        
        {results.results.permissions && results.results.permissions.length > 0 && (
          <div>
            <h4>Permissions ({results.count.permissions})</h4>
            <ul style={{ maxHeight: '150px', overflowY: 'auto' }}>
              {results.results.permissions.map(permission => (
                <li key={permission.id}>{permission.permission_type} - {permission.permission_scope}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};