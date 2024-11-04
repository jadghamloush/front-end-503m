import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";

// Importing a Google Font (e.g., Pacifico)
export const Title = () => {
  return (
    <StyledLink to="/">
      <TitleContainer>Sportify</TitleContainer>;
    </StyledLink>
  );
};

const TitleContainer = styled.div`
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 3rem;
  font-weight: bold;
  color: white;
  font-family: "Pacifico", cursive;
  text-transform: uppercase;
  letter-spacing: 2px;
  z-index: 2;
  &:hover {
    color: #1e90ff; /* Electric blue hover effect */
  }
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  position: absolute;
  top: 1rem;
  left: 1rem;
  z-index: 3; /* Ensure it is above other elements */
`;
