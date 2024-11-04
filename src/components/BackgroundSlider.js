import React, { useState, useEffect } from "react";
import styled from "styled-components";

const images = [
  "/images/image1.jpg",
  "/images/image2.jpg",
  "/images/image3.jpg",
];

const BackgroundSlider = () => {
  const [currentImage, setCurrentImage] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <BackgroundImage
      style={{ backgroundImage: `url(${images[currentImage]})` }}
    />
  );
};

export default BackgroundSlider;

const BackgroundImage = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-size: cover;
  background-position: center;
  transition: background-image 0.5s ease-in-out;
  z-index: -1;
`;
