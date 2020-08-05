/*
npm install gltf-pipeline
*/

var myArgs = process.argv.slice(2);
console.log('myArgs: ', myArgs);

gltf_name = myArgs[0];
glb_name = myArgs[1];
resourceDirectory = myArgs[0].split('\\', 3);
path = "."
for (line of resourceDirectory){
    path += '/' + line
    }
console.log(path);

const gltfPipeline = require('gltf-pipeline');
const fsExtra = require('fs-extra');
const gltfToGlb = gltfPipeline.gltfToGlb;
const gltf = fsExtra.readJsonSync(gltf_name);
var options = {
    resourceDirectory: path,
}
gltfToGlb(gltf, options).then(function(results) {
        fsExtra.writeFileSync(glb_name, results.glb);
    });