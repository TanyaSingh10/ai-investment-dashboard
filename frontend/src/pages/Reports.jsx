import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { FileText, Trash2, Loader2, Calendar } from 'lucide-react';

const API_URL = "http://localhost:5001";

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await fetch(`${API_URL}/api/reports/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setReports(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const deleteReport = async (id) => {
    if (!window.confirm('Are you sure you want to delete this report?')) return;
    
    try {
      const response = await fetch(`${API_URL}/api/reports/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setReports(reports.filter(r => r.id !== id));
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Saved Reports</h1>
        <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm font-medium">
          {reports.length} Total
        </span>
      </div>

      {loading ? (
        <div className="flex justify-center p-12">
          <Loader2 className="animate-spin text-primary" size={32} />
        </div>
      ) : reports.length === 0 ? (
        <div className="glass-panel rounded-xl p-12 text-center text-muted-foreground border-dashed">
           <FileText className="mx-auto mb-4 opacity-50" size={48} />
           <p>No saved reports yet.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => (
            <div key={report.id} className="glass-panel p-6 rounded-xl flex flex-col group hover:border-white/20 transition-all">
              <div className="flex justify-between items-start mb-4">
                 <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                    <FileText size={20} />
                 </div>
                 <button 
                   onClick={() => deleteReport(report.id)}
                   className="text-muted-foreground hover:text-rose-400 opacity-0 group-hover:opacity-100 transition-opacity"
                 >
                   <Trash2 size={18} />
                 </button>
              </div>
              <h3 className="text-lg font-semibold mb-2 line-clamp-1 group-hover:text-primary transition-colors">{report.title}</h3>
              <p className="text-sm text-muted-foreground line-clamp-2 flex-1 mb-4 italic">"{report.query}"</p>
              
              <div className="pt-4 border-t border-white/5 flex items-center text-xs text-muted-foreground">
                <Calendar size={14} className="mr-1.5" />
                {new Date(report.created_at).toLocaleDateString(undefined, {
                  year: 'numeric', month: 'short', day: 'numeric'
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
