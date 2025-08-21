import React from 'react';

interface BookProps {
    title: string;
    author: string;
}

const Book: React.FC<BookProps> = ({ title, author }) => {
    return (
        <div className="flex flex-col border text-xl">
            <div>
                <p>{title}</p>
                <p>by {author}</p>
            </div>
            <div className="flex flex-row space-x-5 mx-5 items-center">
                <button className="btn bg-amber-200 w-12 h-12 border flex items-center justify-center ">&lt;</button>
                <p className="w-96 h-[35rem] border">BOOK TEXT</p>
                <button className="btn bg-amber-200 w-12 h-12 border flex items-center justify-center">&gt;</button>
            </div>
        </div>
    );
};

export default Book;