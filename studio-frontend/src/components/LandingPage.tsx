import { motion } from 'framer-motion';
import { ArrowRight, Cpu, Zap, Shield, Sparkles, ChevronRight } from 'lucide-react';
import heroImage from '../assets/hero.png';

interface LandingPageProps {
  onGetStarted: () => void;
}

export const LandingPage = ({ onGetStarted }: LandingPageProps) => {
  return (
    <div className="min-h-screen bg-background text-white overflow-x-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-background/50 backdrop-blur-xl border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent rounded-xl flex items-center justify-center">
              <Cpu className="text-white w-6 h-6" />
            </div>
            <span className="font-bold text-xl tracking-tight">Vision Studio AI</span>
          </div>
          
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-muted">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#solutions" className="hover:text-white transition-colors">Solutions</a>
            <a href="#pricing" className="hover:text-white transition-colors">Pricing</a>
            <button 
              onClick={onGetStarted}
              className="bg-accent hover:bg-accent-hover text-white px-6 py-2 rounded-full transition-all flex items-center gap-2"
            >
              Sign In <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-6">
        <div className="max-w-7xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-accent/10 text-accent text-sm font-medium border border-accent/20 mb-8">
              <Sparkles size={14} />
              The Future of Computer Vision Design
            </span>
            <h1 className="text-5xl lg:text-7xl font-bold tracking-tight mb-8 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/40">
              Build Production-Ready <br />
              <span className="text-accent">Vision AI</span> in Minutes
            </h1>
            <p className="text-lg lg:text-xl text-muted max-w-2xl mx-auto mb-12">
              The world's most intuitive platform for designing, training, and deploying computer vision models. No deep learning PhD required.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button 
                onClick={onGetStarted}
                className="w-full sm:w-auto px-8 py-4 bg-accent hover:bg-accent-hover text-white rounded-xl font-bold text-lg transition-all flex items-center justify-center gap-2 group"
              >
                Start Designing Free <ChevronRight className="group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="w-full sm:w-auto px-8 py-4 bg-white/5 hover:bg-white/10 text-white rounded-xl font-bold text-lg transition-all border border-white/10">
                View Documentation
              </button>
            </div>
          </motion.div>

          {/* Hero Image / Dashboard Preview */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="mt-20 relative"
          >
            <div className="absolute inset-0 bg-accent/20 blur-[120px] rounded-full w-2/3 mx-auto h-2/3 -z-10" />
            <div className="glass-panel p-2 rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
              <img 
                src={heroImage} 
                alt="Vision Studio Interface" 
                className="rounded-xl w-full"
              />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-6 bg-white/[0.02]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-3xl lg:text-5xl font-bold mb-6">Built for Modern AI Teams</h2>
            <p className="text-muted text-lg max-w-2xl mx-auto">
              Everything you need to move from prototype to production faster than ever.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <Zap className="text-yellow-400" />,
                title: "Rapid Prototyping",
                description: "Test your computer vision ideas in real-time with our drag-and-drop model builder."
              },
              {
                icon: <Shield className="text-green-400" />,
                title: "Production Ready",
                description: "Export models optimized for edge devices, mobile, or cloud infrastructure."
              },
              {
                icon: <Cpu className="text-accent" />,
                title: "Auto-Annotation",
                description: "Save hundreds of hours with our AI-powered dataset labeling tools."
              }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass-card p-8 group"
              >
                <div className="w-14 h-14 bg-white/5 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-white/10 transition-colors">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-4">{feature.title}</h3>
                <p className="text-muted leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Live AI Preview Section */}
      <section className="py-24 px-6 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl lg:text-5xl font-bold mb-8">See through the eyes of <span className="text-accent">AI</span></h2>
              <p className="text-muted text-lg mb-8 leading-relaxed">
                Experience the power of real-time object detection and classification. Our engine processes high-resolution video streams with sub-10ms latency.
              </p>
              <div className="space-y-4">
                {[
                  "Multi-object tracking in real-time",
                  "99.8% accuracy on standard datasets",
                  "Seamless integration with IoT devices",
                  "Edge-optimized deployment"
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="w-5 h-5 rounded-full bg-accent/20 flex items-center justify-center">
                      <div className="w-2 h-2 rounded-full bg-accent" />
                    </div>
                    <span className="text-white/80 font-medium">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="relative">
              <div className="glass-panel p-4 aspect-video relative overflow-hidden group">
                <img 
                  src="https://images.unsplash.com/photo-1593508512855-9944216593d7?w=800&q=80" 
                  alt="AI Detection Preview" 
                  className="w-full h-full object-cover rounded-lg"
                />
                {/* Mock Bounding Boxes */}
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  className="absolute top-[20%] left-[30%] w-[40%] h-[50%] border-2 border-accent rounded-sm"
                >
                  <span className="absolute -top-6 left-0 bg-accent text-[10px] px-2 py-0.5 rounded font-bold uppercase">Human 0.98</span>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                  className="absolute top-[10%] left-[10%] w-[20%] h-[30%] border-2 border-purple-500 rounded-sm"
                >
                  <span className="absolute -top-6 left-0 bg-purple-500 text-[10px] px-2 py-0.5 rounded font-bold uppercase">Backpack 0.92</span>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.4 }}
                  className="absolute bottom-[20%] right-[10%] w-[30%] h-[40%] border-2 border-yellow-500 rounded-sm"
                >
                  <span className="absolute -top-6 left-0 bg-yellow-500 text-[10px] px-2 py-0.5 rounded font-bold uppercase">Vehicle 0.89</span>
                </motion.div>
              </div>
              {/* Background Glow */}
              <div className="absolute inset-0 bg-accent/20 blur-[100px] -z-10" />
            </div>
          </div>
        </div>
      </section>

      {/* Solutions Section */}
      <section id="solutions" className="py-24 px-6 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-3xl lg:text-5xl font-bold mb-6">Industry Solutions</h2>
            <p className="text-muted text-lg max-w-2xl mx-auto">
              Tailored computer vision architectures for every vertical.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: "Smart Retail", category: "Retail & E-commerce", img: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&q=80" },
              { title: "Defect Detection", category: "Manufacturing", img: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=400&q=80" },
              { title: "Traffic Analysis", category: "Smart Cities", img: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&q=80" },
              { title: "Medical Imaging", category: "Healthcare", img: "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=400&q=80" }
            ].map((item, i) => (
              <motion.div
                key={i}
                whileHover={{ y: -10 }}
                className="glass-card overflow-hidden group cursor-pointer"
              >
                <div className="h-48 overflow-hidden">
                  <img src={item.img} alt={item.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                </div>
                <div className="p-6">
                  <span className="text-accent text-xs font-bold uppercase tracking-widest">{item.category}</span>
                  <h4 className="text-xl font-bold mt-2">{item.title}</h4>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 px-6 bg-white/[0.02]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-3xl lg:text-5xl font-bold mb-6">Simple, Transparent Pricing</h2>
            <p className="text-muted text-lg max-w-2xl mx-auto">
              Choose the plan that fits your team's needs.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                name: "Starter",
                price: "$0",
                description: "Perfect for students and hobbyists.",
                features: ["3 active projects", "500 training images", "Community support", "Basic model export"]
              },
              {
                name: "Pro",
                price: "$49",
                description: "For professional AI designers and small teams.",
                features: ["Unlimited projects", "50k training images", "Priority support", "Advanced model optimization", "Cloud API access"],
                highlight: true
              },
              {
                name: "Enterprise",
                price: "Custom",
                description: "Scaling AI across large organizations.",
                features: ["Dedicated infrastructure", "Unlimited images", "24/7 support", "Custom integrations", "On-premise deployment"]
              }
            ].map((plan, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className={`glass-card p-8 flex flex-col ${plan.highlight ? 'border-accent shadow-lg shadow-accent/10 relative scale-105 z-10' : ''}`}
              >
                {plan.highlight && (
                  <span className="absolute -top-4 left-1/2 -translate-x-1/2 bg-accent text-white px-4 py-1 rounded-full text-xs font-bold uppercase tracking-widest">Most Popular</span>
                )}
                <div className="mb-8">
                  <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                  <div className="flex items-baseline gap-1 mb-4">
                    <span className="text-4xl font-bold">{plan.price}</span>
                    {plan.price !== "Custom" && <span className="text-muted text-sm">/month</span>}
                  </div>
                  <p className="text-muted text-sm">{plan.description}</p>
                </div>
                
                <div className="space-y-4 mb-10 flex-1">
                  {plan.features.map((feature, j) => (
                    <div key={j} className="flex items-center gap-3 text-sm">
                      <Sparkles size={14} className="text-accent shrink-0" />
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>

                <button 
                  onClick={onGetStarted}
                  className={`w-full py-3 rounded-xl font-bold transition-all ${plan.highlight ? 'bg-accent hover:bg-accent-hover text-white' : 'bg-white/5 hover:bg-white/10 text-white border border-white/10'}`}
                >
                  {plan.price === "Custom" ? "Contact Sales" : "Get Started"}
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 px-6 border-y border-white/5">
        <div className="max-w-7xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-12 text-center">
          {[
            { label: "Active Users", value: "50k+" },
            { label: "Models Trained", value: "1.2M" },
            { label: "Designers", value: "15k" },
            { label: "Edge Deploys", value: "800k" }
          ].map((stat, i) => (
            <div key={i}>
              <div className="text-4xl font-bold text-white mb-2">{stat.value}</div>
              <div className="text-muted text-sm uppercase tracking-wider">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 px-6 border-t border-white/5">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-12">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
              <Cpu className="text-white w-5 h-5" />
            </div>
            <span className="font-bold text-lg tracking-tight">Vision Studio AI</span>
          </div>
          <div className="flex gap-12 text-sm text-muted">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Twitter</a>
            <a href="#" className="hover:text-white transition-colors">GitHub</a>
          </div>
          <p className="text-sm text-muted">© 2024 Vision Studio AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
