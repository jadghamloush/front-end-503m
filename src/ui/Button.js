import styled from "styled-components";

export const Button = ({ icon, label, onClick }) => {
  return (
    <StyledButton onClick={onClick}>
      <IconWrapper>{icon}</IconWrapper>
      <TextWrapper>{label}</TextWrapper>
    </StyledButton>
  );
};

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
  width: 2.5rem; /* Initial width to show only icon */

  &:hover {
    width: 8rem; /* Expand width to show text */
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

const TextWrapper = styled.span`
  margin-left: 0.5rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease;

  ${StyledButton}:hover & {
    opacity: 1;
  }
`;
