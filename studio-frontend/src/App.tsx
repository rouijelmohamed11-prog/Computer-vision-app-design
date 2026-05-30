import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';
import { LandingPage } from './components/LandingPage';

function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  if (!showDashboard) {
    return <LandingPage onGetStarted={() => setShowDashboard(true)} />;
  }

  return (
    <div className="flex h-screen w-screen bg-background text-white overflow-hidden">
      {/* Background Decor */}
      <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-accent/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="fixed bottom-[-10%] right-[-10%] w-[30%] h-[30%] bg-purple-500/10 rounded-full blur-[100px] pointer-events-none" />
      
      <Sidebar />
      
      <main className="flex-1 flex flex-col relative overflow-hidden">
        <Header />
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
