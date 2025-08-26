import React from 'react';

interface PostProps {
    author: string;
    post: string;
}

const Post: React.FC<PostProps> = ({ author, post }) => {
    return (
        <div className="flex flex-col h-fit w-[36rem] border text-left p-4">
            <p className="mb-2 border rounded-full w-fit px-2">{author}</p>
            <p className="">{post}</p>
        </div>
    );
};

export default Post;