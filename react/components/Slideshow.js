import React, { useState } from "react";

function Slides({ slides }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const isFirstSlide = currentIndex === 0;
  const isLastSlide = currentIndex === slides.length - 1;

  const handleNext = () => {
    setCurrentIndex((prev) => prev + 1);
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => prev - 1);
  };

  const handleRestart = () => {
    setCurrentIndex(0);
  };

  return (
    <div>
      <div id="navigation" className="text-center">
        <button
          data-testid="button-restart"
          className="small outlined"
          onClick={handleRestart}
          disabled={isFirstSlide}
        >
          Restart
        </button>

        <button
          data-testid="button-prev"
          className="small"
          onClick={handlePrev}
          disabled={isFirstSlide}
        >
          Prev
        </button>

        <button
          data-testid="button-next"
          className="small"
          onClick={handleNext}
          disabled={isLastSlide}
        >
          Next
        </button>
      </div>

      <div id="slide" className="card text-center">
        <h1 data-testid="title">{slides[currentIndex].title}</h1>
        <p data-testid="text">{slides[currentIndex].text}</p>
      </div>
    </div>
  );
}

export default Slides;
