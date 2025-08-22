import { useEffect, useMemo, useState } from "react";

interface BookProps {
    title: string;
    author: string;
}

// Eagerly import all .txt files as raw strings
const files = import.meta.glob<string>("../texts/*.txt", { query: "?raw", import: 'default', eager: true }) as Record<string, string>;
// Sort by path to get stable order
const ENTRIES = Object.entries(files).sort(([a], [b]) => a.localeCompare(b));

const first_page_number = Number(ENTRIES[0]?.[0].replace("../texts/", "").replace(".txt", ""));

const Book: React.FC<BookProps> = ({ title, author }) => {
    const [index, setIndex] = useState(0);
    
    const clamp = (i: number) => Math.max(0, Math.min(ENTRIES.length - 1, i));
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

    const [path, rawContent] = ENTRIES[index] ?? ["", ""];

    const maxPageNumber = useMemo(() => first_page_number + ENTRIES.length - 1, [first_page_number, ENTRIES]);

    const content = useMemo(() => {
        return rawContent.replace(/\r?\n/g, " ").trim();
    },[rawContent]);

    const pageLabel = useMemo(
        () => `${first_page_number + index} / ${maxPageNumber}`,
        [index]
    );

    return (
        <div className="flex flex-col text-xl mx-auto max-w-3xl">
            <div>
                <p>{title}</p>
                <p>by {author}</p>
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
                    disabled={index === ENTRIES.length - 1}
                >▶</button>
            </div>
        </div>
    );
};

export default Book;