/*
npm install obj2gltf
*/

var myArgs = process.argv.slice(2);
//console.log('myArgs: ', myArgs);

obj_name = myArgs[0]
glb_name = myArgs[1]

const obj2gltf = require('obj2gltf');
const fs = require('fs');
const options = {
    binary : true
}
obj2gltf(obj_name, options)
    .then(function(glb) {
        fs.writeFileSync(glb_name, glb);
    });
