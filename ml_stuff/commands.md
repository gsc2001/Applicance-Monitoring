## Export/Import commands


```

sudo apt install mongo-tools

mongoexport --uri mongodb+srv://admin:<PASSWORD>@cluster0.x7zgm.mongodb.net/myFirstDatabase --collection datas --type json --out ./data.json --forceTableScan 

Then, replace "^\}" with "},"

Then, add "[" and "]" at the beginning and end to convert it into an array

```

