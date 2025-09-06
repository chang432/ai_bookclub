import { useEffect, useMemo, useState } from "react";

const base_url = "http://localhost"; 

function getCurrentUTCDate(): string {
  const now = new Date();

  const month = String(now.getUTCMonth() + 1).padStart(2, "0"); // months are 0-based
  const day = String(now.getUTCDate()).padStart(2, "0");
  const year = now.getUTCFullYear();

  return `${month}/${day}/${year}`;
}

const files = await fetch(base_url+"/data/index.json").then(r => r.json()); // string[]
const book_info = await fetch(base_url+"/data/book_info.json").then(r => r.json()); 
// const current = await fetch(`${base_url}/data/${files[idx]}`).then(r => r.text());

// const files = import.meta.glob<string>("../data/*.txt", { query: "?raw", import: 'default', eager: true }) as Record<string, string>;

const first_page_number = Number(files[0].replace(".txt", ""));

const Book: React.FC = () => {
    const [index, setIndex] = useState(0);
    
    const clamp = (i: number) => Math.max(0, Math.min(files.length - 1, i));
    const prev = () => setIndex((i) => clamp(i - 1));
    const next = () => setIndex((i) => clamp(i + 1));

    useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
        if (e.key === "ArrowLeft") prev();
        if (e.key === "ArrowRight") next();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    }, []);

    const maxPageNumber = useMemo(() => first_page_number + files.length - 1, [first_page_number, files]);

    const [content, setContent] = useState("");

    useEffect(() => {
        const fetchContent = async () => {
            const current = await fetch(`${base_url}/data/${files[index]}`).then(r => r.text());
            setContent(current.replace(/\r?\n/g, " ").trim());
        };
        fetchContent();
    }, [index]);

    const pageLabel = useMemo(
        () => `${first_page_number + index} / ${maxPageNumber}`,
        [index]
    );

    return (
        <div className="flex flex-col text-xl mx-auto max-w-3xl">
            <div>
                <p className="text-red-500 mb-2">{getCurrentUTCDate()}</p>
                <p className="mb-2">{book_info["title_display"]} by {book_info["author"]}</p>
                <span className="text-sm text-gray-600">Page {pageLabel}</span>
            </div>
            <div className="flex flex-row space-x-5 mx-5 items-center">
                <button 
                    className="btn bg-amber-200 w-12 h-12 border flex items-center justify-center"
                    onClick={prev}
                    disabled={index === 0}
                >◀</button>
                <div className="rounded-2xl border bg-white p-4 text-center">
                    <p className="whitespace-pre-wrap wrap-break-word text-sm leading-relaxed tracking-[0.05em]">
                    {content}
                    </p>
                </div>
                <button 
                    className="btn bg-amber-200 w-12 h-12 border flex items-center justify-center"
                    onClick={next}
                    disabled={index === files.length - 1}
                >▶</button>
            </div>
        </div>
    );
};

export default Book;