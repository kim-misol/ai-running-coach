import { CoachFeedback } from "@/lib/types"; 
import { Brain, TrendingUp, AlertCircle, CheckCircle2 } from "lucide-react";

export function AIReport({ data }: { data: CoachFeedback }) { return ( <div className="space-y-6"> <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-lg relative overflow-hidden"> <h3 className="text-lg font-semibold mb-2 flex items-center gap-2"> <Brain className="text-blue-400" size={20}/> AI Running Coach Analysis </h3> <p className="text-slate-200 leading-relaxed text-lg">{data.summary}</p> </div>

  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div className="rounded-xl border bg-white p-6 shadow-sm">
       <h4 className="font-semibold mb-4 text-gray-800">Performance Breakdown</h4>
       <div className="space-y-4">
         <div>
           <p className="text-sm font-medium text-green-600 mb-2 flex items-center gap-1">
             <CheckCircle2 size={16}/> Good Points
           </p>
           <ul className="list-disc list-inside text-sm text-gray-600 space-y-1 bg-green-50 p-3 rounded-lg">
             {data.strength.map((s, i) => <li key={i}>{s}</li>)}
           </ul>
         </div>
         <div>
           <p className="text-sm font-medium text-red-600 mb-2 flex items-center gap-1">
             <AlertCircle size={16}/> Improvement Needed
           </p>
           <ul className="list-disc list-inside text-sm text-gray-600 space-y-1 bg-red-50 p-3 rounded-lg">
             {data.weakness.map((w, i) => <li key={i}>{w}</li>)}
           </ul>
         </div>
       </div>
    </div>

    <div className="rounded-xl border bg-white p-6 shadow-sm flex flex-col">
      <h4 className="font-semibold mb-4 text-gray-800 flex items-center gap-2">
        <TrendingUp size={18} /> Race Predictions
      </h4>
      <div className="flex-1 space-y-3">
         {data.race_predictions.map((race) => (
           <div key={race.distance_km} className="flex justify-between items-center p-3 border rounded-lg hover:bg-slate-50 transition-colors">
             <span className="font-medium text-slate-700">{race.distance_km}K</span>
             <div className="text-right">
               <div className="font-bold text-slate-900">{race.predicted_time_str}</div>
               <div className="text-xs text-slate-400">Conf: {Math.round(race.confidence_score * 100)}%</div>
             </div>
           </div>
         ))}
      </div>
      <div className="mt-4 pt-4 border-t">
         <p className="text-xs font-semibold text-slate-500 uppercase mb-1">Coach Suggestion</p>
         <p className="text-sm text-blue-700 font-medium">{data.suggested_workout}</p>
      </div>
    </div>
  </div>
</div>

); }