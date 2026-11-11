import SearchForm from "@/components/SearchForm";

const STEPS = [
  {
    title: "Understand your request",
    text: "Your words become a 384-number embedding from a sentence-transformer fine-tuned on restaurant reviews.",
  },
  {
    title: "Read reviews by aspect",
    text: "Every review sentence is tagged as food, service, ambience, price, noise or wait time, and scored positive or negative.",
  },
  {
    title: "Match and rank",
    text: "Restaurants are ranked by how closely reviews match you, how well each aspect fits, and a weighted star rating.",
  },
  {
    title: "Explain the pick",
    text: "A language model writes two sentences on why each place fits, based on the reviews it relied on.",
  },
];

export default function Home() {
  return (
    <>
      <section className="bg-white">
        <div className="mx-auto max-w-6xl px-6 pb-14 pt-16 md:pt-20">
          <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-accent">
            Restaurant recommendations from what reviewers actually say
          </p>
          <h1 className="max-w-4xl font-display text-4xl font-bold leading-[1.04] tracking-tight md:text-6xl">
            Describe the meal you want. We read the reviews for you.
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-muted md:text-xl">
            A 4-star average can hide great food and slow service. TasteLens scores food, service,
            ambience, price, noise and wait time separately, then matches them to your request.
          </p>
          <div className="mt-10">
            <SearchForm />
          </div>
        </div>
      </section>

      <section id="how" className="bg-ink text-white">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <h2 className="font-display text-4xl font-bold tracking-tight">
            How a recommendation is made
          </h2>
          <p className="mb-10 mt-3 max-w-2xl text-lg text-[#c9ccd1]">
            Four NLP steps run between your sentence and the ranked list.
          </p>
          <ol className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {STEPS.map((step, i) => (
              <li key={step.title} className="rounded-2xl border border-[#3a3e45] p-6">
                <p className="font-display text-5xl font-bold text-accent-light">0{i + 1}</p>
                <h3 className="my-2 text-lg font-semibold">{step.title}</h3>
                <p className="text-[#c9ccd1]">{step.text}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section id="about" className="mx-auto flex max-w-6xl flex-wrap gap-10 px-6 py-16">
        <div className="min-w-0 flex-[1_1_420px]">
          <h2 className="mb-3 font-display text-3xl font-bold tracking-tight">About the data</h2>
          <p className="text-lg text-muted">
            Recommendations come from the Yelp Open Dataset, used for educational purposes.
            Reviews are cleaned (duplicates, very short and pre-2015 reviews removed), and only
            restaurants with at least 15 reviews are ranked.
          </p>
        </div>
        <dl className="grid flex-[1_1_320px] grid-cols-2 items-start gap-4">
          <div className="flex flex-col rounded-2xl bg-white p-5">
            <dt className="text-sm text-muted">restaurant reviews ingested</dt>
            <dd className="order-first font-display text-3xl font-bold">687k</dd>
          </div>
          <div className="flex flex-col rounded-2xl bg-white p-5">
            <dt className="text-sm text-muted">aspects scored per review</dt>
            <dd className="order-first font-display text-3xl font-bold">6</dd>
          </div>
        </dl>
      </section>
    </>
  );
}
