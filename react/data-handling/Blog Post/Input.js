import React from "react";

function Input({ title, description, setTitle, setDescription }) {
  return (
    <div className="layout-column justify-content-center align-items-center">
      <input
        className="w-100"
        type="text"
        placeholder="Enter Title"
        value={title}
        data-testid="title-input"
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        className="mt-10 w-100"
        placeholder="Enter Description"
        value={description}
        data-testid="description-input"
        onChange={(e) => setDescription(e.target.value)}
      />
    </div>
  );
}

export default Input;
