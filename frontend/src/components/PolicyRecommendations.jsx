import React, { useState, useEffect } from "react";
import {
  Sparkles,
  Check,
  AlertCircle,
  TrendingUp,
  Award,
  Filter,
  ArrowRight,
  Shield,
  Layers,
} from "lucide-react";

export default function PolicyRecommendations({
  customerProfile,
  onSelectPolicyForQuote,
  onComparePolicies,
}) {
  const [budget, setBudget] = useState(500);
  const [priorities, setPriorities] = useState(["coverage", "premium", "network"]);
  const [billingCycle, setBillingCycle] = useState("monthly"); // 'monthly' | 'annual'
  const [recommendations, setRecommendations] = useState([]);
  const [aiSummary, setAiSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async (targetBudget) => {
    setLoading(true);
    try {
      const res = await fetch("/api/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: customerProfile?.customer_id || "cust_demo123",
          budget_monthly: targetBudget || budget,
          priorities: priorities,
          insurance_type: customerProfile?.insurance_type || "health",
        }),
      });

      if (!res.ok) throw new Error("Recommendation fetch failed");
      const data = await res.json();
      setRecommendations(data.recommendations || []);
      setAiSummary(data.ai_summary || "");
    } catch (err) {
      console.warn("Failed to fetch recommendations from API, using catalog:", err);
      // Fallback sample recommendations
      setRecommendations([
        {
          rank: 1,
          policy_id: "pol_003",
          policy_name: "Family Care Plus",
          provider: "FamilyFirst Insurance",
          match_score: 0.94,
          monthly_premium: 380.0,
          annual_premium: 4332.0,
          coverage_amount: 400000.0,
          key_benefits: [
            "Family floater plan (covers up to 6)",
            "Maternity & newborn care included",
            "Child immunization schedule",
            "Routine outpatient visits covered",
          ],
          limitations: ["Co-pay required for specialist visits outside network"],
          reasoning: "Optimal balance for family coverage with low out-of-pocket costs.",
        },
        {
          rank: 2,
          policy_id: "pol_001",
          policy_name: "Premium Health Shield",
          provider: "HealthGuard Insurance",
          match_score: 0.91,
          monthly_premium: 450.0,
          annual_premium: 5130.0,
          coverage_amount: 500000.0,
          key_benefits: [
            "Comprehensive hospitalization coverage",
            "Dental & vision packages included",
            "Global emergency medical coverage",
            "Zero deductible option",
          ],
          limitations: ["12-month waiting period for pre-existing conditions"],
          reasoning: "Highest coverage limit within your target budget.",
        },
        {
          rank: 3,
          policy_id: "pol_002",
          policy_name: "Essential Health Plan",
          provider: "SafeLife Insurance",
          match_score: 0.82,
          monthly_premium: 250.0,
          annual_premium: 2850.0,
          coverage_amount: 300000.0,
          key_benefits: [
            "Full in-patient hospitalization",
            "Emergency room and ambulance",
            "Preventive screening & tests",
          ],
          limitations: ["No dental or vision", "Restricted regional network"],
          reasoning: "Highly affordable baseline plan with 40% monthly savings.",
        },
      ]);
      setAiSummary(
        `Based on your target budget of $${budget}/month and family profile, 'Family Care Plus' offers the highest value at $380/month with zero waiting period for children's care.`
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations(budget);
  }, [budget]);

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center">
            <Sparkles className="w-5 h-5 mr-2 text-blue-600" />
            AI-Powered Policy Recommendations
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Ranked by multi-factor compatibility matching your risk score, budget, and family needs.
          </p>
        </div>

        {/* Monthly vs Annual Toggle */}
        <div className="flex items-center space-x-2 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs font-semibold">
          <button
            onClick={() => setBillingCycle("monthly")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              billingCycle === "monthly" ? "bg-white text-slate-900 shadow-sm" : "text-slate-500"
            }`}
          >
            Monthly
          </button>
          <button
            onClick={() => setBillingCycle("annual")}
            className={`px-3 py-1.5 rounded-lg transition-all flex items-center ${
              billingCycle === "annual" ? "bg-white text-blue-700 shadow-sm" : "text-slate-500"
            }`}
          >
            Annual <span className="ml-1 text-[10px] text-emerald-600 bg-emerald-50 px-1 py-0.2 rounded font-bold">5% OFF</span>
          </button>
        </div>
      </div>

      {/* AI Advisory Summary Callout */}
      {aiSummary && (
        <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/80 rounded-2xl flex items-start space-x-3 text-sm text-slate-800">
          <div className="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center shrink-0 mt-0.5">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <span className="font-bold text-blue-900 text-xs uppercase tracking-wide">
              Advisory Analysis
            </span>
            <p className="text-xs text-slate-700 mt-0.5 leading-relaxed">{aiSummary}</p>
          </div>
        </div>
      )}

      {/* Budget Slider Filter */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="w-full sm:w-1/2">
          <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1.5">
            <span>Target Monthly Budget</span>
            <span className="text-blue-600 font-bold">${budget} / month</span>
          </div>
          <input
            type="range"
            min="150"
            max="800"
            step="25"
            value={budget}
            onChange={(e) => setBudget(parseInt(e.target.value))}
            className="w-full accent-blue-600 cursor-pointer"
          />
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => onComparePolicies(["pol_003", "pol_001"])}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition-colors"
          >
            <Layers className="w-4 h-4" />
            <span>Compare Top 2 Plans Side-by-Side</span>
          </button>
        </div>
      </div>

      {/* Recommendation Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {recommendations.map((policy) => {
          const isTopRank = policy.rank === 1;
          const matchPercent = Math.round(policy.match_score * 100);
          const displayPrice =
            billingCycle === "annual"
              ? (policy.annual_premium / 12).toFixed(2)
              : policy.monthly_premium.toFixed(2);

          return (
            <div
              key={policy.policy_id}
              className={`bg-white rounded-2xl border transition-all flex flex-col justify-between overflow-hidden relative shadow-sm hover:shadow-md ${
                isTopRank
                  ? "border-blue-500 ring-2 ring-blue-500/20"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >
              {isTopRank && (
                <div className="bg-blue-600 text-white text-[10px] font-extrabold uppercase tracking-widest text-center py-1 flex items-center justify-center space-x-1">
                  <Award className="w-3.5 h-3.5" />
                  <span>Top AI Match ({matchPercent}%)</span>
                </div>
              )}

              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wide">
                      {policy.provider}
                    </span>
                    <h3 className="text-base font-bold text-slate-900 mt-0.5">
                      {policy.policy_name}
                    </h3>
                  </div>

                  {!isTopRank && (
                    <span className="bg-slate-100 text-slate-700 text-xs font-bold px-2 py-0.5 rounded-full">
                      {matchPercent}% Match
                    </span>
                  )}
                </div>

                {/* Price Display */}
                <div className="mt-4 pt-4 border-t border-slate-100 flex items-baseline space-x-1">
                  <span className="text-3xl font-extrabold text-slate-900">${displayPrice}</span>
                  <span className="text-xs text-slate-500">/ month</span>
                </div>
                {billingCycle === "annual" && (
                  <p className="text-[11px] text-emerald-600 font-medium">
                    Billed annually at ${policy.annual_premium.toLocaleString()}
                  </p>
                )}

                <div className="mt-3 text-xs text-slate-600 flex items-center">
                  <Shield className="w-3.5 h-3.5 mr-1 text-blue-600" />
                  <span>${policy.coverage_amount.toLocaleString()} Coverage Limit</span>
                </div>

                {/* Benefits */}
                <div className="mt-5 space-y-2">
                  <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider block">
                    Key Benefits Included:
                  </span>
                  {policy.key_benefits.map((benefit, i) => (
                    <div key={i} className="flex items-start space-x-2 text-xs text-slate-600">
                      <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                      <span>{benefit}</span>
                    </div>
                  ))}
                </div>

                {/* Limitations */}
                {policy.limitations && policy.limitations.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-slate-100">
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                      Limitations:
                    </span>
                    {policy.limitations.map((lim, i) => (
                      <p key={i} className="text-[11px] text-slate-500 italic">
                        • {lim}
                      </p>
                    ))}
                  </div>
                )}
              </div>

              {/* Card Footer Actions */}
              <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center space-x-2">
                <button
                  onClick={() => onSelectPolicyForQuote(policy)}
                  className="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold text-center transition-all flex items-center justify-center space-x-1 shadow-sm"
                >
                  <span>Select for Quote</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
