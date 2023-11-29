# Differentiable Iso-Surface Extraction Package (DISO)
This repo contains various differentiable iso-surface extraction algorithms implemented in `cuda`.

Currently two algorithms are implemented:
* Differentiable **Marching Cubes** [1] (DiffMC)
* Differentiable **Dual Marching Cubes** [2] (DiffDMC)

The differentiable iso-surface algorithms have multiple applications in gradient-based optimization, such as shape, texture, materials reconstruction from images.

# Installation
Requirements: torch (should be compatible with cuda version), trimesh
```
pip install diso
```

# Quick Start
You can simply try the following command, which turns a sphere SDF into triangle mesh using different algorithms. The generated results are saved in `out/`.
```
python test.py
```

Note:
* `DiffMC` generates guaranteed watertight manifold meshes w/ or w/o grid deformation.
* `DiffDMC` generated watertight manifold meshes when grid deformation is diabled. When enbale grid deformation, self-intersection may appear but the face connectivity is still manifold.
* `DiffDMC` can generate more uniform triangle distribution and smoother surfaces than `DiffMC` and supports generating quad mesh (in the example, the quad is automatically divided into two triangles by `trimesh`).

<p align="center">
  <img src="imgs/example.png" alt="drawing" width="600" />
</p>

# How to use
## Input
* `sdf`: queries sdf values on the grid vertices. The gradient will be back-propagated to the source that generates the sdf values.
* `deform (optional)`: (learnable) deformation values on the grid vertices, the range must be [-0.5, 0.5], default=None

## Output
* `verts`: mesh vertices within the range of [0, 1]
* `faces`: mesh faces

# Speed Comparison
We compare our library with DMTet [3] and FlexiCubes [4] on two examples: a simple round cube and a random initialized signed distance function.

<p align="center">
  <img src="imgs/speed.png" alt="drawing" width="400" />
</p>

| Round Cube | DMTet | FlexiCubes | DiffMC | DiffDMC |
| --- | --- | --- | --- | --- |
| \# Vertices | 19622 | 19424 | 19944 | 19946 |
| \# Faces | 39240 | 38844 | 39884 | 39888 |
| Memory / G | 1.57 | 5.4 | 0.6 | 0.6 |
| Time / ms | 9.61 | 10 | 1.54 | 1.44 |
|  |  |  |  |  |


| Rand Init. | DMTet | FlexiCubes | DiffMC | DiffDMC |
| --- | --- | --- | --- | --- |
| \# Vertices | 2597474 | 2785274 | 2651046 | 2713134 |
| \# Faces | 4774241 | 4364842 | 4717384 | 2215690 |
| Memory / G | 3.07 | 4.07 | 0.59 | 0.45 |
| Time / ms | 49.1 | 65.35 | 2.55 | 2.78 |
|  |  |  |  |  |


# Citation
If you find this repo useful, please cite the following paper:
```
@article{wei2023neumanifold,
  title={NeuManifold: Neural Watertight Manifold Reconstruction with Efficient and High-Quality Rendering Support},
  author={Wei, Xinyue and Xiang, Fanbo and Bi, Sai and Chen, Anpei and Sunkavalli, Kalyan and Xu, Zexiang and Su, Hao},
  journal={arXiv preprint arXiv:2305.17134},
  year={2023}
}
```

# Reference
[1] We L S. Marching cubes: A high resolution 3d surface construction algorithm[J]. Comput Graph, 1987, 21: 163-169.

[2] Nielson G M. Dual marching cubes[C]//IEEE visualization 2004. IEEE, 2004: 489-496.

[3] Shen T, Gao J, Yin K, et al. Deep marching tetrahedra: a hybrid representation for high-resolution 3d shape synthesis[J]. Advances in Neural Information Processing Systems, 2021, 34: 6087-6101.

[4] Shen T, Munkberg J, Hasselgren J, et al. Flexible isosurface extraction for gradient-based mesh optimization[J]. ACM Transactions on Graphics (TOG), 2023, 42(4): 1-16.