const mongoose = require("mongoose");

const DataSchema = new mongoose.Schema({
  device: {
    type: String,
    required: true,
  },
  data: [{ type: Number, required: true }],
});

module.exports = mongoose.model("data", DataSchema);
