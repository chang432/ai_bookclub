import React from 'react';
import Post from "./Post";

const base_url = "http://127.0.0.1"; 

const posts = await fetch(base_url+"/data/posts.json").then(r => r.json()); // string[]

const PostList: React.FC = () => {
    return (
        <div className="space-y-4">
            {posts.map((post: {author: string, post: string}, index: number) => (
                <Post key={index} author={post.author} post={post.post} />
            ))}
        </div>
    );
};

export default PostList;