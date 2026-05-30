import { Plus, FolderOpen, Clock, ChevronRight, ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';

const recentProjects = [
  { id: 1, name: 'Autonomous Drone Navigation', type: 'Object Detection', date: '2 hours ago', thumbnail: 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=400&h=250&fit=crop' },
  { id: 2, name: 'Retail Analytics V2', type: 'Face Recognition', date: 'Yesterday', thumbnail: 'https://images.unsplash.com/photo-1556742044-3c52d6e88c62?w=400&h=250&fit=crop' },
  { id: 3, name: 'Medical X-Ray Analysis', type: 'Image Classification', date: '3 days ago', thumbnail: 'https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=400&h=250&fit=crop' },
  { id: 4, name: 'Smart Traffic Monitor', type: 'OCR Analysis', date: '1 week ago', thumbnail: 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=250&fit=crop' },
];

const templates = [
  { name: 'Object Detection', icon: '🎯', description: 'Real-time multi-object tracking' },
  { name: 'Face Recognition', icon: '👤', description: 'Biometric identification systems' },
  { name: 'Image Classification', icon: '🖼️', description: 'Category-based image sorting' },
  { name: 'OCR Analysis', icon: '📝', description: 'Text extraction from images' },
  { name: 'Custom Blank', icon: '✨', description: 'Start from scratch' },
];

export const Dashboard = () => {
  return (
    <div className="flex-1 overflow-y-auto p-8 space-y-12">
      {/* Welcome Section */}
      <section>
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold mb-2"
        >
          Welcome to Vision Studio AI
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-muted text-lg"
        >
          Create, open, and manage your computer vision design projects.
        </motion.p>
      </section>

      {/* Quick Actions */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.button 
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="glass-panel p-8 flex flex-col items-center justify-center gap-4 group cursor-pointer border-accent/20 hover:border-accent/50"
        >
          <div className="w-16 h-16 bg-accent rounded-2xl flex items-center justify-center shadow-lg shadow-accent/20 transition-transform group-hover:rotate-90">
            <Plus size={32} />
          </div>
          <div className="text-center">
            <h3 className="text-xl font-bold mb-1">Create New Design</h3>
            <p className="text-sm text-muted">Start a new CV project from scratch</p>
          </div>
        </motion.button>

        <motion.button 
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="glass-panel p-8 flex flex-col items-center justify-center gap-4 group cursor-pointer"
        >
          <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center group-hover:bg-white/10 transition-colors">
            <FolderOpen size={32} className="text-muted group-hover:text-white transition-colors" />
          </div>
          <div className="text-center">
            <h3 className="text-xl font-bold mb-1">Open Design</h3>
            <p className="text-sm text-muted">Import existing project files</p>
          </div>
        </motion.button>

        <motion.button 
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="glass-panel p-8 flex flex-col items-center justify-center gap-4 group cursor-pointer"
        >
          <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center group-hover:bg-white/10 transition-colors">
            <Clock size={32} className="text-muted group-hover:text-white transition-colors" />
          </div>
          <div className="text-center">
            <h3 className="text-xl font-bold mb-1">Recent Designs</h3>
            <p className="text-sm text-muted">Continue where you left off</p>
          </div>
        </motion.button>
      </section>

      {/* Recent Projects */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold">Recent Projects</h2>
          <button className="text-accent hover:underline flex items-center gap-1 text-sm font-medium">
            View all projects <ChevronRight size={16} />
          </button>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {recentProjects.map((project, index) => (
            <motion.div 
              key={project.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.1 }}
              className="glass-card group cursor-pointer overflow-hidden"
            >
              <div className="relative h-40 overflow-hidden">
                <img 
                  src={project.thumbnail} 
                  alt={project.name}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <button className="btn-primary py-2 px-4 text-sm scale-90 group-hover:scale-100 transition-transform">
                    Open <ExternalLink size={14} />
                  </button>
                </div>
              </div>
              <div className="p-4">
                <h4 className="font-bold truncate mb-1">{project.name}</h4>
                <div className="flex items-center justify-between text-xs text-muted">
                  <span>{project.type}</span>
                  <span>{project.date}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Quick Templates */}
      <section>
        <h2 className="text-2xl font-bold mb-6">Quick Templates</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {templates.map((template, index) => (
            <motion.button
              key={template.name}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 + index * 0.05 }}
              className="glass-card p-4 text-left hover:border-accent/30 transition-all group"
            >
              <span className="text-3xl mb-3 block group-hover:scale-110 transition-transform">{template.icon}</span>
              <h4 className="font-bold text-sm mb-1">{template.name}</h4>
              <p className="text-xs text-muted">{template.description}</p>
            </motion.button>
          ))}
        </div>
      </section>
    </div>
  );
};
