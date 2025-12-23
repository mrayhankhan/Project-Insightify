import Link from 'next/link';
import { BarChart3, Upload, PieChart, Lightbulb, Home } from 'lucide-react';

const Navbar = () => {
    return (
        <nav className="bg-slate-900 text-white p-4 shadow-lg">
            <div className="container mx-auto flex justify-between items-center">
                <Link href="/" className="text-2xl font-bold flex items-center gap-2">
                    <BarChart3 className="text-blue-400" />
                    Insightify
                </Link>
                <div className="flex gap-6">
                    <Link href="/" className="flex items-center gap-1 hover:text-blue-300 transition">
                        <Home size={18} /> Home
                    </Link>
                    <Link href="/upload" className="flex items-center gap-1 hover:text-blue-300 transition">
                        <Upload size={18} /> Upload Data
                    </Link>
                    <Link href="/dashboard" className="flex items-center gap-1 hover:text-blue-300 transition">
                        <BarChart3 size={18} /> Dashboard
                    </Link>
                    <Link href="/segmentation" className="flex items-center gap-1 hover:text-blue-300 transition">
                        <PieChart size={18} /> Segmentation
                    </Link>
                    <Link href="/insights" className="flex items-center gap-1 hover:text-blue-300 transition">
                        <Lightbulb size={18} /> Insights
                    </Link>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
