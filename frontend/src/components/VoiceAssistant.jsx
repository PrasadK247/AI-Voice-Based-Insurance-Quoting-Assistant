import React, { useState, useEffect, useRef } from "react";
import {
  Mic,
  MicOff,
  Send,
  Volume2,
  VolumeX,
  Sparkles,
  Bot,
  User,
  Activity,
  ArrowRight,
  Smile,
  Frown,
  Meh,
  CheckCircle2,
} from "lucide-react";

export default function VoiceAssistant({
  sessionId,
  customerProfile,
  setCustomerProfile,
  quoteData,
  setQuoteData,
  onOpenTab,
  uniphoreMetrics,
  setUniphoreMetrics,
}) {
  const [messages, setMessages] = useState([
    {
      id: "init",
      sender: "ai",
      text: "Hello! I am your AI Insurance Quoting Assistant. I can help you find the best health, life, auto, or home insurance policy, calculate your risk-adjusted quote, and compare plans. Click the microphone or pick a prompt below to get started!",
      intent: "general_inquiry",
      sentiment: "positive",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);

  const [inputQuery, setInputQuery] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [speechMuted, setSpeechMuted] = useState(false);
  const [recognitionSupported, setRecognitionSupported] = useState(false);

  const recognitionRef = useRef(null);
  const chatEndRef = useRef(null);

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Setup Browser Web Speech API for voice listening
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      setRecognitionSupported(true);
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = false;
      rec.lang = "en-US";

      rec.onstart = () => setIsListening(true);
      rec.onend = () => setIsListening(false);
      rec.onerror = (err) => {
        console.warn("Speech recognition error:", err);
        setIsListening(false);
      };
      rec.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        if (transcript) {
          handleSendMessage(transcript);
        }
      };
      recognitionRef.current = rec;
    }
  }, []);

  const toggleMic = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.start();
        } catch (err) {
          console.warn("Recognition start error:", err);
        }
      } else {
        // Fallback: trigger demo preset utterance
        handleSendMessage("Hi, I'm looking for health insurance for my family of 4.");
      }
    }
  };

  const speakText = (text) => {
    if (speechMuted || !("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  const handleSendMessage = async (textToSend) => {
    const userText = (textToSend || inputQuery).trim();
    if (!userText || isLoading) return;

    setInputQuery("");

    // Add user message to thread
    const userMsg = {
      id: "u_" + Date.now(),
      sender: "user",
      text: userText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await fetch("/api/voice/conversation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          text_input: userText,
          language: "en",
        }),
      });

      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }

      const data = await res.json();

      const aiMsg = {
        id: "ai_" + Date.now(),
        sender: "ai",
        text: data.assistant_message,
        intent: data.intent,
        sentiment: data.sentiment,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, aiMsg]);
      speakText(data.assistant_message);

      // Sync customer profile if extracted
      if (data.customer_profile && setCustomerProfile) {
        setCustomerProfile((prev) => ({
          ...prev,
          ...data.customer_profile,
          risk_score: data.risk_score !== undefined ? data.risk_score : prev.risk_score,
        }));
      }

      // Sync quote data
      if (data.quote_data && setQuoteData) {
        setQuoteData(data.quote_data);
      }

      // Sync Uniphore Metrics
      if (setUniphoreMetrics) {
        setUniphoreMetrics((prev) => ({
          ...prev,
          sentiment: data.sentiment || prev.sentiment,
          sentimentScore: data.sentiment === "positive" ? 0.85 : data.sentiment === "negative" ? 0.35 : 0.55,
          intent: data.intent || prev.intent,
        }));
      }
    } catch (err) {
      console.warn("Conversation API error, falling back locally:", err);
      // Clean fallback response
      const fallbackAiMsg = {
        id: "ai_" + Date.now(),
        sender: "ai",
        text: "I've registered your insurance requirements. Based on a family of 4, our 'Family Care Plus' plan covers hospitalization, pediatric immunizations, and routine checkups at $380/mo. Would you like to review coverage details or compare other options?",
        intent: "customer_profiling",
        sentiment: "positive",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, fallbackAiMsg]);
      speakText(fallbackAiMsg.text);
    } finally {
      setIsLoading(false);
    }
  };

  const demoPresets = [
    "I need health insurance for my family of 4",
    "I'm 35 years old, non-smoker, annual income $120,000",
    "Can you compare Family Care Plus with Premium Health Shield?",
    "Generate quote with $500 deductible and add dental & vision",
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-160px)] min-h-[580px]">
      {/* Left / Main: Chat Conversation */}
      <div className="lg:col-span-8 flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        {/* Chat Header */}
        <div className="px-6 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-800">Live Voice Session</h2>
              <p className="text-xs text-slate-500">
                LangGraph State Machine • Real-time intent detection
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setSpeechMuted(!speechMuted)}
              title={speechMuted ? "Unmute AI Voice" : "Mute AI Voice"}
              className={`p-2 rounded-lg text-xs font-medium border transition-colors ${
                speechMuted
                  ? "bg-amber-50 text-amber-700 border-amber-200"
                  : "bg-white text-slate-600 border-slate-200 hover:bg-slate-50"
              }`}
            >
              {speechMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>

            {isSpeaking && (
              <span className="flex items-center space-x-1 text-xs text-blue-600 font-medium px-2 py-1 bg-blue-50 rounded-md">
                <span className="w-1.5 h-1.5 bg-blue-600 rounded-full animate-ping"></span>
                <span>Speaking...</span>
              </span>
            )}
          </div>
        </div>

        {/* Message Feed */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex items-start space-x-3 ${
                msg.sender === "user" ? "flex-row-reverse space-x-reverse" : ""
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-white text-xs font-bold ${
                  msg.sender === "user" ? "bg-slate-800" : "bg-blue-600 shadow-sm"
                }`}
              >
                {msg.sender === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  msg.sender === "user"
                    ? "bg-slate-900 text-white rounded-tr-none"
                    : "bg-slate-100 text-slate-900 rounded-tl-none border border-slate-200/70"
                }`}
              >
                <p>{msg.text}</p>

                <div className="mt-2 flex items-center justify-between space-x-2 text-[11px] opacity-75">
                  <span>{msg.timestamp}</span>
                  {msg.intent && (
                    <span className="font-mono bg-white/40 px-1.5 py-0.5 rounded text-[10px] text-slate-700 font-semibold uppercase">
                      {msg.intent.replace("_", " ")}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex items-center space-x-3 text-slate-500 text-xs italic">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                <Sparkles className="w-4 h-4 animate-spin" />
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5">
                AI is reasoning, analyzing risk, and generating quote...
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input Bar & Controls */}
        <div className="p-4 bg-slate-50 border-t border-slate-200">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center space-x-3"
          >
            {/* Microphone Button */}
            <button
              type="button"
              onClick={toggleMic}
              className={`p-3 rounded-xl flex items-center justify-center transition-all ${
                isListening
                  ? "bg-red-500 text-white ring-4 ring-red-200 animate-pulse"
                  : "bg-blue-600 hover:bg-blue-700 text-white shadow-md shadow-blue-500/20"
              }`}
              title={isListening ? "Listening... click to stop" : "Click to speak"}
            >
              {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            {/* Input field */}
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder={
                  isListening
                    ? "Listening to your voice..."
                    : "Speak or type your insurance needs..."
                }
                className="w-full bg-white border border-slate-300 rounded-xl pl-4 pr-10 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm"
              />
            </div>

            {/* Send Button */}
            <button
              type="submit"
              disabled={!inputQuery.trim() || isLoading}
              className="px-4 py-2.5 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-white rounded-xl text-sm font-semibold flex items-center space-x-1.5 transition-all"
            >
              <span>Send</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>

          {/* Sound Wave / Listening Indicator */}
          {isListening && (
            <div className="mt-3 flex items-center justify-center space-x-1.5 h-8 bg-blue-50/80 rounded-lg border border-blue-200">
              <span className="text-xs font-semibold text-blue-700 mr-2">
                Listening to microphone:
              </span>
              <div className="w-1 bg-blue-600 rounded-full animate-sound-wave-1"></div>
              <div className="w-1 bg-blue-600 rounded-full animate-sound-wave-2"></div>
              <div className="w-1 bg-blue-600 rounded-full animate-sound-wave-3"></div>
              <div className="w-1 bg-blue-600 rounded-full animate-sound-wave-4"></div>
              <div className="w-1 bg-blue-600 rounded-full animate-sound-wave-5"></div>
            </div>
          )}
        </div>
      </div>

      {/* Right Column: Demo Script Steps & Quick Actions */}
      <div className="lg:col-span-4 flex flex-col space-y-4">
        {/* Quick Demo Script Prompts */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center">
              <Sparkles className="w-4 h-4 mr-1.5 text-blue-600" />
              10-Minute Demo Script Prompts
            </h3>
            <span className="text-[11px] bg-blue-50 text-blue-700 font-semibold px-2 py-0.5 rounded">
              1-Click Voice
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-3">
            Click any prompt below to simulate exact customer voice inputs:
          </p>

          <div className="space-y-2">
            {demoPresets.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(preset)}
                className="w-full text-left p-2.5 rounded-xl border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 text-xs text-slate-700 font-medium transition-all group flex items-start justify-between"
              >
                <span className="flex-1 pr-2">"{preset}"</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600 shrink-0 mt-0.5" />
              </button>
            ))}
          </div>
        </div>

        {/* Live Profile Glance */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex-1">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-bold text-slate-900 flex items-center">
              <Activity className="w-4 h-4 mr-1.5 text-emerald-600" />
              Dynamic Profile State
            </h3>
            <button
              onClick={() => onOpenTab("profile")}
              className="text-xs text-blue-600 hover:underline font-semibold"
            >
              Full Profile →
            </button>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="text-slate-500">Customer Name</span>
              <span className="font-semibold text-slate-800">{customerProfile?.name || "John Doe"}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="text-slate-500">Family Members</span>
              <span className="font-semibold text-slate-800">{customerProfile?.family_members || 4}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="text-slate-500">Risk Assessment</span>
              <span className="px-2 py-0.5 rounded-full font-bold uppercase text-[10px] bg-emerald-100 text-emerald-700">
                {customerProfile?.risk_category || "Low Risk"} ({(customerProfile?.risk_score || 0.25).toFixed(2)})
              </span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="text-slate-500">Target Coverage</span>
              <span className="font-semibold text-slate-800">
                ${(customerProfile?.recommended_coverage || 500000).toLocaleString()}
              </span>
            </div>
          </div>

          {/* Shortcut to Quote */}
          <div className="mt-4 pt-3 border-t border-slate-100 flex space-x-2">
            <button
              onClick={() => onOpenTab("recommendations")}
              className="flex-1 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg text-xs font-semibold text-center transition-colors"
            >
              View Recommendations
            </button>
            <button
              onClick={() => onOpenTab("quote")}
              className="flex-1 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold text-center transition-colors"
            >
              Quote Engine
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
