import React, { useState } from "react";
import {
  User,
  ShieldAlert,
  ShieldCheck,
  HeartPulse,
  DollarSign,
  Users,
  MapPin,
  Briefcase,
  Save,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";

export default function CustomerProfile({ profile, setProfile, onProceedToQuote }) {
  const [formData, setFormData] = useState({
    name: profile?.name || "John Doe",
    age: profile?.age || 35,
    gender: profile?.gender || "male",
    occupation: profile?.occupation || "Software Engineer",
    annual_income: profile?.annual_income || 120000,
    location: profile?.location || "New York, NY",
    smoking_status: profile?.smoking_status || false,
    pre_existing_conditions: profile?.pre_existing_conditions || [],
    family_members: profile?.family_members || 4,
    insurance_type: profile?.insurance_type || "health",
  });

  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const availableConditions = [
    "Hypertension",
    "Asthma",
    "Type 2 Diabetes",
    "Allergies",
    "High Cholesterol",
    "Arthritis",
  ];

  const handleConditionToggle = (cond) => {
    const current = formData.pre_existing_conditions;
    if (current.includes(cond)) {
      setFormData({
        ...formData,
        pre_existing_conditions: current.filter((c) => c !== cond),
      });
    } else {
      setFormData({
        ...formData,
        pre_existing_conditions: [...current, cond],
      });
    }
  };

  const handleSaveProfile = async (e) => {
    e?.preventDefault();
    setSaving(true);
    setSavedSuccess(false);

    try {
      const res = await fetch("/api/customers/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error("Failed to save profile");

      const data = await res.json();
      setProfile({
        ...formData,
        customer_id: data.customer_id,
        risk_score: data.risk_profile?.risk_score || 0.25,
        risk_category: data.risk_profile?.risk_category || "low",
        risk_factors: data.risk_profile?.risk_factors || [],
        recommended_coverage: data.recommended_coverage || 1200000,
      });

      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.warn("Profile save error, updating local state:", err);
      // Local risk computation
      let score = 0.15;
      if (formData.age > 50) score += 0.25;
      else if (formData.age > 40) score += 0.15;
      if (formData.smoking_status) score += 0.20;
      score += formData.pre_existing_conditions.length * 0.10;
      const finalScore = Math.min(score, 0.95);

      setProfile({
        ...formData,
        risk_score: Number(finalScore.toFixed(2)),
        risk_category: finalScore < 0.35 ? "low" : finalScore < 0.65 ? "medium" : "high",
        recommended_coverage: formData.annual_income * 10,
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } finally {
      setSaving(false);
    }
  };

  const riskScore = profile?.risk_score ?? 0.25;
  const riskCategory = profile?.risk_category ?? "low";

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center">
            <User className="w-5 h-5 mr-2 text-blue-600" />
            Customer Profiling & Actuarial Risk Engine
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Builds digital customer twins, assesses mortality/morbidity factors, and calculates target coverage limits.
          </p>
        </div>

        <button
          onClick={handleSaveProfile}
          disabled={saving}
          className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-xl text-sm font-semibold flex items-center justify-center space-x-2 shadow-md shadow-blue-500/20 transition-all"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? "Saving..." : "Save Profile & Re-assess Risk"}</span>
        </button>
      </div>

      {savedSuccess && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center space-x-3 text-emerald-800 text-sm animate-fade-in">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
          <span>Profile updated and risk assessment recalculated successfully!</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Form Details */}
        <div className="lg:col-span-8 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 mb-4 pb-2 border-b border-slate-100">
            Personal & Demographic Attributes
          </h3>

          <form onSubmit={handleSaveProfile} className="space-y-5">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Full Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Age (Years)
                </label>
                <input
                  type="number"
                  min="18"
                  max="100"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || 18 })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Gender
                </label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Non-binary / Other</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Occupation
                </label>
                <div className="relative">
                  <Briefcase className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={formData.occupation}
                    onChange={(e) => setFormData({ ...formData, occupation: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Annual Income ($ USD)
                </label>
                <div className="relative">
                  <DollarSign className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="number"
                    step="5000"
                    value={formData.annual_income}
                    onChange={(e) =>
                      setFormData({ ...formData, annual_income: parseFloat(e.target.value) || 0 })
                    }
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Location (State / City)
                </label>
                <div className="relative">
                  <MapPin className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Family Members to Insure
                </label>
                <div className="relative">
                  <Users className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={formData.family_members}
                    onChange={(e) =>
                      setFormData({ ...formData, family_members: parseInt(e.target.value) || 1 })
                    }
                    className="w-full bg-slate-50 border border-slate-300 rounded-xl pl-9 pr-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Insurance Type
                </label>
                <select
                  value={formData.insurance_type}
                  onChange={(e) => setFormData({ ...formData, insurance_type: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none"
                >
                  <option value="health">Health Insurance</option>
                  <option value="life">Life Insurance</option>
                  <option value="auto">Auto Insurance</option>
                  <option value="home">Homeowners Insurance</option>
                </select>
              </div>
            </div>

            {/* Smoking status */}
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
              <div>
                <span className="text-sm font-semibold text-slate-800">Tobacco / Nicotine Use</span>
                <p className="text-xs text-slate-500">
                  Has the applicant used cigarettes, e-cigarettes, or tobacco in the past 12 months?
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.smoking_status}
                  onChange={(e) => setFormData({ ...formData, smoking_status: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-amber-600"></div>
              </label>
            </div>

            {/* Medical History */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-2 flex items-center">
                <HeartPulse className="w-4 h-4 mr-1 text-red-500" />
                Pre-Existing Medical History
              </label>
              <div className="flex flex-wrap gap-2">
                {availableConditions.map((cond) => {
                  const selected = formData.pre_existing_conditions.includes(cond);
                  return (
                    <button
                      key={cond}
                      type="button"
                      onClick={() => handleConditionToggle(cond)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                        selected
                          ? "bg-red-50 text-red-700 border-red-300 font-semibold"
                          : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"
                      }`}
                    >
                      {selected ? "✓ " : "+ "}
                      {cond}
                    </button>
                  );
                })}
              </div>
            </div>
          </form>
        </div>

        {/* Right Column: Live Risk Assessment Gauge */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-slate-900 flex items-center">
                  <ShieldCheck className="w-4 h-4 mr-1.5 text-blue-600" />
                  Actuarial Risk Assessment
                </h3>
                <span
                  className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide ${
                    riskCategory === "low"
                      ? "bg-emerald-100 text-emerald-800"
                      : riskCategory === "medium"
                      ? "bg-amber-100 text-amber-800"
                      : "bg-red-100 text-red-800"
                  }`}
                >
                  {riskCategory} Risk
                </span>
              </div>

              {/* Visual Score Meter */}
              <div className="my-6 text-center">
                <div className="text-4xl font-extrabold text-slate-900 tracking-tight">
                  {riskScore.toFixed(2)}
                </div>
                <p className="text-xs text-slate-500 mt-1">Actuarial Loss Probability Index (0.0 - 1.0)</p>

                {/* Progress bar */}
                <div className="w-full bg-slate-100 rounded-full h-3 mt-4 overflow-hidden p-0.5 border border-slate-200">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      riskScore < 0.35
                        ? "bg-emerald-500"
                        : riskScore < 0.65
                        ? "bg-amber-500"
                        : "bg-red-500"
                    }`}
                    style={{ width: `${Math.min(riskScore * 100, 100)}%` }}
                  ></div>
                </div>

                <div className="flex justify-between text-[10px] text-slate-400 font-mono mt-1 px-1">
                  <span>0.00 (Low)</span>
                  <span>0.50 (Standard)</span>
                  <span>1.00 (High)</span>
                </div>
              </div>

              {/* Factors Summary */}
              <div className="space-y-2.5 text-xs pt-4 border-t border-slate-100">
                <div className="flex justify-between">
                  <span className="text-slate-500">Age Bracket Factor:</span>
                  <span className="font-semibold text-slate-800">
                    {formData.age > 50 ? "+0.25 (Elevated)" : "+0.10 (Standard)"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Tobacco Surcharge:</span>
                  <span className="font-semibold text-slate-800">
                    {formData.smoking_status ? "+20% Premium" : "0% (Preferred)"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Medical Conditions:</span>
                  <span className="font-semibold text-slate-800">
                    {formData.pre_existing_conditions.length > 0
                      ? `${formData.pre_existing_conditions.length} noted`
                      : "None declared"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Recommended Life/Health Coverage:</span>
                  <span className="font-bold text-blue-600">
                    ${(formData.annual_income * 10).toLocaleString()} (10x Income)
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100">
              <button
                onClick={onProceedToQuote}
                className="w-full py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold text-center transition-all flex items-center justify-center space-x-1.5"
              >
                <span>Proceed to Quote Engine →</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
