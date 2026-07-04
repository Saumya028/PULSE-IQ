import Navbar from "@/components/Navbar";
import SearchBox from "@/components/SearchBox";

export default function Home() {
  return (
    <>
      <Navbar />

      <main className="flex flex-col items-center justify-center px-8 py-20">

        <h1 className="text-6xl font-bold text-center">
          AI Powered Industry Intelligence
        </h1>

        <p className="text-slate-400 mt-6 text-xl text-center max-w-3xl">
          Search any industry and generate an AI-powered executive intelligence dashboard in seconds.
        </p>

        <SearchBox />

        <div className="mt-16">

          <p className="text-slate-500 text-center mb-5">
            Popular Industries
          </p>

          <div className="flex flex-wrap justify-center gap-3">

            {[
              "FMCG",
              "Banking",
              "Retail",
              "Healthcare",
              "Technology",
              "Packaging Printing",
            ].map((item) => (
              <div
                key={item}
                className="
                  bg-slate-800
                  border
                  border-slate-700
                  rounded-full
                  px-5
                  py-2
                  hover:border-blue-500
                  cursor-pointer
                  transition
                "
              >
                {item}
              </div>
            ))}

          </div>

        </div>

      </main>
    </>
  );
}