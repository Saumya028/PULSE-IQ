"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/services/api";

export default function SearchBox() {

    const router = useRouter();

    const [industry, setIndustry] = useState("");

    const [loading, setLoading] = useState(false);

    async function analyzeIndustry() {

        if (!industry.trim()) return;

        try {

            setLoading(true);

            await api.post("/industry/search", {
                industry,
            });

            router.push(
                `/dashboard?industry=${encodeURIComponent(industry)}`
            );

        } catch (err) {

            console.error(err);

            alert("Backend Error");

        } finally {

            setLoading(false);

        }

    }

    return (

        <div className="w-full max-w-3xl mx-auto mt-12">

            <input
                type="text"
                placeholder="Enter Industry (e.g. FMCG)"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl p-4 text-lg outline-none focus:border-blue-500"
            />

            <button
                onClick={analyzeIndustry}
                disabled={loading}
                className="mt-6 w-full bg-blue-600 hover:bg-blue-700 rounded-xl py-4 text-lg font-semibold"
            >
                {loading ? "Analyzing..." : "Analyze Industry"}
            </button>

        </div>

    );
}