require('dotenv').config();
const express = require('express');
const cors = require('cors');
const http = require('http');
const { Server } = require('socket.io');
const mongoose = require('mongoose');
const { Pool } = require('pg');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

app.use(cors());
app.use(express.json());

// Database Connections
// MongoDB
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB Connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// PostgreSQL
const pgPool = new Pool({
    connectionString: process.env.PG_URI,
});
pgPool.connect()
    .then(() => console.log('PostgreSQL Connected'))
    .catch(err => console.error('PostgreSQL connection error:', err));

const { initDB } = require('./models/dbInit');
initDB();

const usersRoute = require('./routes/users');
const reportsRoute = require('./routes/reports');
const alertsRoute = require('./routes/alerts');

app.use('/api/users', usersRoute);
app.use('/api/reports', reportsRoute);
app.use('/api/alerts', alertsRoute);

// Basic Route
app.get('/', (req, res) => {
    res.send('SafeRoute AI Backend is running');
});

// Socket.io for Real-time alerts
io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
    });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
