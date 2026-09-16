import React from "react";
import {
  Activity,
  Smile,
  Frown,
  Meh,
  Volume2,
  Brain,
  Gauge,
  Sparkles,
  CheckCircle2,
  Clock,
  Mic,
} from "lucide-react";

export default function UniphoreAnalytics({ metrics, customerProfile }) {
  const sentiment = metrics?.sentiment || "positive";
  const sentimentScore = metrics?.sentimentScore ?? 0.85;
  const tone = metrics?.tone || "enthusiastic";
  const emotion = metrics?.emotion || "satisfied";
  const tempo = metrics?.speech_tempo_wpm || 135;
  const engagement = metrics?.engagement_index ?? 0.92;
  const confidence = metrics?.biometric_confidence ?? 0.96;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h2 className="text-xl font-bold text-slate-900 flex items-center">
              <Brain className="w-5 h-5 mr-2 text-indigo-600" />
              Uniphore Conversation Intelligence & Biometrics
            </h2>
            <span className="text-[10px] font-extrabold uppercase bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full border border-indigo-200">
              Live Feed
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time acoustic analysis, sentiment classification, speech tempo, and conversational intent scoring.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="text-slate-400 font-medium">Biometric Match:</span>
          <span className="font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">
            {(confidence * 100).toFixed(0)}% Verified
          </span>
        </div>
      </div>

      {/* Top 4 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Sentiment */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div
            className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 ${
              sentiment === "positive"
                ? "bg-emerald-50 text-emerald-600 border border-emerald-200"
                : sentiment === "negative"
                ? "bg-red-50 text-red-600 border border-red-200"
                : "bg-amber-50 text-amber-600 border border-amber-200"
            }`}
          >
            {sentiment === "positive" ? (
              <Smile className="w-6 h-6" />
            ) : sentiment === "negative" ? (
              <Frown className="w-6 h-6" />
            ) : (
              <Meh className="w-6 h-6" />
            )}
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">
              Customer Sentiment
            </span>
            <div className="text-lg font-bold text-slate-900 capitalize mt-0.5">{sentiment}</div>
            <span className="text-xs text-slate-500">{(sentimentScore * 100).toFixed(0)}% Positivity Index</span>
          </div>
        </div>

        {/* Vocal Tone */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 border border-blue-200 flex items-center justify-center shrink-0">
            <Volume2 className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">
              Acoustic Tone
            </span>
            <div className="text-lg font-bold text-slate-900 capitalize mt-0.5">{tone}</div>
            <span className="text-xs text-slate-500">Emotion: {emotion}</span>
          </div>
        </div>

        {/* Speech Tempo */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 border border-indigo-200 flex items-center justify-center shrink-0">
            <Gauge className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">
              Speech Tempo
            </span>
            <div className="text-lg font-bold text-slate-900 mt-0.5">{tempo} WPM</div>
            <span className="text-xs text-emerald-600 font-medium">Optimal Conversational Pace</span>
          </div>
        </div>

        {/* Engagement Index */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-purple-50 text-purple-600 border border-purple-200 flex items-center justify-center shrink-0">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">
              Engagement Index
            </span>
            <div className="text-lg font-bold text-slate-900 mt-0.5">
              {(engagement * 100).toFixed(0)}%
            </div>
            <span className="text-xs text-purple-600 font-medium">High Active Intent</span>
          </div>
        </div>
      </div>

      {/* Deep Analytics & Conversation Signals */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Sentiment Progress & Pitch Stability */}
        <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
          <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100 flex items-center justify-between">
            <span>Conversational Dynamics</span>
            <span className="text-xs font-normal text-slate-500">Uniphore Audio Analytics Engine</span>
          </h3>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1.5">
              <span>Customer Satisfaction Probability</span>
              <span className="text-emerald-600 font-bold">88%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div className="bg-emerald-500 h-full rounded-full" style={{ width: "88%" }}></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1.5">
              <span>Customer Frustration / Hesitation Index</span>
              <span className="text-blue-600 font-bold">12% (Minimal)</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div className="bg-blue-500 h-full rounded-full" style={{ width: "12%" }}></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1.5">
              <span>Vocal Pitch & Stress Stability</span>
              <span className="text-purple-600 font-bold">94% (Calm & Clear)</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div className="bg-purple-500 h-full rounded-full" style={{ width: "94%" }}></div>
            </div>
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1">
            <span className="font-bold text-slate-700 block">Uniphore Intelligence Summary:</span>
            <p className="text-slate-600">
              Customer is highly receptive and expresses positive intent regarding family healthcare protection.
              Tone demonstrates confidence with no significant friction markers or rate spikes detected.
            </p>
          </div>
        </div>

        {/* Right: Key Behavioral Triggers & Insights */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-900 pb-2 border-b border-slate-100">
            Detected Conversation Keywords & Entities
          </h3>

          <div className="space-y-2">
            {[
              { entity: "Family Coverage", type: "Product Need", weight: "High" },
              { entity: "4 Dependents", type: "Demographics", weight: "Crucial" },
              { entity: "Hospitalization & Dental", type: "Coverage Priority", weight: "High" },
              { entity: "$500 Deductible", type: "Financial Parameter", weight: "Medium" },
              { entity: "Annual Savings", type: "Closing Trigger", weight: "High" },
            ].map((item, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-2.5 bg-slate-50 rounded-xl text-xs border border-slate-100"
              >
                <div>
                  <span className="font-bold text-slate-800">{item.entity}</span>
                  <span className="text-slate-400 block text-[10px]">{item.type}</span>
                </div>
                <span className="bg-blue-50 text-blue-700 font-semibold px-2 py-0.5 rounded text-[10px]">
                  {item.weight}
                </span>
              </div>
            ))}
          </div>

          <div className="pt-2 flex items-center justify-between text-xs text-slate-500 border-t border-slate-100">
            <span className="flex items-center">
              <Clock className="w-3.5 h-3.5 mr-1 text-slate-400" />
              Analysis Latency: &lt;180ms
            </span>
            <span className="text-emerald-600 font-semibold">Live Compliant</span>
          </div>
        </div>
      </div>
    </div>
  );
}
