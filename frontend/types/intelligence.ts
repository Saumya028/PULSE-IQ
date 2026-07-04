export interface Intelligence {
    id: number;

    headline: string;
    summary: string;

    company: string;
    country: string;

    category: string;
    priority: string;

    dashboard_score: number;

    business_impact: string;
    recommended_action: string;

    source: string;          // <-- add if missing
    url: string;             // <-- add if missing
    published_at: string;    // <-- add if missing
}