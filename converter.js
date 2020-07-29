/*
npm install obj2gltf
*/

const obj2gltf = require('obj2gltf');
const fs = require('fs');
const options = {
    binary : true
}
obj2gltf('./test_files/mono.obj', options)
    .then(function(glb) {
        fs.writeFileSync('./test_files/model1.glb', glb);
    });