from pygltflib import GLTF2
from pygltflib.utils import glb2gltf, gltf2glb


def gtlf2glb_call(f, d):
    gltf2glb(f, destination=d, override=True)

