"use client";

import { useEffect, useState } from 'react';
import { getInsights } from '@/lib/api';
import { Lightbulb, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';

export default function InsightsPage() {
    const [youtubeInsights, setYoutubeInsights] = useState<any[]>([]);
    const [adsInsights, setAdsInsights] = useState<any[]>([]);
    const [bankingInsights, setBankingInsights] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const yt = await getInsights('youtube');
                setYoutubeInsights(yt);
            } catch (e) { console.log("YouTube data not found"); }

            try {
                const ad = await getInsights('ads');
                setAdsInsights(ad);
            } catch (e) { console.log("Ads data not found"); }

            try {
                const bk = await getInsights('banking');
                setBankingInsights(bk);
            } catch (e) { console.log("Banking data not found"); }

            setLoading(false);
        };

        fetchData();
    }, []);

    if (loading) return <div className="p-8 text-center">Loading insights...</div>;

    const InsightCard = ({ category, insight, color }: any) => (
        <div className={`bg-white p-6 rounded-xl shadow-sm border-l-4 ${color} mb-4`}>
            <div className="flex items-start gap-4">
                <div className={`p-2 rounded-full ${color.replace('border-', 'bg-').replace('500', '100')} text-${color.replace('border-', '').replace('500', '600')}`}>
                    <Lightbulb size={20} />
                </div>
                <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1 block">{category}</span>
                    <p className="text-gray-800 font-medium text-lg">{insight}</p>
                </div>
            </div>
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-2">Business Insights</h1>
            <p className="text-gray-600 mb-10">Automated insights generated from your data patterns.</p>

            {youtubeInsights.length > 0 && (
                <div className="mb-10">
                    <h2 className="text-xl font-bold mb-4 text-red-600 flex items-center gap-2">
                        <TrendingUp size={24} /> YouTube Strategy
                    </h2>
                    {youtubeInsights.map((item, idx) => (
                        <InsightCard key={idx} category={item.category} insight={item.insight} color="border-red-500" />
                    ))}
                </div>
            )}

            {adsInsights.length > 0 && (
                <div className="mb-10">
                    <h2 className="text-xl font-bold mb-4 text-blue-600 flex items-center gap-2">
                        <CheckCircle size={24} /> Ad Optimization
                    </h2>
                    {adsInsights.map((item, idx) => (
                        <InsightCard key={idx} category={item.category} insight={item.insight} color="border-blue-500" />
                    ))}
                </div>
            )}

            {bankingInsights.length > 0 && (
                <div className="mb-10">
                    <h2 className="text-xl font-bold mb-4 text-green-600 flex items-center gap-2">
                        <AlertTriangle size={24} /> Banking Risk & Retention
                    </h2>
                    {bankingInsights.map((item, idx) => (
                        <InsightCard key={idx} category={item.category} insight={item.insight} color="border-green-500" />
                    ))}
                </div>
            )}

            {youtubeInsights.length === 0 && adsInsights.length === 0 && bankingInsights.length === 0 && (
                <div className="text-center py-20 bg-gray-50 rounded-xl border border-dashed border-gray-300">
                    <h3 className="text-xl font-medium text-gray-500 mb-2">No Insights Available</h3>
                    <p className="text-gray-400">Upload data to generate insights.</p>
                </div>
            )}
        </div>
    );
}
