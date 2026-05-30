import { Home, LayoutGrid, FileCode, Database, Cpu, Settings } from 'lucide-react';

const navItems = [
  { icon: Home, label: 'Home', active: true },
  { icon: LayoutGrid, label: 'Projects', active: false },
  { icon: FileCode, label: 'Templates', active: false },
  { icon: Database, label: 'Datasets', active: false },
  { icon: Cpu, label: 'Models', active: false },
  { icon: Settings, label: 'Settings', active: false },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 bg-sidebar border-r border-white/5 flex flex-col h-screen">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
            <Cpu className="text-white w-5 h-5" />
          </div>
          <span className="font-bold text-lg tracking-tight">Vision Studio AI</span>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => (
            <button
              key={item.label}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                item.active 
                  ? 'bg-accent/10 text-accent' 
                  : 'text-muted hover:bg-white/5 hover:text-white'
              }`}
            >
              <item.icon size={20} />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>
      
      <div className="mt-auto p-6 border-t border-white/5">
        <div className="flex items-center gap-3 px-3 py-2 text-muted">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accent to-purple-500" />
          <div className="flex flex-col">
            <span className="text-sm font-medium text-white">Alex Chen</span>
            <span className="text-xs">Pro Plan</span>
          </div>
        </div>
      </div>
    </aside>
  );
};
