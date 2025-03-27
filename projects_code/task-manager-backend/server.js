const express = require('express');
const cors = require('cors');
const { Pool } = require('pg');
require('dotenv').config();  // Load .env

const app = express();
const port = 4000;

app.use(cors());
app.use(express.json());

// Connect to PostgreSQL using info from .env
const db = new Pool({
  host: process.env.PGHOST,
  user: process.env.PGUSER,
  password: process.env.PGPASSWORD,
  database: process.env.PGDATABASE,
  port: process.env.PGPORT
});

// Test route
app.get('/', (req, res) => {
  res.send('Task Manager API is live!');
});

// Start server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});

// Register a new user
app.post('/auth/register', async (req, res) => {
    const { username, password } = req.body;
  
    try {
      // Check if the user already exists
      const existingUser = await db.query(
        'SELECT * FROM users WHERE username = $1',
        [username]
      );
  
      if (existingUser.rows.length > 0) {
        return res.status(400).json({ message: 'User already exists' });
      }
  
      // Create the new user
      await db.query(
        'INSERT INTO users (username, password) VALUES ($1, $2)',
        [username, password]
      );
  
      res.status(201).json({ message: 'User registered successfully' });
    } catch (error) {
      console.error('Register error:', error);
      res.status(500).json({ message: 'Server error' });
    }
  });
  