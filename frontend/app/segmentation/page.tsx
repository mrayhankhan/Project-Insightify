"use client";

import { useEffect, useState } from 'react';
import { getSegmentation } from '@/lib/api';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Users, Target, CreditCard } from 'lucide-react';

export default function SegmentationPage() {
    const [youtubeClusters, setYoutubeClusters] = useState<any>(null);
    const [adsClusters, setAdsClusters] = useState<any>(null);
    const [bankingClusters, setBankingClusters] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const yt = await getSegmentation('youtube');
                setYoutubeClusters(yt.clusters);
            } catch (e) { console.log("YouTube data not found"); }

            try {
                const ad = await getSegmentation('ads');
                setAdsClusters(ad.clusters);
            } catch (e) { console.log("Ads data not found"); }

            try {
                const bk = await getSegmentation('banking');
                setBankingClusters(bk.clusters);
            } catch (e) { console.log("Banking data not found"); }

            setLoading(false);
        };

        fetchData();
    }, []);

    if (loading) return <div className="p-8 text-center">Loading segmentation...</div>;

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    const ClusterSection = ({ title, clusters, icon: Icon, color }: any) => {
        if (!clusters) return null;

        const pieData = clusters.map((c: any) => ({ name: `Cluster ${c.cluster_id}`, value: c.size }));

        return (
            <div className="mb-16">
                <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                    <div className={`p-2 rounded-lg ${color} text-white`}>
                        <Icon size={24} />
                    </div>
                    {title} Segmentation
                </h2>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Pie Chart */}
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-[300px]">
                        <h3 className="text-lg font-semibold mb-4">Cluster Distribution</h3>
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {pieData.map((entry: any, index: number) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Cluster Details */}
                    <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-4">
                        {clusters.map((cluster: any, idx: number) => (
                            <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 relative overflow-hidden">
                                <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-${color.replace('bg-', '')}-500 to-transparent opacity-50`}></div>
                                <h3 className="text-lg font-bold mb-2 text-gray-800">Cluster {cluster.cluster_id}</h3>
                                <p className="text-sm text-gray-500 mb-4">{cluster.size} items</p>

                                <div className="space-y-2">
                                    {Object.entries(cluster.features).map(([feature, value]: [string, any]) => (
                                        <div key={feature} className="flex justify-between text-sm">
                                            <span className="text-gray-600 capitalize">{feature.replace(/_/g, ' ')}:</span>
                                            <span className="font-semibold">{typeof value === 'number' ? value.toFixed(1) : value}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div className="max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold mb-2">Customer & Audience Segmentation</h1>
            <p className="text-gray-600 mb-10">K-Means clustering analysis to identify distinct groups within your data.</p>

            <ClusterSection title="YouTube Viewers" clusters={youtubeClusters} icon={Users} color="bg-red-500" />
            <ClusterSection title="Ad Campaigns" clusters={adsClusters} icon={Target} color="bg-blue-500" />
            <ClusterSection title="Banking Customers" clusters={bankingClusters} icon={CreditCard} color="bg-green-500" />

            {!youtubeClusters && !adsClusters && !bankingClusters && (
                <div className="text-center py-20 bg-gray-50 rounded-xl border border-dashed border-gray-300">
                    <h3 className="text-xl font-medium text-gray-500 mb-2">No Segmentation Data</h3>
                    <p className="text-gray-400">Upload data to generate segments.</p>
                </div>
            )}
        </div>
    );
}
