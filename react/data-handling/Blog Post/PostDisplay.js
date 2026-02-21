import React from "react";

function PostDisplay({ posts = [], onDelete }) {
  return (
    <div data-testid="posts-container" className="flex wrap gap-10">
      {posts.map((post, index) => (
        <div key={index} className="post-box">
          <h3>{post.title}</h3>
          <p>{post.description}</p>
          <button onClick={() => onDelete(index)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}

export default PostDisplay;
