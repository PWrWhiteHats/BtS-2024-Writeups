const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
const PORT = process.env.PORT || 3000;


// MongoDB Connection
const mongoURI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/ctfDB';

const connectDB = async() => {
    try {
        await mongoose.connect(mongoURI);
    } catch (error) {
        console.error(`Error connecting to MongoDB (${mongoURI}):`, error);
    }
}

// Define MongoDB Schema
const fruitSchema = new mongoose.Schema({
    id: String,
    name: String,
    price: Number
});
const Fruit = mongoose.model('Fruit', fruitSchema);

const listAllFruits = async () => {
    try {
        const fruits = await Fruit.find();
        console.log('All fruits in the database:');
        fruits.forEach(fruit => {
            console.log(fruit);
        });
    } catch (err) {
        console.error('Error listing fruits:', err);
    }
};

// Initialize default records in MongoDB upon server startup
const initializeDefaultRecords = async () => {
    try {
        // Check if fruits collection is empty
        const count = await Fruit.countDocuments();
        if (count === 0) {
            // Insert default records with specified _id values
            await Fruit.insertMany([
                { id: '661c4cf05717c55d8ceb5d23', name: 'Banana', price: 0.99 },
                { id: '7e3c3c2ac105a4d471c060e0', name: 'Orange', price: 1.49 },
                { id: 'eb33ae021289259b83f2b635', name: 'Apple', price: 1.29 },
                { id: 'd07c3907ea5e559981518e21', name: 'BtSCTF{tutti_frutti}', price: 999.99 }
            ]);
            console.log('Default records inserted into MongoDB.');
        } else {
            console.log('MongoDB already populated with default records.');
        }

        // List all fruits in the database after inserting defaults
        await listAllFruits();
    } catch (err) {
        console.error('Error initializing default records:', err);
    }
};

// Express Middleware
app.use(bodyParser.json());

// Define API routes
// POST /fruits - Create a new fruit
app.post('/fruits', async (req, res) => {
    const { name, price } = req.body;
    try {
        const newFruit = new Fruit({ name, price });
        // await newFruit.save();
        res.status(201).json({ message: 'Waiting for verification', id: newFruit._id });
    } catch (err) {
        console.error('Error creating fruit:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// GET /fruits/:id - Get fruit details by ID
app.get('/fruits', async (req, res) => {
    const id = req.query.id; // Extract 'id' from query parameters
    console.log('Requested fruit ID:', id); // Check the ID in console

    try {
        const fruit = await Fruit.find({ id }).select('-_id -__v').lean();;
        if (!fruit) {
            return res.status(404).json({ error: 'Fruit not found' });
        }
        res.json(fruit);
    } catch (err) {
        console.error('Error fetching fruit:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Swagger Configuration
const swaggerOptions = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Mango',
            version: '1.0.0',
            description: 'Welcome to my fruit shop!'
        },
        components: {
            schemas: {
                Fruit: {
                    type: 'object',
                    properties: {
                        id: {
                            type: 'string'
                        },
                        name: {
                            type: 'string'
                        },
                        price: {
                            type: 'number'
                        }
                    }
                }
            }
        }
    },
    apis: ['index.js']
};

/**
 * @swagger
 * components:
 *   schemas:
 *     Fruit:
 *       type: object
 *       properties:
 *         id:
 *           type: string
 *           description: Unique identifier for the fruit
 *         name:
 *           type: string
 *           description: Name of the fruit
 *         price:
 *           type: number
 *           description: Price of the fruit
 * /fruits:
 *   post:
 *     summary: Create a new fruit
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:  
 *               name:
 *                 type: string
 *               price:
 *                 type: number
 *     responses:
 *       201:
 *         description: Fruit created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Fruit'
 *             example:
 *               message: 'Waiting for verification'
 *               id: '661c4d125717c55d8ceb5d27'
 *       400:
 *         description: Invalid request body
 *   get:
 *     summary: Get fruit details by ID
 *     description: Returns details of a fruit by its ID using query parameter.
 *     parameters:
 *       - in: query
 *         name: id
 *         required: true
 *         description: ID of the fruit to retrieve
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Successful response
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Fruit'
 *             example:
 *               id: '661c4cf05717c55d8ceb5d23'
 *               name: 'Banana'
 *               price: 0.99
 *       404:
 *         description: Fruit not found
 */

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// Start Express server
app.listen(PORT, async () => {
    console.log(`Server is running on port ${PORT}`);

    // Initialize default records in MongoDB
    await connectDB();
    await initializeDefaultRecords();
});
