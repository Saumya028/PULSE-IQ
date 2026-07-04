"use client";

export default function LoadingScreen() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-[#0F172A]">

            <div className="w-20 h-20 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>

            <h2 className="mt-8 text-3xl font-bold">
                Generating Intelligence...
            </h2>

            <p className="mt-3 text-slate-400">
                Fetching news, filtering articles and generating executive insights.
            </p>

        </div>
    );
}