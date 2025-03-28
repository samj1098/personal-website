const express = require('express');
const db = require('../db');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// GET tasks
router.get('/', authenticateToken, async (req, res) => {
  try {
    const result = await db.query(
      'SELECT id, content FROM tasks WHERE user_id = $1 ORDER BY created_at DESC',
      [req.user.id]
    );
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching tasks:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// POST (add) task
router.post('/', authenticateToken, async (req, res) => {
  const { content } = req.body;

  if (!content) {
    return res.status(400).json({ message: 'Task content is required' });
  }

  try {
    await db.query(
      'INSERT INTO tasks (content, user_id) VALUES ($1, $2)',
      [content, req.user.id]
    );
    res.status(201).json({ message: 'Task added' });
  } catch (error) {
    console.error('Error adding task:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// DELETE task
router.delete('/:id', authenticateToken, async (req, res) => {
  const { id } = req.params;
  await db.query('DELETE FROM tasks WHERE id = $1 AND user_id = $2', [id, req.user.id]);
  res.json({ message: 'Task deleted' });
});

// UPDATE task
router.put('/:id', authenticateToken, async (req, res) => {
  const { id } = req.params;
  const { content } = req.body;
  await db.query(
    'UPDATE tasks SET content = $1 WHERE id = $2 AND user_id = $3',
    [content, id, req.user.id]
  );
  res.json({ message: 'Task updated' });
});

module.exports = router;