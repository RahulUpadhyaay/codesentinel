import React, { useState } from 'react';
import api from '../api';
import { Play, ShieldAlert, CheckCircle, AlertTriangle, LogOut } from 'lucide-react';

export default function Auditor({ userName, onLogout }) {
  const [filename, setFilename] = useState('main.py');
  const [codeContent, setCodeContent] = useState(
    '# Paste your Python or JavaScript code here\nquery = "SELECT * FROM users WHERE name = \'" + user_input + "\'"\n'
  );
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleScan = async () => {
    setScanning(true);
    setError('');
    try {
      const res = await api.post('/api/audit/scan', {
        filename,
        code_content: codeContent,
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Scan failed');
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navbar */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="bg-emerald-500/20 p-2 rounded-lg border border-emerald-500/40">
            <ShieldAlert className="w-6 h-6 text-emerald-400" />
          </div>
          <span className="font-bold text-lg text-white">CodeSentinel AI</span>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-slate-400">Welcome, <strong className="text-white">{userName}</strong></span>
          <button
            onClick={onLogout}
            className="flex items-center space-x-1 text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Logout</span>
          </button>
        </div>
      </header>

      {/* Main Split Cockpit */}
      <main className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 p-6 max-w-7xl mx-auto w-full">
        {/* Code Input Panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col">
          <div className="flex justify-between items-center mb-3">
            <input
              type="text"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-xs text-emerald-400 px-3 py-1 rounded font-mono"
            />
            <button
              onClick={handleScan}
              disabled={scanning}
              className="flex items-center space-x-2 bg-emerald-500 hover:bg-emerald-600 text-slate-950 px-4 py-2 rounded-lg font-semibold text-sm transition-colors shadow-lg shadow-emerald-500/20"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>{scanning ? 'Auditing Code...' : 'Run Security Scan'}</span>
            </button>
          </div>

          <textarea
            value={codeContent}
            onChange={(e) => setCodeContent(e.target.value)}
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-xs text-slate-200 focus:outline-none focus:border-emerald-500/50 resize-none min-h-[350px]"
            placeholder="Paste code here..."
          />
        </div>

        {/* Audit Results Panel */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col overflow-y-auto">
          <h2 className="text-lg font-bold text-white mb-4">AI Security Audit Report</h2>

          {error && (
            <div className="bg-red-500/20 border border-red-500/40 text-red-300 p-4 rounded-xl text-sm mb-4">
              {error}
            </div>
          )}

          {!result && !scanning && (
            <div className="flex-1 flex flex-col items-center justify-center text-slate-500 space-y-2">
              <ShieldAlert className="w-12 h-12 stroke-1" />
              <p className="text-sm">Click "Run Security Scan" to audit your code snippet.</p>
            </div>
          )}

          {scanning && (
            <div className="flex-1 flex flex-col items-center justify-center text-emerald-400 space-y-3">
              <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
              <p className="text-sm font-medium">Multi-Agent AI is scanning for vulnerabilities...</p>
            </div>
          )}

          {result && !scanning && (
            <div className="space-y-6">
              {/* Score Badge */}
              <div className="flex items-center justify-between bg-slate-950 p-4 rounded-xl border border-slate-800">
                <div>
                  <span className="text-xs text-slate-400 block uppercase font-semibold">Security Health Score</span>
                  <span className="text-3xl font-extrabold text-white">{result.security_score} / 100</span>
                </div>
                <div className={`px-4 py-1.5 rounded-full text-xs font-bold ${
                  result.security_score >= 80 ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                  result.security_score >= 50 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                  'bg-red-500/20 text-red-400 border border-red-500/30'
                }`}>
                  {result.security_score >= 80 ? 'SECURE' : result.security_score >= 50 ? 'NEEDS REVIEW' : 'CRITICAL RISKS'}
                </div>
              </div>

              {/* Summary */}
              <div className="text-sm text-slate-300 bg-slate-950/50 p-3 rounded-lg border border-slate-800/80">
                {result.summary}
              </div>

              {/* Findings List */}
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-slate-200">Vulnerabilities Detected</h3>
                {result.findings.map((f, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
                    <div className="flex justify-between items-start">
                      <span className="font-bold text-sm text-white">{f.issue_title}</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        f.severity === 'HIGH' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                      }`}>
                        {f.severity}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400">{f.description}</p>
                    <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 p-2 rounded text-xs">
                      <strong>Fix:</strong> {f.suggested_fix}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}