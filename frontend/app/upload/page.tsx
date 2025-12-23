"use client";

import { useState } from 'react';
import { uploadDataset } from '@/lib/api';
import { Upload, CheckCircle, AlertCircle } from 'lucide-react';

export default function UploadPage() {
    const [status, setStatus] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState<Record<string, boolean>>({});

    const handleUpload = async (type: string, e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files?.[0]) return;

        const file = e.target.files[0];
        setLoading(prev => ({ ...prev, [type]: true }));
        setStatus(prev => ({ ...prev, [type]: '' }));

        try {
            await uploadDataset(type, file);
            setStatus(prev => ({ ...prev, [type]: 'success' }));
        } catch (error) {
            console.error(error);
            setStatus(prev => ({ ...prev, [type]: 'error' }));
        } finally {
            setLoading(prev => ({ ...prev, [type]: false }));
        }
    };

    const UploadCard = ({ title, type, description }: { title: string, type: string, description: string }) => (
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
            <h3 className="text-xl font-semibold mb-2">{title}</h3>
            <p className="text-gray-500 mb-4 text-sm">{description}</p>

            <div className="flex items-center gap-4">
                <label className="cursor-pointer bg-blue-50 text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-100 transition flex items-center gap-2">
                    <Upload size={18} />
                    Choose File
                    <input
                        type="file"
                        accept=".csv"
                        className="hidden"
                        onChange={(e) => handleUpload(type, e)}
                        disabled={loading[type]}
                    />
                </label>

                {loading[type] && <span className="text-gray-500 text-sm animate-pulse">Uploading...</span>}
                {status[type] === 'success' && <span className="text-green-600 flex items-center gap-1 text-sm"><CheckCircle size={16} /> Uploaded</span>}
                {status[type] === 'error' && <span className="text-red-600 flex items-center gap-1 text-sm"><AlertCircle size={16} /> Failed</span>}
            </div>
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-2">Upload Datasets</h1>
            <p className="text-gray-600 mb-8">Upload your CSV files to start analyzing.</p>

            <div className="grid gap-6">
                <UploadCard
                    title="YouTube Analytics"
                    type="youtube"
                    description="Upload CSV containing video views, likes, comments, and watch time."
                />
                <UploadCard
                    title="Ads Performance"
                    type="ads"
                    description="Upload CSV containing campaign impressions, clicks, conversions, and cost."
                />
                <UploadCard
                    title="Banking Customer Data"
                    type="banking"
                    description="Upload CSV containing customer balance, transactions, products, and churn flag."
                />
            </div>
        </div>
    );
}
