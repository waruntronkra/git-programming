const express = require('express');

const app = express();

const users = [
    {id: 1, name: 'warun'},
    {id: 2, name: 'tron'},
    {id: 3, name: 'kran'}
]

app.get('/users', (req, res) => {
    try {
        res.json(users);
    } catch (err) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(3000, '0.0.0.0', () => {
    console.log('Server running on port 3000');
});
