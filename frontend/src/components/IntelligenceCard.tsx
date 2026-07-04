type Props = {
    headline?: string;
    summary?: string;
    category?: string;
    priority?: string;
    company?: string;
    country?: string;
    score?: number;

    source?: string;
    url?: string;
    published_at?: string;
};

export default function IntelligenceCard({
    headline = "No headline",
    summary = "No summary available.",
    category = "General",
    priority = "Medium",
    company = "Unknown",
    country = "Unknown",
    score = 0,

    source = "Unknown Source",
    url = "#",
    published_at,
}: Props) {
    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">

            <div className="flex justify-between">
                <span className="text-blue-400 text-sm">
                    {category}
                </span>

                <span className="text-green-400 text-sm">
                    Score {score}
                </span>
            </div>

            <h3 className="text-xl font-semibold mt-3">
                {headline}
            </h3>

            <p className="text-slate-300 mt-3">
                {summary}
            </p>

            <div className="flex gap-4 mt-5 text-sm text-slate-400">
                <span>{company}</span>
                <span>{country}</span>
                <span>{priority}</span>
            </div>

            <div className="mt-6 flex flex-wrap items-center gap-6 text-sm text-slate-400">

                <span>
                    📰 {source}
                </span>

                <span>
                    📅 {published_at
                        ? new Date(published_at).toLocaleDateString()
                        : "Unknown Date"}
                </span>

                <a
                    href={url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 underline"
                >
                    Read Full Article →
                </a>

            </div>

        </div>
    );
}