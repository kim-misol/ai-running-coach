"use client";

import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { TimeSeriesDataPoint } from "@/lib/types";
import { formatPace } from "@/lib/utils";

interface RunChartProps {
  data: TimeSeriesDataPoint[];
}

export function RunChart({ data }: RunChartProps) {
  return (
    <div className="w-full bg-white rounded-xl border p-6 shadow-sm">
      <h3 className="text-lg font-semibold mb-6 text-slate-800 flex items-center gap-2">
        📈 Heart Rate & Pace Analysis
      </h3>
      
      <div className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorHr" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
              </linearGradient>
            </defs>
            
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            
            {/* X축: 시간 */}
            <XAxis 
              dataKey="time_offset" 
              tickFormatter={(val: number) => `${Math.floor(val / 60)}m`}
              stroke="#94a3b8"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />

            {/* Y축 (좌측): 심박수 */}
            <YAxis 
              yAxisId="left" 
              domain={['dataMin - 10', 'dataMax + 10']} 
              stroke="#ef4444"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              label={{ value: 'BPM', angle: -90, position: 'insideLeft', fill: '#ef4444', fontSize: 10 }}
            />

            {/* Y축 (우측): 페이스 (Reversed) */}
            <YAxis 
              yAxisId="right" 
              orientation="right" 
              domain={['dataMin - 0.5', 'dataMax + 0.5']} 
              reversed={true} // 페이스는 낮을수록 빠르므로 뒤집음
              stroke="#3b82f6"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(val: number) => formatPace(val)}
              label={{ value: 'Pace', angle: 90, position: 'insideRight', fill: '#3b82f6', fontSize: 10 }}
            />

            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              labelFormatter={(val: number) => `${Math.floor(val / 60)} min`}
              formatter={(value: number, name: string) => {
                if (name === "Pace") return [formatPace(value), "Pace"];
                if (name === "Heart Rate") return [`${value} bpm`, "Heart Rate"];
                return [value, name];
              }}
            />
            
            <Legend verticalAlign="top" height={36} iconType="circle"/>

            {/* 심박수 영역 그래프 */}
            <Area
              yAxisId="left"
              type="monotone"
              dataKey="heart_rate"
              name="Heart Rate"
              stroke="#ef4444"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorHr)"
            />

            {/* 페이스 라인 그래프 */}
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="pace"
              name="Pace"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}