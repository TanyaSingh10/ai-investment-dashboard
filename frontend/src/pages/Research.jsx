import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Search, Loader2, Save, TrendingUp, Presentation, AlertOctagon, Link as LinkIcon } from 'lucide-react';

const API_URL = "http://localhost:5001";

export default function Research() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [saving, setSaving] = useState(false);
  const { token } = useAuth();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;
    
    setLoading(true);
    setResult(null);
    
    try {
      const response = await fetch(`${API_URL}/api/research/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ query })
      });
      
      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        alert(data.message || 'An error occurred during research.');
      }
    } catch (error) {
      console.error(error);
      alert('Failed to connect to the research service.');
    } finally {
      setLoading(false);
    }
  };

  const saveReport = async () => {
    if (!result) return;
    setSaving(true);
    try {
      const response = await fetch(`${API_URL}/api/reports/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          title: result.company_overview?.name ? `${result.company_overview.name} Analysis` : 'Custom Research Report',
          query: query,
          report_data: result
        })
      });
      
      const data = await response.json();
      if (response.ok) {
        alert('Report saved successfully!');
      } else {
        alert(data.message || 'Failed to save report.');
      }
    } catch (error) {
       alert('Error saving report.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="text-center space-y-4 pt-10 pb-6">
        <h1 className="text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">
          AI Investment Research
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Ask anything about earnings, stock performance, or company news. Our AI will automatically gather data from tools and knowledge bases.
        </p>
      </div>

      <form onSubmit={handleSearch} className="relative max-w-3xl mx-auto group">
        <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        <div className="relative flex items-center glass-panel rounded-full overflow-hidden p-2 shadow-2xl">
          <div className="pl-4 pr-2 text-primary">
             <Search size={24} />
          </div>
          <input
            type="text"
            className="flex-1 bg-transparent border-none focus:outline-none text-lg px-2 placeholder:text-muted-foreground/50 py-3"
            placeholder="e.g. Analyze Apple's latest earnings and stock trend..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={loading}
            className="bg-primary text-primary-foreground px-8 py-3 rounded-full font-medium hover:bg-primary/90 disabled:opacity-50 transition-all shadow-lg min-w-[120px] flex justify-center"
          >
            {loading ? <Loader2 className="animate-spin" size={24} /> : 'Analyze'}
          </button>
        </div>
      </form>

      {/* Results View */}
      {result && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-700 mt-12">
          <div className="flex justify-between items-center bg-card/40 border border-white/5 p-4 rounded-xl backdrop-blur-sm">
             <h2 className="text-xl font-bold flex items-center gap-2">
                <Presentation className="text-primary" />
                {result.company_overview?.name || 'Analysis Result'} 
                <span className="text-sm font-normal text-muted-foreground ml-2">({result.company_overview?.sector})</span>
             </h2>
             <button 
                onClick={saveReport} 
                disabled={saving}
                className="flex items-center gap-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-lg text-sm transition-colors"
             >
                {saving ? <Loader2 className="animate-spin" size={16} /> : <Save size={16} />}
                Save Report
             </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-panel p-6 rounded-xl space-y-4">
               <h3 className="text-lg font-semibold flex items-center gap-2 text-emerald-400">
                 <TrendingUp size={20} /> Stock Data
               </h3>
               {result.stock_data?.error ? (
                  <p className="text-red-400">{result.stock_data.error}</p>
               ) : (
                  <div>
                    <p className="text-4xl font-bold">${result.stock_data?.price}</p>
                    <p className="text-emerald-500 font-medium">{result.stock_data?.change || ''}</p>
                    <p className="text-xs text-muted-foreground mt-4">Source: {result.stock_data?.source}</p>
                  </div>
               )}
            </div>

            <div className="glass-panel p-6 rounded-xl space-y-4">
               <h3 className="text-lg font-semibold flex items-center gap-2 text-rose-400">
                 <AlertOctagon size={20} /> Risk & Context
               </h3>
               <p className="text-muted-foreground leading-relaxed">
                 {result.risk_analysis || 'No risk analysis provided.'}
               </p>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-xl space-y-4">
             <h3 className="text-lg font-semibold">Recent News & Sentiment</h3>
             <div className="space-y-3">
               {result.news?.map((n, i) => (
                 <div key={i} className="flex flex-col sm:flex-row justify-between items-start sm:items-center p-3 rounded-lg bg-black/20 hover:bg-black/40 transition-colors border border-white/5">
                   <div className="flex-1">
                     <p className="font-medium">{n.title}</p>
                     <p className="text-xs text-muted-foreground mt-1 text-primary hover:underline cursor-pointer">{n.source}</p>
                   </div>
                   <span className={`mt-2 sm:mt-0 text-xs px-2.5 py-1 rounded-full border ${n.sentiment === 'positive' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : n.sentiment === 'negative' ? 'bg-rose-500/10 border-rose-500/20 text-rose-400' : 'bg-blue-500/10 border-blue-500/20 text-blue-400'}`}>
                      {n.sentiment?.toUpperCase() || 'NEUTRAL'}
                   </span>
                 </div>
               ))}
               {(!result.news || result.news.length === 0) && <p className="text-muted-foreground text-sm">No recent news found.</p>}
             </div>
          </div>

          <div className="bg-card/30 p-4 rounded-xl border border-white/5 flex gap-2 overflow-x-auto">
             <span className="text-sm font-medium text-muted-foreground whitespace-nowrap">Sources used:</span>
             {result.sources?.map((s, i) => (
                <span key={i} className="flex items-center gap-1 text-xs bg-white/5 px-2 py-1 rounded-md whitespace-nowrap">
                  <LinkIcon size={12} /> {s}
                </span>
             ))}
          </div>

        </div>
      )}
    </div>
  );
}
