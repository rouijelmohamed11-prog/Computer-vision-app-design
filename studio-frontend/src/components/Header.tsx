import { Search, Bell, Settings, User } from 'lucide-react';

export const Header = () => {
  return (
    <header className="h-16 border-b border-white/5 bg-background/50 backdrop-blur-md px-8 flex items-center justify-between z-10">
      <div className="flex-1 flex justify-center max-w-2xl mx-auto">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted w-4 h-4" />
          <input 
            type="text" 
            placeholder="Search projects, templates, or datasets..." 
            className="w-full bg-white/5 border border-white/10 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-accent/50 transition-colors"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <button className="p-2 text-muted hover:text-white transition-colors relative">
          <Bell size={20} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-accent rounded-full border-2 border-background" />
        </button>
        <button className="p-2 text-muted hover:text-white transition-colors">
          <Settings size={20} />
        </button>
        <div className="h-8 w-[1px] bg-white/10 mx-2" />
        <button className="flex items-center gap-2 hover:bg-white/5 p-1 rounded-full pr-3 transition-colors">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accent to-purple-500 flex items-center justify-center">
            <User size={16} className="text-white" />
          </div>
        </button>
      </div>
    </header>
  );
};
