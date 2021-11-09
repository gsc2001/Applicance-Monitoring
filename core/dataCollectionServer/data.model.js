const mongoose = require("mongoose");

const DataSchema = new mongoose.Schema({
  device: {
    type: String,
    required: true,
  },
  sender: {
    type: String,
    required: true,
  },
  version: {
    type: Number,
    required: true,
  },
  iteration: {
    type: Number,
    required: true,
  },
  delay: {
    type: Number,
    required: true,
  },
  zeroValue: {
    type: Number,
    required: true,
  },
  description: {
    type: String,
  },
  data: [{ type: Number, required: true }],
});

module.exports = mongoose.model("data", DataSchema);
