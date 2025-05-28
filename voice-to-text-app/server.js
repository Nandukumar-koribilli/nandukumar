const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const app = express();
const port = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/voiceToText', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log('Connected to MongoDB');
}).catch(err => {
    console.error('MongoDB connection error:', err);
});

// Define schema
const transcriptionSchema = new mongoose.Schema({
    text: String,
    timestamp: { type: Date, default: Date.now }
});
const Transcription = mongoose.model('Transcription', transcriptionSchema);

// Serve the frontend
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Save transcription
app.post('/save', async (req, res) => {
    try {
        const { text } = req.body;
        const transcription = new Transcription({ text });
        await transcription.save();
        res.status(201).send('Transcription saved');
    } catch (err) {
        console.error('Error saving transcription:', err);
        res.status(500).send('Error saving transcription');
    }
});

// Get all transcriptions
app.get('/transcriptions', async (req, res) => {
    try {
        const transcriptions = await Transcription.find().sort({ timestamp: -1 });
        res.json(transcriptions);
    } catch (err) {
        console.error('Error fetching transcriptions:', err);
        res.status(500).send('Error fetching transcriptions');
    }
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});