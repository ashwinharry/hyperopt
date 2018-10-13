const express = require('express')
var bodyParser     =        require("body-parser");
var fs = require("fs");
const app = express()
const spawn = require("child_process").spawn;
const port = 3000

// app.get('/', (req, res) => {
//     res.send('Hello World!')
// })

app.use(bodyParser.json());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});
app.post('/submitModel', (req, res) => {
    console.log(req.body.mode)
    finalObj = {}
    finalObj[req.body.mode] = {}
    console.log(req.body.parameters)
    for( var param in req.body.parameters) {
        if(param === 'hidden_layer_sizes') {
            // console.log(req.body.parameters[param]);
            // var tuples = req.body.parameters[param].split(" ");
            tuples = req.body.parameters[param]
            len = tuples.length
            console.log(len)
            for(var idx=0; idx<len; idx++) {
                console.log('idx is ' + idx)
                tuples[idx] = tuples[idx].split(",").map(function(item) {
                    return parseInt(item, 10);
                });
            }
            // tuples.forEach((element, idx) => {
            //     console.log(element)
            //     tuples[idx] = element.split(",").map(function(item) {
            //         return parseInt(item, 10);
            //     });

            // });
            console.log(tuples);
            req.body.parameters[param] = tuples
        }
        finalObj[req.body.mode][param] = req.body.parameters[param];
    }
    console.log(finalObj);
    fs.writeFile( "hyperoptInput.json", JSON.stringify( finalObj ), "utf8", () => {console.log('json created')} );
    const hyperoptProcess = spawn('python',["./hyperopt.py", req.body.mode, "hyperoptInput.json"]);
    hyperoptProcess.stdout.on('data', (data) => {
        console.log(data.toString());
        var jsonResponse = data.toString();
        res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(jsonResponse));
    });
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}!`);
})