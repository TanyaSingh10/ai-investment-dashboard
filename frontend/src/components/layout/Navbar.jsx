import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Search, FileText, LogOut, BarChart3 } from 'lucide-react';
import { cn } from '../../lib/utils';

export default function Navbar() {
  const { logout } = useAuth();
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: Activity },
    { name: 'Research', path: '/research', icon: Search },
    { name: 'Reports', path: '/reports', icon: FileText },
  ];

  return (
    <nav className="border-b border-white/10 bg-card/50 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-emerald-400 flex items-center justify-center">
                <BarChart3 size={18} className="text-white" />
              </div>
              <span className="font-bold text-xl tracking-tight text-white">Nexus</span>
            </div>
            <div className="hidden sm:-my-px sm:ml-8 sm:flex sm:space-x-8">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={cn(
                      "inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors",
                      isActive
                        ? "border-primary text-white"
                        : "border-transparent text-muted-foreground hover:text-white hover:border-white/30"
                    )}
                  >
                    <Icon size={16} className="mr-2" />
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>
          <div className="flex items-center">
            <button
              onClick={logout}
              className="inline-flex items-center gap-2 px-3 py-1.5 border border-white/10 text-sm leading-4 font-medium rounded-md text-muted-foreground bg-black/20 hover:text-white hover:bg-black/40 focus:outline-none transition-all"
            >
              <LogOut size={16} />
              Sign out
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
