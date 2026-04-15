import React from 'react';
import { TrendingUp, Activity, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  // Mock data for dashboard
  const stats = [
    { name: 'Active Researches', value: '12', change: '+2.1%', icon: Activity },
    { name: 'Saved Reports', value: '48', change: '+12%', icon: TrendingUp },
    { name: 'System Status', value: 'Healthy', change: 'All APIs ops', icon: AlertCircle },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Overview</h1>
        <Link 
          to="/research" 
          className="bg-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20"
        >
          New Research
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="glass-panel p-6 rounded-xl flex items-center justify-between group hover:border-primary/50 transition-colors">
              <div>
                <p className="text-sm font-medium text-muted-foreground">{stat.name}</p>
                <p className="text-3xl font-semibold mt-2">{stat.value}</p>
              </div>
              <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Icon className="text-primary" size={24} />
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent Activity/Empty State */}
      <div className="glass-panel rounded-xl p-8 text-center mt-8 border-dashed border-2 border-white/10 hover:border-white/20 transition-colors">
        <div className="mx-auto w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4">
          <Activity className="text-muted-foreground" size={32} />
        </div>
        <h3 className="text-lg font-medium mb-2">No recent reports</h3>
        <p className="text-muted-foreground mb-6 max-w-sm mx-auto">
          Start your first AI-powered investment research to generate a comprehensive analysis and save it here.
        </p>
        <Link 
          to="/research" 
          className="inline-flex justify-center bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          Start Querying
        </Link>
      </div>
    </div>
  );
}
