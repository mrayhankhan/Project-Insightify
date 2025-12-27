"use client";

import { useEffect, useState } from 'react';
import { getKPIs, getPreview, getSegmentation, getInsights } from '@/lib/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, ScatterChart, Scatter, ZAxis } from 'recharts';
import { Users, DollarSign, Eye, MousePointer, Activity, TrendingUp, Lightbulb, Target } from 'lucide-react';

export default function DashboardPage() {
    const [youtubeKPIs, setYoutubeKPIs] = useState<any>(null);
    const [adsKPIs, setAdsKPIs] = useState<any>(null);
    const [bankingKPIs, setBankingKPIs] = useState<any>(null);
    const [youtubeData, setYoutubeData] = useState<any[]>([]);
    const [adsData, setAdsData] = useState<any[]>([]);

    const [segmentationData, setSegmentationData] = useState<any>(null);
    const [insightsData, setInsightsData] = useState<any[]>([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const ytKPIs = await getKPIs('youtube');
                setYoutubeKPIs(ytKPIs);
                const ytData = await getPreview('youtube');
                setYoutubeData(ytData);
            } catch (e) { console.log("YouTube data not found"); }

            try {
                const adKPIs = await getKPIs('ads');
                setAdsKPIs(adKPIs);
                const adData = await getPreview('ads');
                setAdsData(adData);
            } catch (e) { console.log("Ads data not found"); }

            try {
                const bkKPIs = await getKPIs('banking');
                setBankingKPIs(bkKPIs);
            } catch (e) { console.log("Banking data not found"); }

            // Fetch Segmentation and Insights for the first available dataset (prioritizing Banking > Ads > YouTube for demo)
            try {
                let type = 'youtube';
                if (await getKPIs('banking').then(() => true).catch(() => false)) type = 'banking';
                else if (await getKPIs('ads').then(() => true).catch(() => false)) type = 'ads';

                const seg = await getSegmentation(type);
                setSegmentationData(seg);
                const ins = await getInsights(type);
                setInsightsData(ins);
            } catch (e) { console.log("Segmentation/Insights error", e); }

            setLoading(false);
        };

        fetchData();
    }, []);

    if (loading) return <div className="p-8 text-center">Loading dashboard...</div>;

    const KPICard = ({ title, value, icon: Icon, color }: any) => (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <p className="text-gray-500 text-sm font-medium">{title}</p>
                    <h3 className="text-2xl font-bold mt-1">{value}</h3>
                </div>
                <div className={`p-3 rounded-lg ${color}`}>
                    <Icon size={20} className="text-white" />
                </div>
            </div>
        </div>
    );

    return (
        <div className="space-y-12">
            <div>
                <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

                {/* YouTube Section */}
                {youtubeKPIs && (
                    <div className="mb-12">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <span className="w-2 h-8 bg-red-600 rounded-full"></span> YouTube Analytics
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                            <KPICard title="Total Views" value={youtubeKPIs.total_views.toLocaleString()} icon={Eye} color="bg-red-500" />
                            <KPICard title="Avg Engagement Rate" value={(youtubeKPIs.avg_engagement_rate * 100).toFixed(2) + '%'} icon={Activity} color="bg-red-500" />
                            <KPICard title="Top Category" value={youtubeKPIs.top_category} icon={TrendingUp} color="bg-red-500" />
                        </div>

                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-[400px]">
                            <h3 className="text-lg font-semibold mb-4">Views vs Likes (Sample)</h3>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={youtubeData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="video_id" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="views" fill="#ef4444" name="Views" />
                                    <Bar dataKey="likes" fill="#3b82f6" name="Likes" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                )}

                {/* Ads Section */}
                {adsKPIs && (
                    <div className="mb-12">
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <span className="w-2 h-8 bg-blue-600 rounded-full"></span> Ads Performance
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                            <KPICard title="Impressions" value={adsKPIs.total_impressions.toLocaleString()} icon={Eye} color="bg-blue-500" />
                            <KPICard title="CTR" value={(adsKPIs.avg_ctr * 100).toFixed(2) + '%'} icon={MousePointer} color="bg-blue-500" />
                            <KPICard title="Conversion Rate" value={(adsKPIs.avg_conversion_rate * 100).toFixed(2) + '%'} icon={Activity} color="bg-blue-500" />
                            <KPICard title="Total Cost" value={'$' + adsKPIs.total_cost.toLocaleString()} icon={DollarSign} color="bg-blue-500" />
                        </div>

                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-[400px]">
                            <h3 className="text-lg font-semibold mb-4">Cost vs Conversions (Sample)</h3>
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={adsData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="campaign_id" />
                                    <YAxis yAxisId="left" />
                                    <YAxis yAxisId="right" orientation="right" />
                                    <Tooltip />
                                    <Legend />
                                    <Line yAxisId="left" type="monotone" dataKey="cost" stroke="#3b82f6" name="Cost ($)" />
                                    <Line yAxisId="right" type="monotone" dataKey="conversions" stroke="#10b981" name="Conversions" />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                )}

                {/* Banking Section */}
                {bankingKPIs && (
                    <div>
                        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                            <span className="w-2 h-8 bg-green-600 rounded-full"></span> Banking Analytics
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <KPICard title="Avg Balance" value={'$' + bankingKPIs.avg_balance.toFixed(2)} icon={DollarSign} color="bg-green-500" />
                            <KPICard title="Churn Rate" value={(bankingKPIs.churn_rate * 100).toFixed(2) + '%'} icon={Users} color="bg-green-500" />
                            <KPICard title="Avg Products" value={bankingKPIs.avg_products.toFixed(1)} icon={Activity} color="bg-green-500" />
                        </div>
                    </div>
                )}

                {/* Segmentation & Insights Section */}
                {(segmentationData || insightsData.length > 0) && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Segmentation Chart */}
                        {segmentationData && (
                            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-[500px]">
                                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                    <Target className="text-purple-600" /> Customer Segmentation
                                </h2>
                                <p className="text-sm text-gray-500 mb-4">AI-driven clustering of your audience/customers.</p>
                                <ResponsiveContainer width="100%" height="85%">
                                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                        <CartesianGrid />
                                        <XAxis type="number" dataKey="x" name="PC1" unit="" />
                                        <YAxis type="number" dataKey="y" name="PC2" unit="" />
                                        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                        <Legend />
                                        {segmentationData.clusters.map((cluster: any, index: number) => (
                                            <Scatter
                                                key={cluster.cluster_id}
                                                name={`Cluster ${cluster.cluster_id}`}
                                                data={cluster.points}
                                                fill={['#8884d8', '#82ca9d', '#ffc658'][index % 3]}
                                            />
                                        ))}
                                    </ScatterChart>
                                </ResponsiveContainer>
                            </div>
                        )}

                        {/* Insights List */}
                        {insightsData.length > 0 && (
                            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                                <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                                    <Lightbulb className="text-yellow-500" /> Actionable Insights
                                </h2>
                                <div className="space-y-4">
                                    {insightsData.map((insight: any, index: number) => (
                                        <div key={index} className="p-4 rounded-lg border border-gray-100 bg-gray-50 hover:bg-white hover:shadow-md transition">
                                            <div className="flex justify-between items-start mb-2">
                                                <span className="text-xs font-semibold uppercase tracking-wider text-gray-500 bg-gray-200 px-2 py-1 rounded">
                                                    {insight.category}
                                                </span>
                                                <span className={`text-xs font-bold px-2 py-1 rounded ${insight.impact === 'High' ? 'bg-red-100 text-red-600' :
                                                    insight.impact === 'Medium' ? 'bg-yellow-100 text-yellow-600' :
                                                        'bg-blue-100 text-blue-600'
                                                    }`}>
                                                    {insight.impact} Impact
                                                </span>
                                            </div>
                                            <p className="text-gray-800 font-medium">{insight.insight}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {!youtubeKPIs && !adsKPIs && !bankingKPIs && (
                    <div className="text-center py-20 bg-gray-50 rounded-xl border border-dashed border-gray-300">
                        <h3 className="text-xl font-medium text-gray-500 mb-2">No Data Available</h3>
                        <p className="text-gray-400">Please upload datasets to view the dashboard.</p>
                    </div>
                )}
            </div>

        </div>
    );
}
