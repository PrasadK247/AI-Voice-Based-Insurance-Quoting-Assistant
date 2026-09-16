import React, { useState, useEffect } from "react";
import {
  Scale,
  Check,
  X,
  Sparkles,
  Shield,
  Layers,
  Award,
} from "lucide-react";

export default function PolicyComparison({ selectedPolicyIds, customerProfile }) {
  const [selectedIds, setSelectedIds] = useState(selectedPolicyIds || ["pol_003", "pol_001"]);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const allAvailable = [
    { id: "pol_001", name: "Premium Health Shield" },
    { id: "pol_002", name: "Essential Health Plan" },
    { id: "pol_003", name: "Family Care Plus" },
    { id: "pol_004", name: "Budget Health Basic" },
    { id: "pol_005", name: "Executive Health Elite" },
  ];

  const handleTogglePolicy = (id) => {
    if (selectedIds.includes(id)) {
      if (selectedIds.length > 2) {
        setSelectedIds(selectedIds.filter((p) => p !== id));
      } else {
        alert("Please select at least 2 policies for comparison.");
      }
    } else {
      if (selectedIds.length < 4) {
        setSelectedIds([...selectedIds, id]);
      } else {
        alert("You can compare up to 4 policies simultaneously.");
      }
    }
  };

  const runComparison = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/quotes/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_id: customerProfile?.customer_id || "cust_demo123",
          policy_ids: selectedIds,
        }),
      });

      if (!res.ok) throw new Error("Comparison failed");
      const data = await res.json();
      setComparisonResult(data);
    } catch (err) {
      console.warn("Comparison API error, using static mock:", err);
      setComparisonResult({
        success: true,
        policies: [
          {
            policy_id: "pol_003",
            policy_name: "Family Care Plus",
            provider: "FamilyFirst Insurance",
            tier: "family",
            monthly_premium: 380.0,
            coverage_amount: 400000.0,
            deductible: 750.0,
            key_benefits: ["Family floater plan", "Maternity coverage", "Child immunization", "Wellness programs"],
            limitations: ["Co-pay required for specialist visits"],
          },
          {
            policy_id: "pol_001",
            policy_name: "Premium Health Shield",
            provider: "HealthGuard Insurance",
            tier: "premium",
            monthly_premium: 450.0,
            coverage_amount: 500000.0,
            deductible: 500.0,
            key_benefits: ["Comprehensive hospitalization", "Dental & vision included", "Global coverage", "Zero deductible option"],
            limitations: ["12-month waiting period for pre-existing conditions"],
          },
        ],
        recommendation:
          "We recommend 'Family Care Plus' because it provides the strongest value-to-cost ratio with $400,000 in coverage for $380.00/mo, specially tailored for families.",
        comparison_summary:
          "Compared 2 policies. Monthly premiums range from $380 to $450. Family Care Plus provides maternity and child vaccines, while Premium Health Shield includes international emergency transit.",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runComparison();
  }, [selectedIds]);

  const policies = comparisonResult?.policies || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center">
            <Scale className="w-5 h-5 mr-2 text-blue-600" />
            Side-by-Side Policy Comparison Matrix
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Compare monthly premiums, deductibles, benefit tiers, and network limitations.
          </p>
        </div>

        {/* Policy Selector Pills */}
        <div className="flex flex-wrap gap-1.5">
          {allAvailable.map((pol) => {
            const active = selectedIds.includes(pol.id);
            return (
              <button
                key={pol.id}
                onClick={() => handleTogglePolicy(pol.id)}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all ${
                  active
                    ? "bg-blue-600 text-white border-blue-600 shadow-sm"
                    : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"
                }`}
              >
                {active ? "✓ " : "+ "}
                {pol.name}
              </button>
            );
          })}
        </div>
      </div>

      {/* AI Recommendation Banner */}
      {comparisonResult?.recommendation && (
        <div className="p-4 bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 rounded-2xl flex items-start space-x-3 text-sm text-slate-800">
          <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0 mt-0.5 shadow-sm">
            <Award className="w-4 h-4" />
          </div>
          <div>
            <span className="font-bold text-emerald-900 text-xs uppercase tracking-wide">
              AI Comparative Analysis & Verdict
            </span>
            <p className="text-xs text-slate-700 mt-1 leading-relaxed">
              {comparisonResult.recommendation}
            </p>
            <p className="text-[11px] text-slate-500 mt-1">
              {comparisonResult.comparison_summary}
            </p>
          </div>
        </div>
      )}

      {/* Comparison Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50">
              <th className="py-4 px-6 text-xs font-bold text-slate-500 uppercase tracking-wider w-1/4">
                Policy Attribute
              </th>
              {policies.map((p) => (
                <th key={p.policy_id} className="py-4 px-6 text-slate-900">
                  <div className="text-xs font-semibold text-slate-400 uppercase tracking-wide">
                    {p.provider}
                  </div>
                  <div className="text-base font-extrabold">{p.policy_name}</div>
                  <div className="mt-1">
                    <span className="inline-block px-2 py-0.5 bg-blue-50 text-blue-700 rounded-full text-[10px] font-bold uppercase">
                      {p.tier} Tier
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-xs text-slate-700">
            {/* Monthly Premium */}
            <tr>
              <td className="py-4 px-6 font-semibold text-slate-900 bg-slate-50/50">
                Monthly Premium
              </td>
              {policies.map((p) => (
                <td key={p.policy_id} className="py-4 px-6">
                  <span className="text-lg font-black text-slate-900">
                    ${p.monthly_premium?.toFixed(2)}
                  </span>
                  <span className="text-[11px] text-slate-500"> /mo</span>
                </td>
              ))}
            </tr>

            {/* Annual Premium */}
            <tr>
              <td className="py-4 px-6 font-semibold text-slate-900 bg-slate-50/50">
                Annual Premium (5% off)
              </td>
              {policies.map((p) => (
                <td key={p.policy_id} className="py-4 px-6 font-semibold text-emerald-700">
                  ${(p.monthly_premium * 12 * 0.95).toFixed(2)} /yr
                </td>
              ))}
            </tr>

            {/* Coverage Limit */}
            <tr>
              <td className="py-4 px-6 font-semibold text-slate-900 bg-slate-50/50">
                Aggregate Coverage Limit
              </td>
              {policies.map((p) => (
                <td key={p.policy_id} className="py-4 px-6 font-bold text-blue-700">
                  ${p.coverage_amount?.toLocaleString()}
                </td>
              ))}
            </tr>

            {/* Deductible */}
            <tr>
              <td className="py-4 px-6 font-semibold text-slate-900 bg-slate-50/50">
                Annual Deductible
              </td>
              {policies.map((p) => (
                <td key={p.policy_id} className="py-4 px-6 font-mono font-medium text-slate-800">
                  ${p.deductible?.toLocaleString()}
                </td>
              ))}
            </tr>

            {/* Key Benefits */}
            <tr>
              <td className="py-4 px-6 font-semibold text-slate-900 bg-slate-50/50 align-top">
                Key Benefits
              </td>
              {policies.map((p) => (
                <td key={p.policy_id} className="py-4 px-6 align-top">
                  <ul className="space-y-1.5">
                    {p.key_benefits?.map((b, i) => (
                      <li key={i} className="flex items-start space-x-1.5">
                        <Check className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                        <span>{b}</span>
                      </li>
                    ))}
                  </ul>
                </td>
              ))}
            </tr>

            {/* Limitations */}
            <tr>
              <td className="py-4 px-6 font-semibold text-slate-900 bg-slate-50/50 align-top">
                Limitations & Waiting Periods
              </td>
              {policies.map((p) => (
                <td key={p.policy_id} className="py-4 px-6 align-top">
                  <ul className="space-y-1.5">
                    {p.limitations?.map((lim, i) => (
                      <li key={i} className="flex items-start space-x-1.5 text-slate-500 italic">
                        <span className="text-amber-500 font-bold">•</span>
                        <span>{lim}</span>
                      </li>
                    ))}
                  </ul>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
