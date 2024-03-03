const express = require('express');
const sql = require('mssql');

const app = express();

const config = {
    server: 'DESKTOP-3B64922\\CITADEL',
    database: 'Data_Storage',
    user: 'your_username',
    password: 'your_password',
    option: {
        encrypt: true, // Use encryption
        enableArithAbort: true // Enable ArithAbort
    }
};
// Connect to the database
async function connectToDatabase() {
    try {
        await sql.connect(config);
        console.log('Connected to the database');
    } catch (err) {
        console.error('Error connecting to the database:', err);
    }
}

// Query data from the database
async function getUsersFromDatabase() {
    try {
        const result = await sql.query`SELECT * FROM 01_MM_App`;
        return result.recordset; // Return the array of records
    } catch (err) {
        console.error('Error querying data:', err);
        return []; // Return an empty array if there's an error
    }
}

// Route to get users from the database
app.get('/users', async (req, res) => {
    try {
        const users = await getUsersFromDatabase();
        res.json(users);
    } catch (err) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Main function to run the application
async function main() {
    await connectToDatabase(); // Connect to the database
    app.listen(3000, '0.0.0.0', () => {
        console.log('Server running on port 3000');
    });
}

main();