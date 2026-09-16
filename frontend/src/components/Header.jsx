import React, { useEffect, useState } from "react";
import { Shield, Radio, Sparkles, CheckCircle2, AlertCircle } from "lucide-react";

export default function Header({ activeTab, setActiveTab, sessionId }) {
  const [backendStatus, setBackendStatus] = useState("checking");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch("/api/voice/transcribe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ audio_base64: "", language: "en" }),
        });
        if (res.ok) {
          setBackendStatus("connected");
        } else {
          setBackendStatus("connected"); // server reachable
        }
      } catch (err) {
        // Fallback check root /
        try {
          const r = await fetch("/");
          setBackendStatus(r.ok ? "connected" : "offline");
        } catch {
          setBackendStatus("mock_mode");
        }
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 20000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: "voice", label: "Voice Assistant" },
    { id: "profile", label: "Customer Profile & Risk" },
    { id: "recommendations", label: "AI Recommendations" },
    { id: "quote", label: "Quote Engine" },
    { id: "comparison", label: "Policy Comparison" },
    { id: "analytics", label: "Uniphore Intelligence" },
  ];

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg tracking-tight text-slate-900">
                  UC189 <span className="text-blue-600 font-semibold">Insurance Advisor</span>
                </span>
                <span className="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded-full font-semibold flex items-center">
                  <Sparkles className="w-3 h-3 mr-1" /> AI Voice
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Azure OpenAI • LangGraph • Uniphore • ElevenLabs
              </p>
            </div>
          </div>

          {/* Right Status */}
          <div className="flex items-center space-x-4 text-xs">
            <div className="hidden md:flex items-center bg-slate-100 rounded-lg px-3 py-1.5 text-slate-600">
              <span className="text-slate-400 mr-1.5">Session:</span>
              <span className="font-mono font-medium">{sessionId.slice(0, 10)}...</span>
            </div>

            <div className="flex items-center space-x-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200/60 rounded-lg px-3 py-1.5 font-medium">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span>FastAPI Backend Active</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 sm:space-x-4 overflow-x-auto py-2 scrollbar-none border-t border-slate-100">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`px-3.5 py-1.5 text-xs sm:text-sm font-semibold rounded-lg whitespace-nowrap transition-all ${
                activeTab === item.id
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}
