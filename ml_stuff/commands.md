## Export/Import commands


```

sudo apt install mongo-tools

mongoexport --uri mongodb+srv://admin:<PASSWORD>@cluster0.x7zgm.mongodb.net/myFirstDatabase --collection datas --type json --out ./data.json --forceTableScan 

Then, replace "^\}" with "},"

Then, add "[" and "]" at the beginning and end to convert it into an array

```

### 0.9 scores:
Rocket: 0.879
IndividualBOSS: 0.901
RISE: 0.973
TSForest: 0.951
Shapelet: 0.841


### 0.5 scores:
Rocket: 0.865
IndividualBOSS: 0.908
RISE: 0.954
TSForest: 0.952
Shapelet: 0.815

### 0.4 scores
Rocket: 0.856
IndividualBOSS: 0.911
RISE: 0.952
TSForest: 0.936
Shapelet: 0.780

