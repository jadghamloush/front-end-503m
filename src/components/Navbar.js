import React from "react";
import styled from "styled-components";
import { Button } from "../ui/Button";
import { SearchButton } from "../ui/SearchButton";
import { FaSearch, FaShoppingCart, FaUser } from "react-icons/fa"; // Importing icons
import { useNavigate } from "react-router-dom";

const Navbar = ({ isLoggedIn }) => {
  const navigate = useNavigate();

  const handleProfileCheck = () => {
    if (isLoggedIn) {
      navigate("/profile");
    } else {
      navigate("/login");
    }
  };

  return (
    <Nav>
      <NavLinks>
        <NavLink href="#men">Men</NavLink>
        <NavLink href="#women">Women</NavLink>
        <NavLink href="#kids">Kids</NavLink>
      </NavLinks>
      <Actions>
        <SearchButton
          icon={<FaSearch />}
          label="Search"
          expandable
          onClick={() => console.log("Searching...")}
        />

        <Button
          icon={<FaShoppingCart />}
          label="Cart"
          onClick={() => console.log("Cart")}
        />
        <Button
          icon={<FaUser />}
          label="Profile"
          onClick={handleProfileCheck}
        />
      </Actions>
    </Nav>
  );
};

export default Navbar;

const Nav = styled.nav`
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  position: absolute;
  width: 100%;
  top: 0;
`;

const NavLinks = styled.div`
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex: 1;
`;

const NavLink = styled.a`
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  margin-right: 1.5rem;
  position: relative;
  &:hover {
    color: #1e90ff;
  }
`;

const Actions = styled.div`
  display: flex;
  gap: 1rem;
`;
