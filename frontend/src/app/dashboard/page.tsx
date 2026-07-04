"use client";

import { useEffect, useState } from "react";

import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import KPISection from "@/components/KPISection";
import ExecutiveSummary from "@/components/ExecutiveSummary";
import IntelligenceCard from "@/components/IntelligenceCard";

import { getDashboard } from "@/services/dashboard";

export default function Dashboard() {

    const [articles, setArticles] = useState([]);

    useEffect(() => {

        loadDashboard();

    }, []);

    async function loadDashboard() {

        try {

            const data = await getDashboard();

            setArticles(data);

        }

        catch (err) {

            console.log(err);

        }

    }

    return (

        <div className="min-h-screen bg-slate-950 text-white">

            <Navbar />

            <div className="flex">

                <Sidebar />

                <main className="flex-1 p-8">

                    <KPISection />

                    <div className="mt-8">

                        <ExecutiveSummary />

                    </div>

                    <div className="mt-8 space-y-6">

                        {

                            articles.map((article: any) => (

                                <IntelligenceCard

                                    key={article.id}

                                    headline={article.headline}

                                    summary={article.summary}

                                    company={article.company}

                                    country={article.country}

                                    priority={article.priority}

                                    category={article.category}

                                    score={article.dashboard_score}
                                    source={article.source}
                                    url={article.url}
                                    published_at={article.published_at}

                                />

                            ))

                        }

                    </div>

                </main>

            </div>

        </div>

    );

}