import React, { useState } from "react";
import Header from "./components/Header.jsx";
import VoiceAssistant from "./components/VoiceAssistant.jsx";
import CustomerProfile from "./components/CustomerProfile.jsx";
import PolicyRecommendations from "./components/PolicyRecommendations.jsx";
import QuoteGenerator from "./components/QuoteGenerator.jsx";
import PolicyComparison from "./components/PolicyComparison.jsx";
import UniphoreAnalytics from "./components/UniphoreAnalytics.jsx";
import DemoWalkthrough from "./components/DemoWalkthrough.jsx";

export default function App() {
  const [activeTab, setActiveTab] = useState("voice");
  const [sessionId] = useState(() => "sess_" + Math.random().toString(36).substring(2, 12));

  // Customer Profile State
  const [customerProfile, setCustomerProfile] = useState({
    customer_id: "cust_demo123",
    name: "John Doe",
    age: 35,
    gender: "male",
    occupation: "Software Engineer",
    annual_income: 120000,
    location: "New York, NY",
    smoking_status: false,
    pre_existing_conditions: [],
    family_members: 4,
    insurance_type: "health",
    risk_score: 0.25,
    risk_category: "low",
    recommended_coverage: 1200000,
  });

  // Selected Policy & Active Quote State
  const [selectedPolicy, setSelectedPolicy] = useState({
    policy_id: "pol_003",
    policy_name: "Family Care Plus",
    provider: "FamilyFirst Insurance",
    monthly_premium: 380.0,
    coverage_amount: 400000.0,
    deductible: 500.0,
  });

  const [quoteData, setQuoteData] = useState({
    policy_name: "Family Care Plus",
    monthly_premium: 380.0,
    annual_premium: 4332.0,
    coverage_amount: 500000.0,
    deductible: 500.0,
  });

  const [comparisonPolicyIds, setComparisonPolicyIds] = useState(["pol_003", "pol_001"]);

  // Uniphore Conversation Intelligence Metrics
  const [uniphoreMetrics, setUniphoreMetrics] = useState({
    sentiment: "positive",
    sentimentScore: 0.85,
    tone: "enthusiastic",
    emotion: "satisfied",
    speech_tempo_wpm: 135,
    engagement_index: 0.92,
    biometric_confidence: 0.96,
  });

  // Handler for 1-Click Demo Scenarios
  const handleApplyScenario = (scenario) => {
    if (scenario.profile) setCustomerProfile(scenario.profile);
    if (scenario.quote) {
      setQuoteData(scenario.quote);
      setSelectedPolicy({ ...selectedPolicy, policy_name: scenario.quote.policy_name });
    }
  };

  const handleSelectPolicyForQuote = (policy) => {
    setSelectedPolicy(policy);
    setQuoteData({
      policy_name: policy.policy_name,
      monthly_premium: policy.monthly_premium,
      annual_premium: policy.annual_premium,
      coverage_amount: policy.coverage_amount,
      deductible: 500.0,
    });
    setActiveTab("quote");
  };

  const handleComparePolicies = (ids) => {
    if (ids) setComparisonPolicyIds(ids);
    setActiveTab("comparison");
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} sessionId={sessionId} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Demo Script Walkthrough Persona Bar */}
        <DemoWalkthrough onApplyScenario={handleApplyScenario} />

        {/* Tab View Routing */}
        {activeTab === "voice" && (
          <VoiceAssistant
            sessionId={sessionId}
            customerProfile={customerProfile}
            setCustomerProfile={setCustomerProfile}
            quoteData={quoteData}
            setQuoteData={setQuoteData}
            onOpenTab={setActiveTab}
            uniphoreMetrics={uniphoreMetrics}
            setUniphoreMetrics={setUniphoreMetrics}
          />
        )}

        {activeTab === "profile" && (
          <CustomerProfile
            profile={customerProfile}
            setProfile={setCustomerProfile}
            onProceedToQuote={() => setActiveTab("quote")}
          />
        )}

        {activeTab === "recommendations" && (
          <PolicyRecommendations
            customerProfile={customerProfile}
            onSelectPolicyForQuote={handleSelectPolicyForQuote}
            onComparePolicies={handleComparePolicies}
          />
        )}

        {activeTab === "quote" && (
          <QuoteGenerator
            customerProfile={customerProfile}
            selectedPolicy={selectedPolicy}
            quoteData={quoteData}
            setQuoteData={setQuoteData}
          />
        )}

        {activeTab === "comparison" && (
          <PolicyComparison
            selectedPolicyIds={comparisonPolicyIds}
            customerProfile={customerProfile}
          />
        )}

        {activeTab === "analytics" && (
          <UniphoreAnalytics
            metrics={uniphoreMetrics}
            customerProfile={customerProfile}
          />
        )}
      </main>

    </div>
  );
}
