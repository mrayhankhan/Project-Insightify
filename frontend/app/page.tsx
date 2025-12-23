import Link from 'next/link';
import { ArrowRight, Upload, BarChart2, Users } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
        Unified Business Analytics
      </h1>
      <p className="text-xl text-gray-600 mb-10 max-w-2xl">
        Insightify brings together YouTube, Advertising, and Banking data into one powerful dashboard.
        Upload your data, visualize trends, and unlock actionable insights.
      </p>

      <div className="flex gap-4 mb-16">
        <Link href="/upload" className="bg-blue-600 text-white px-8 py-3 rounded-full font-semibold hover:bg-blue-700 transition flex items-center gap-2">
          Get Started <ArrowRight size={20} />
        </Link>
        <Link href="/dashboard" className="bg-white text-gray-800 border border-gray-300 px-8 py-3 rounded-full font-semibold hover:bg-gray-50 transition">
          View Demo
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl">
        <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
          <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4 mx-auto text-blue-600">
            <Upload size={24} />
          </div>
          <h3 className="text-xl font-semibold mb-2">Easy Upload</h3>
          <p className="text-gray-500">Simply drag and drop your CSV files to get started instantly.</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
          <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4 mx-auto text-purple-600">
            <BarChart2 size={24} />
          </div>
          <h3 className="text-xl font-semibold mb-2">Visual Analytics</h3>
          <p className="text-gray-500">Interactive charts and KPIs to track performance at a glance.</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
          <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4 mx-auto text-green-600">
            <Users size={24} />
          </div>
          <h3 className="text-xl font-semibold mb-2">Smart Segmentation</h3>
          <p className="text-gray-500">Group your customers and audience using advanced clustering.</p>
        </div>
      </div>
    </div>
  );
}
