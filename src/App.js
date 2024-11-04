import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import { Title } from "./ui/Title";
import styled, { keyframes } from "styled-components";
import Profile from "./components/Profile";
import Login from "./components/Login";
import SignUp from "./components/SignUp";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

const images = ["/image1.jpg", "/image2.jpg", "/image3.jpg"];

const App = () => {
  const [currentImage, setCurrentImage] = useState(0);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImage((prev) => (prev + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <AppContainer>
        <BackgroundImage
          style={{ backgroundImage: `url(${images[currentImage]})` }}
        />
        <Title /> {/* Title component with higher z-index */}
        <NavbarContainer>
          <Navbar isLoggedIn={isLoggedIn} />
        </NavbarContainer>
        <Content>
          <Routes>
            <Route path="/profile" element={<Profile />} />
            <Route
              path="/login"
              element={<Login setIsLoggedIn={setIsLoggedIn} />}
            />
            <Route
              path="/signup"
              element={<SignUp setIsLoggedIn={setIsLoggedIn} />}
            />
          </Routes>
        </Content>
      </AppContainer>
    </Router>
  );
};

export default App;

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const AppContainer = styled.div`
  position: relative;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
`;

const BackgroundImage = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-size: cover;
  background-position: center;
  transition: background-image 0.5s ease-in-out;
  z-index: -1;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
    z-index: -1;
  }
`;

const NavbarContainer = styled.div`
  position: relative;
  z-index: 2;
  width: 100%;
`;

const Content = styled.div`
  position: relative;
  z-index: 1;
  padding: 2rem;
  animation: ${fadeIn} 0.5s ease-in-out;
  overflow: auto;
`;
