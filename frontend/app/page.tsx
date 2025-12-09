"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useRunningAnalysis } from "@/hooks/useRunningData";
import { StatCard } from "@/components/metrics/StatCard";
import { AIReport } from "@/components/analysis/AIReport";
import { Activity, Timer, Heart, Zap, Loader2 } from "lucide-react";
import { formatDistance, formatDuration, formatPace } from "@/lib/utils";

// QueryClient 인스턴스 (실제 앱에서는 lib/queryClient.ts 등으로 분리 권장)
const queryClient = new QueryClient();

function Dashboard() {
  const { data, isLoading, isError } = useRunningAnalysis();

  if (isLoading) {
    return (
      <div className="flex h-screen w-full items-center justify-center">
        <div className="flex flex-col items-center gap-2 text-slate-500">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
          <p>Analyzing your run...</p>
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return <div className="p-8 text-center text-red-500">Failed to load data.</div>;
  }

  const { metrics } = data;

  return (
    <main className="min-h-screen bg-slate-50 p-6 md:p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Training Dashboard</h1>
            <p className="text-slate-500">
              {new Date(metrics.activity_date).toLocaleDateString()} Morning Run Analysis
            </p>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
            Sync Garmin
          </button>
        </div>

        {/* Metric Cards Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard 
            title="Distance" 
            value={formatDistance(metrics.distance_meters)} 
            unit="km" 
            icon={Activity} 
          />
          <StatCard 
            title="Duration" 
            value={formatDuration(metrics.duration_seconds)} 
            icon={Timer} 
          />
          <StatCard 
            title="Avg Pace" 
            value={formatPace(metrics.avg_pace)} 
            unit="/km" 
            icon={Zap} 
          />
          <StatCard 
            title="Avg Heart Rate" 
            value={metrics.average_heart_rate.toString()} 
            unit="bpm" 
            icon={Heart} 
            description={`Max: ${metrics.max_heart_rate} bpm`}
          />
        </div>

        {/* AI Analysis Section */}
        <AIReport data={data} />
        
      </div>
    </main>
  );
}

// Wrapper for QueryProvider
export default function Page() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );
}