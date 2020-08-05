#! /usr/bin/env python

from pygltflib import GLTF2
from subprocess import call
from pygltflib.utils import glb2gltf, gltf2glb

from pygltflib.utils import ImageFormat, Image

FILE_NAME = "test_files/Spiral_GLTF/Untitled.gltf"
DESTINATION = "model.glb"
path = 'converter.js'
path_gltf = 'gltf_glb.js'


def gtlf2glb_call(file, destination):
    call(["node", path_gltf, file, destination])


def obj2glb_call(file, destination):
    call(["node", path, file, destination])





