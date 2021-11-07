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
    res.send("success");
    const dataPoints = req.body.data;
    const { device, sender, description, zeroValue } = req.body;

    const data = new Data({
      device,
      data: dataPoints,
      sender,
      description,
      zeroValue,
    });
    console.log(data);
    await data.save();
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ msg: "Server Error" });
  }
});

app.get("/:device", async (req, res) => {
  try {
    const device = req.params.device;

    const data = await Data.find({ device });

    const dataPoints = [];

    data.forEach((d) => dataPoints.push(...d.data));

    res.json(dataPoints);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ msg: "Server Error" });
  }
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log("Server started"));
