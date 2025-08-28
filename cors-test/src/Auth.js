import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://18.232.65.45:8000"; // your EC2 backend URL

export default function Auth() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("student");
  const [isLogin, setIsLogin] = useState(true); // toggle between login & register
  const [message, setMessage] = useState("");

  // REGISTER
  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/register/`, {
        username,
        password,
        email,
        role,
      });
      setMessage("✅ Registration successful! You can now login.");
      console.log("Registration success:", response.data);
    } catch (error) {
      console.error("Registration failed:", error.response?.data || error.message);
      setMessage("❌ Registration failed. Check console.");
    }
  };

  // LOGIN
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/login/`, {
        username,
        password,
      });
      setMessage("✅ Login successful!");
      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);
      console.log("Login success:", response.data);
    } catch (error) {
      console.error("Login failed:", error.response?.data || error.message);
      setMessage("❌ Login failed. Check console.");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2>{isLogin ? "Login" : "Register"}</h2>
        <form onSubmit={isLogin ? handleLogin : handleRegister} style={styles.form}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={styles.input}
            required
          />
          {!isLogin && (
            <>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={styles.input}
                required
              />
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={styles.input}
              >
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
              </select>
            </>
          )}
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
            required
          />
          <button type="submit" style={styles.button}>
            {isLogin ? "Login" : "Register"}
          </button>
        </form>
        <p style={{ marginTop: "10px" }}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            onClick={() => setIsLogin(!isLogin)}
            style={styles.toggleButton}
          >
            {isLogin ? "Register here" : "Login here"}
          </button>
        </p>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
}

// Inline CSS styles
const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    background: "#f4f4f4",
  },
  card: {
    background: "#fff",
    padding: "30px",
    borderRadius: "8px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    width: "350px",
    textAlign: "center",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px",
    fontSize: "16px",
    borderRadius: "5px",
    border: "none",
    background: "#007bff",
    color: "white",
    cursor: "pointer",
  },
  toggleButton: {
    background: "none",
    border: "none",
    color: "#007bff",
    cursor: "pointer",
    textDecoration: "underline",
    fontSize: "14px",
  },
};
