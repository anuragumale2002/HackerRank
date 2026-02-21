import React, { useState } from "react";

const aspects = [
  "Readability",
  "Performance",
  "Security",
  "Documentation",
  "Testing",
];

const FeedbackSystem = () => {
  const [votes, setVotes] = useState(
    aspects.map(() => ({ upvotes: 0, downvotes: 0 }))
  );

  const handleUpvote = (index) => {
    const updatedVotes = [...votes];
    updatedVotes[index].upvotes += 1;
    setVotes(updatedVotes);
  };

  const handleDownvote = (index) => {
    const updatedVotes = [...votes];
    updatedVotes[index].downvotes += 1;
    setVotes(updatedVotes);
  };

  return (
    <div className="my-0 mx-auto text-center w-mx-1200">
      <div className="flex wrap justify-content-center mt-30 gap-30">
        {aspects.map((aspect, index) => (
          <div key={aspect} className="pa-10 w-300 card">
            <h2>{aspect}</h2>

            <div className="flex my-30 mx-0 justify-content-around">
              <button
                className="py-10 px-15"
                data-testid={`upvote-btn-${index}`}
                onClick={() => handleUpvote(index)}
              >
                👍 Upvote
              </button>

              <button
                className="py-10 px-15 danger"
                data-testid={`downvote-btn-${index}`}
                onClick={() => handleDownvote(index)}
              >
                👎 Downvote
              </button>
            </div>

            <p
              className="my-10 mx-0"
              data-testid={`upvote-count-${index}`}
            >
              Upvotes: <strong>{votes[index].upvotes}</strong>
            </p>

            <p
              className="my-10 mx-0"
              data-testid={`downvote-count-${index}`}
            >
              Downvotes: <strong>{votes[index].downvotes}</strong>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FeedbackSystem;
