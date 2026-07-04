export default function Sidebar() {

    return (

        <aside className="w-64 border-r border-slate-800 bg-slate-900 min-h-screen">

            <div className="p-6">

                <div className="space-y-4">

                    <button className="w-full text-left px-4 py-3 rounded-lg bg-blue-600">

                        Dashboard

                    </button>

                    <button className="w-full text-left px-4 py-3 hover:bg-slate-800 rounded-lg">

                        Executive Brief

                    </button>

                    <button className="w-full text-left px-4 py-3 hover:bg-slate-800 rounded-lg">

                        Intelligence Feed

                    </button>

                    <button className="w-full text-left px-4 py-3 hover:bg-slate-800 rounded-lg">

                        Analytics

                    </button>

                </div>

            </div>

        </aside>

    )

}