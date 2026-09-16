import React from "react";
import { Sparkles, Play, CheckCircle2, Users, Briefcase, Heart, Award } from "lucide-react";

export default function DemoWalkthrough({ onApplyScenario }) {
  const scenarios = [
    {
      id: "family_demo",
      title: "Family Health (Full 10-Min Demo)",
      subtitle: "Step 1-6 User Flow: 35yo, 4 members, $120k income",
      badge: "Official Demo",
      profile: {
        name: "Sarah & David Miller",
        age: 35,
        gender: "female",
        occupation: "Software Architect",
        annual_income: 120000,
        location: "Austin, TX",
        smoking_status: false,
        pre_existing_conditions: [],
        family_members: 4,
        insurance_type: "health",
        risk_score: 0.25,
        risk_category: "low",
        recommended_coverage: 1200000,
      },
      quote: {
        policy_name: "Family Care Plus",
        monthly_premium: 380.0,
        annual_premium: 4332.0,
        coverage_amount: 500000.0,
        deductible: 500.0,
      },
    },
    {
      id: "young_driver",
      title: "Young Professional Individual",
      subtitle: "26yo, Software Developer, $85k, No dependents",
      badge: "Fast Track",
      profile: {
        name: "Alex Chen",
        age: 26,
        gender: "male",
        occupation: "Frontend Engineer",
        annual_income: 85000,
        location: "Seattle, WA",
        smoking_status: false,
        pre_existing_conditions: [],
        family_members: 1,
        insurance_type: "health",
        risk_score: 0.15,
        risk_category: "low",
        recommended_coverage: 850000,
      },
      quote: {
        policy_name: "Essential Health Plan",
        monthly_premium: 250.0,
        annual_premium: 2850.0,
        coverage_amount: 300000.0,
        deductible: 1000.0,
      },
    },
    {
      id: "senior_care",
      title: "Senior Comprehensive Health",
      subtitle: "58yo Consultant, Hypertension, Smoker, 2 members",
      badge: "High Risk Tier",
      profile: {
        name: "Robert Vance",
        age: 58,
        gender: "male",
        occupation: "Business Consultant",
        annual_income: 160000,
        location: "Chicago, IL",
        smoking_status: true,
        pre_existing_conditions: ["Hypertension", "High Cholesterol"],
        family_members: 2,
        insurance_type: "health",
        risk_score: 0.68,
        risk_category: "high",
        recommended_coverage: 1600000,
      },
      quote: {
        policy_name: "Executive Health Elite",
        monthly_premium: 650.0,
        annual_premium: 7410.0,
        coverage_amount: 1000000.0,
        deductible: 0.0,
      },
    },
  ];

  return (
    <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-5 shadow-sm border border-indigo-900/60 mb-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-3">
        <div className="flex items-center space-x-2">
          <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30">
            <Play className="w-4 h-4 fill-indigo-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold tracking-tight">
              1-Click Demo Script Personas
            </h3>
            <p className="text-[11px] text-indigo-200">
              Instantly populate live voice, risk profile, quote calculations, and Uniphore intelligence.
            </p>
          </div>
        </div>
        <span className="text-[10px] font-mono bg-indigo-900/80 text-indigo-300 px-2.5 py-1 rounded-lg border border-indigo-700/60 self-start md:self-auto">
          Demo Presentation Mode
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {scenarios.map((sc) => (
          <button
            key={sc.id}
            onClick={() => onApplyScenario(sc)}
            className="text-left p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-indigo-400/50 transition-all group flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-white group-hover:text-indigo-300 transition-colors">
                  {sc.title}
                </span>
                <span className="text-[9px] font-extrabold uppercase bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded border border-indigo-500/30">
                  {sc.badge}
                </span>
              </div>
              <p className="text-[11px] text-slate-300 leading-snug">{sc.subtitle}</p>
            </div>
            <div className="mt-2 text-[10px] text-indigo-400 font-semibold flex items-center group-hover:translate-x-0.5 transition-transform">
              <span>Load this persona →</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
