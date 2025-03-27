const express = require('express');
const db = require('../db');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Get tasks for logged-in user
router.get('/', authenticateToken, async (req, res) => {
  const userId = req.user.id;

  try {
    const result = await db.query('SELECT * FROM tasks WHERE user_id = $1', [userId]);
    res.json(result.rows);
  } catch (err) {
    console.error('Error getting tasks:', err);
    res.status(500).json({ message: 'Server error' });
  }
});

// Add a new task
router.get('/', authenticateToken, async (req, res) => {
    try {
      const result = await pool.query(
        'SELECT id, description FROM tasks WHERE user_id = $1 ORDER BY created_at DESC',
        [req.user.id]
      );
      res.json(result.rows);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      res.status(500).json({ message: 'Server error' });
    }
  });
  

module.exports = router;

// Edit a task by ID
// DELETE
router.delete('/:id', authenticateToken, async (req, res) => {
    const { id } = req.params;
    await pool.query('DELETE FROM tasks WHERE id = $1 AND user_id = $2', [id, req.user.id]);
    res.json({ message: 'Task deleted' });
  });
  
  // PUT
  router.put('/:id', authenticateToken, async (req, res) => {
    const { id } = req.params;
    const { description } = req.body;
    await pool.query(
      'UPDATE tasks SET description = $1 WHERE id = $2 AND user_id = $3',
      [description, id, req.user.id]
    );
    res.json({ message: 'Task updated' });
  });
  