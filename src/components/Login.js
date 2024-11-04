import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import axios from "axios";

const Login = ({ setIsLoggedIn }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });
      if (response.data.message === "Login successful") {
        setIsLoggedIn(true);
        navigate("/profile");
      }
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  return (
    <Container>
      <FormWrapper>
        <Title>Welcome Back!</Title>
        <Subtitle>Please log in to your account</Subtitle>
        <Form onSubmit={handleLogin}>
          <InputWrapper>
            <Label>Email</Label>
            <Input
              type="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </InputWrapper>
          <InputWrapper>
            <Label>Password</Label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </InputWrapper>
          <LoginButton type="submit">Log In</LoginButton>
        </Form>
        <SignUpPrompt>
          Don't have an account?{" "}
          <SignUpLink onClick={() => navigate("/signup")}>Sign Up</SignUpLink>
        </SignUpPrompt>
      </FormWrapper>
    </Container>
  );
};

export default Login;

// Styled Components

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: transparent;
`;

const FormWrapper = styled.div`
  background-color: transparent;
  padding: 2rem;
  border-radius: 8px;

  width: 100%;
  max-width: 400px;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: white;
`;

const Subtitle = styled.p`
  color: white;
  margin-bottom: 2rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
`;

const InputWrapper = styled.div`
  margin-bottom: 1rem;
  text-align: left;
`;

const Label = styled.label`
  font-size: 0.9rem;
  color: white;
  margin-bottom: 0.25rem;
  display: block;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  &:focus {
    border-color: #007bff;
    outline: none;
  }
`;

const LoginButton = styled.button`
  background-color: #007bff;
  color: #fff;
  font-size: 1rem;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 1rem;
  &:hover {
    background-color: #0056b3;
  }
`;

const SignUpPrompt = styled.p`
  margin-top: 1rem;
  color: white;
`;

const SignUpLink = styled.span`
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
  &:hover {
    color: #0056b3;
  }
`;
