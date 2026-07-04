"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";

export default function ExecutiveSummary() {

    const [brief, setBrief] = useState<any>(null);

    useEffect(() => {

        api
            .get("/brief/FMCG")
            .then((res) => setBrief(res.data))
            .catch(console.error);

    }, []);

    if (!brief) {

        return (

            <div className="bg-slate-900 rounded-xl p-8">

                <h2 className="text-3xl font-bold mb-4">
                    Executive Brief
                </h2>

                <p className="text-slate-400">
                    Loading executive brief...
                </p>

            </div>

        );

    }

    return (

        <div className="bg-slate-900 rounded-xl p-8">

            <h2 className="text-3xl font-bold mb-2">
                Executive Brief
            </h2>

            <h3 className="text-xl font-semibold text-blue-400 mb-5">
                {brief.headline}
            </h3>

            <p className="text-slate-300 leading-8 whitespace-pre-wrap">
                {brief.summary}
            </p>

            {/* Add this section BELOW the summary */}

            <div className="mt-8">

                <h3 className="text-xl font-bold mb-3">
                    Key Trends
                </h3>

                <ul className="space-y-2">

                    {brief.key_trends.split("\n").map((trend: string, index: number) => (

                        <li key={index}>
                            • {trend}
                        </li>

                    ))}

                </ul>

            </div>

            <div className="mt-8">

                <h3 className="text-xl font-bold mb-3">
                    Recommended Actions
                </h3>

                <ul className="space-y-2">

                    {brief.recommended_actions.split("\n").map((action: string, index: number) => (

                        <li key={index}>
                            • {action}
                        </li>

                    ))}

                </ul>

            </div>

        </div>

    );

}