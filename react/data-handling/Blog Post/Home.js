import React, { useState } from "react";
import Input from "./Input";
import PostDisplay from "./PostDisplay";

function Home() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [posts, setPosts] = useState([]);

  const handleCreate = () => {
    if (!title.trim() || !description.trim()) return;

    const newPost = { title, description };

    setPosts([...posts, newPost]);
    setTitle("");
    setDescription("");
  };

  const handleDelete = (indexToDelete) => {
    setPosts(posts.filter((_, index) => index !== indexToDelete));
  };

  return (
    <div className="text-center ma-20">
      <div className="mb-20">
        <Input
          title={title}
          description={description}
          setTitle={setTitle}
          setDescription={setDescription}
        />
        <button
          data-testid="create-button"
          className="mt-10"
          onClick={handleCreate}
        >
          Create Post
        </button>
      </div>

      <div className="posts-section">
        <PostDisplay posts={posts} onDelete={handleDelete} />
      </div>
    </div>
  );
}

export default Home;
