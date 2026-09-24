import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';

// DAG visualizer of the agent pipeline
export default function AgentDAG() {
  const nodes = useMemo(() => [
    { id: 'voice', position: { x: 0, y: 100 }, data: { label: 'Voice STT' } },
    { id: 'redact', position: { x: 200, y: 100 }, data: { label: 'Redaction' } },
    { id: 'router', position: { x: 400, y: 100 'Hybrid Router' } 'Hybrid Router' } },
    { id: 'local', position: { x: 600, y: 40 }, data: { label: 'Local LLM' } },
    { id: 'cloud', position: { x: 600, y: 180 }, data: { label: 'Cloud LLM' } },
    { id: 'finance', position: { x: 820, y: 40 }, data: { label: 'Finance Core' } },
    { id: 'legal', position: { x: 820, y: 120 }, data: { label: 'Legal RAG' } },
    { id: 'trading', position: { x: 820, y: 200 }, data: { label: 'Trading Guard' } },
    { id: 'tax', position: { x: 1020, y: 120 }, data: { label: 'Tax Adapters' } },
  ], []);
  const edges = useMemo(() => [
    { id: 'e1', source: 'voice', target: 'redact', animated: true },
    { id: 'e2', source: 'redact', target: 'router', animated: true },
    { id: 'e3', source: 'router', target: 'local', label: 'private' },
    { id: 'e4', source: 'router', target: 'cloud', label: 'public' },
    { id: 'e5', source: 'local', target: 'finance' },
    { id: 'e6', source: 'local', target: 'legal' },
    { id: 'e7', source: 'local', target: 'trading' },
    { id: 'e8', source: 'finance', target: 'tax' },
  ], []);
  return (
    <div style={{ width: '100%', height: 480, border: '1px solid #ddd' }}>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background /><Controls />
      </ReactFlow>
    </div>);
}
