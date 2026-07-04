"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";

export default function KPICards() {

    const [stats, setStats] = useState<any>(null);

    useEffect(() => {

        api
            .get("/dashboard/stats")
            .then(res => setStats(res.data))
            .catch(console.error);

    }, []);

    if (!stats) {

        return (

            <div className="grid grid-cols-4 gap-6">

                {[1, 2, 3, 4].map(i => (

                    <div
                        key={i}
                        className="bg-slate-900 rounded-xl p-6 animate-pulse h-36"
                    />

                ))}

            </div>

        );

    }

    const cards = [

        {
            title: "Articles",
            value: stats.total_articles
        },

        {
            title: "Critical",
            value: stats.critical
        },

        {
            title: "High Priority",
            value: stats.high
        },

        {
            title: "Latest Update",
            value: stats.latest_update
                ? stats.latest_update.substring(5, 16)
                : "-"
        }

    ];

    return (

        <div className="grid grid-cols-4 gap-6">

            {cards.map(card => (

                <div
                    key={card.title}
                    className="bg-slate-900 rounded-xl p-6 border border-slate-800"
                >

                    <p className="text-slate-400">
                        {card.title}
                    </p>

                    <h2 className="text-5xl font-bold mt-4">

                        {card.value}

                    </h2>

                </div>

            ))}

        </div>

    );

}