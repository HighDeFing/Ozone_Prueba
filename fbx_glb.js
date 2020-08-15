/*
npm install fbx2gltf
*/

var myArgs = process.argv.slice(2);
//console.log('myArgs: ', myArgs);

fbx_name = myArgs[0]
glb_name = myArgs[1]

const convert = require('fbx2gltf');
convert(fbx_name, glb_name, ['--khr-materials-unlit']).then(
  destPath => {
    // yay, do what we will with our shiny new GLB file!
  },
  error => {
    // ack, conversion failed: inspect 'error' for details
  }
);

