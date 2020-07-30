#! /usr/bin/env python

from pygltflib import GLTF2
from subprocess import call
from pygltflib.utils import glb2gltf, gltf2glb

path = 'converter.js'

def gtlf2glb_call(file, destination):
    gltf2glb(file, destination=destination, override=True)


def obj2glb_call(file, destination):
    call(["node", path, file, destination])





