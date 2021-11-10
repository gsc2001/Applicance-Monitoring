require("dotenv").config();
const db = process.env.mongoURI;
const mongoose = require("mongoose");
const express = require("express");

const Data = require("./data.model");

// Connect to DB
const connectDB = async () => {
  try {
    await mongoose.connect(db);

    console.log("Connected to MongoDB");
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }
};

connectDB();
const app = express();
app.use(express.json());

app.post("/", async (req, res) => {
  try {
    const dataPoints = req.body.data;
    const {
      device,
      sender,
      version,
      iteration,
      delay,
      zeroValue,
      description,
    } = req.body;

    const existingData = await Data.findOne({
      device,
      sender,
      version,
      iteration,
    });

    if (existingData) {
      console.log("ERROR: Existing Data");
      console.log(existingData);

      res.status(409).send("Duplicate Data");
    } else {
      res.send("success");

      const data = new Data({
        data: dataPoints,
        device,
        sender,
        version,
        iteration,
        delay,
        zeroValue,
        description,
      });
      console.log(data);
      await data.save();
    }
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ msg: "Server Error" });
  }
});


app.post('/test/t1', async (req,res) => {
	console.log(req.body)
	res.send("done")
});
app.get('/test/t1', async (req,res) => {
	console.log(req.body)
	res.send("done")
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log("Server started"));
