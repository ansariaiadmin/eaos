import React, { useState } from 'react';
import AgentDAG from './AgentDAG.jsx';

export default function Dashboard() {
  const [tab, setTab] = useState('dag');
  const [balances, setBalances] = useState({});
  const [legal, setLegal] = useState(null);
  const [q, setQ] = useState('');
  const api = (p, o) => fetch('/api' + p, o).then(r => r.json());
  const loadBalances = () => api('/ledger/balances').then(setBalances);
  const askLegal = () => api('/legal/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: q }) }).then(setLegal);
  return (
    <div style={{ fontFamily: 'sans-serif', padding: 16 }}>
      <h1>Local-First Enterprise Agent OS</h1>
      <nav>{['dag', 'ledger', 'legal'].map(t =>
        <button key={t} onClick={() => setTab(t)} style={{ marginRight: 8 }}>{t}</button>)}
      </nav>
      {tab === 'dag' && <AgentDAG />}
      {tab === 'ledger' && <div><button onClick={loadBalances}>Load Balances</button>
        <pre>{JSON.stringify(balances, null, 2)}</pre></div>}
      {tab === 'legal' && <div>
        <input value={q} onChange={e => setQ(e.target.value)} />
        <button onClick={askLegal}>Ask</button>
        {legal && <pre>{JSON.stringify(legal, null, 2)}</pre>}</div>}
    </div>);
}
