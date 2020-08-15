/*
npm install gltf-pipeline
*/

var myArgs = process.argv.slice(2);
//console.log('myArgs: ', myArgs);

gltf_name = myArgs[0];
glb_name = myArgs[1];
var path = require('path');
//var resourceDirectory1 = myArgs[0].split('\\', 4);
var resourceDirectory = path.dirname(myArgs[0])
//console.log('resourceDirectory1', resourceDirectory1);
//console.log('resourceDirectory2', resourceDirectory2);
//new_path = "."
//for (line of resourceDirectory1){
//    new_path += '/' + line
//    }
//console.log(new_path);

const gltfPipeline = require('gltf-pipeline');
const fsExtra = require('fs-extra');
const gltfToGlb = gltfPipeline.gltfToGlb;
const gltf = fsExtra.readJsonSync(gltf_name);
var options = {
    resourceDirectory: resourceDirectory,
}
gltfToGlb(gltf, options).then(function(results) {
        fsExtra.writeFileSync(glb_name, results.glb);
    });