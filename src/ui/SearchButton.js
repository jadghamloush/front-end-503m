import React, { useState } from "react";
import styled from "styled-components";

export const SearchButton = ({ icon, label, onClick, expandable }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [inputText, setInputText] = useState("");

  const handleExpand = () => {
    setIsExpanded(true);
  };

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleCollapse = () => {
    setIsExpanded(false);
    setInputText(""); // Clear input when collapsed
  };

  return (
    <Container>
      <StyledButton
        onClick={onClick}
        onMouseEnter={expandable ? handleExpand : null}
        onMouseLeave={expandable ? handleCollapse : null}
        isExpanded={isExpanded}
      >
        <IconWrapper>{icon}</IconWrapper>
        {isExpanded && (
          <InputWrapper>
            <Input
              type="text"
              value={inputText}
              onChange={handleInputChange}
              placeholder={label}
            />
          </InputWrapper>
        )}
      </StyledButton>
    </Container>
  );
};

const Container = styled.div`
  display: inline-block;
`;

const StyledButton = styled.button`
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  padding: 0.5rem;
  border-radius: 5px;
  transition: width 0.3s ease, background-color 0.3s ease;
  overflow: hidden;
  width: ${({ isExpanded }) =>
    isExpanded ? "10rem" : "2.5rem"}; /* Wider width on hover */

  &:hover {
    background-color: rgba(255, 255, 255, 0.4);
  }

  &:focus {
    outline: none;
  }
`;

const IconWrapper = styled.span`
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
`;

const InputWrapper = styled.div`
  margin-left: 0.5rem;
  flex-grow: 1;
`;

const Input = styled.input`
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  width: 100%;
  outline: none;

  &::placeholder {
    color: #ddd;
  }
`;
