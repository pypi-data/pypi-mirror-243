# PyWPH : Wavelet Phase Harmonics in Python

PyWPH is a Python package designed for the computation and handling of the Wavelet Phase Harmonic (WPH) statistics.
These statistics can be computed from real or complex-valued images (2D data). Calculations are GPU-accelerated using PyTorch/CUDA (torch>=1.9.0). See the [PyTorch installation guide](https://pytorch.org/get-started/locally/) if needed.

Install PyWPH and check out our [tutorial](examples/tutorial.ipynb) as well as the examples scripts located in the [examples/](examples/) folder. Example scripts include basic examples to compute WPH coefficients from an image, as well as more complex scripts for synthesis or statistical denoising. Examples of multi-channel syntheses are provided [here](https://github.com/bregaldo/dust_genmodels).

We refer to [arXiv:2208.03538](https://arxiv.org/abs/2208.03538) for a presentation of the WPH statistics computed in this package.

If you use this package, please cite the following paper:
* Regaldo-Saint Blancard, B., Allys, E., Boulanger, F., Levrier, F., & Jeffrey, N. (2021). A new approach for the statistical denoising of Planck interstellar dust polarization data. [arXiv:2102.03160](https://arxiv.org/abs/2102.03160)

Related references:
* Mallat, S., Zhang, S., & Rochette, G. (2020). Phase harmonic correlations and convolutional neural networks. Information and Inference: A Journal of the IMA, 9(3), 721–747. https://doi.org/10.1093/imaiai/iaz019 [arXiv:1810.12136](https://arxiv.org/abs/1810.12136)
* Allys, E., Marchand, T., Cardoso, J.-F., Villaescusa-Navarro, F., Ho, S., & Mallat, S. (2020). New Interpretable Statistics for Large Scale Structure Analysis and Generation. Physical Review D, 102(10), 103506. [arXiv:2006.06298](http://arxiv.org/abs/2006.06298)
* Zhang, S., & Mallat, S. (2021). Maximum Entropy Models from Phase Harmonic Covariances. Applied and Computational Harmonic Analysis, 53, 199–230. https://doi.org/10.1016/j.acha.2021.01.003 [arXiv:1911.10017](https://arxiv.org/abs/1911.10017)
* Régaldo-Saint Blancard, B., Allys, E., Auclair, C., Boulanger, F., Eickenberg, M., Levrier, F., Vacher, L. & Zhang, S. (2022). Generative Models of Multi-channel Data from a Single Example - Application to Dust Emission. [arXiv:2208.03538](https://arxiv.org/abs/2208.03538). [Code](https://github.com/bregaldo/dust_genmodels).

This code originally takes inspiration from [https://github.com/Ttantto/wph_quijote](https://github.com/Ttantto/wph_quijote).

## Install/Uninstall

### Standard installation (from the Python Package Index)

```
pip install pywph
```

### Install from source

Clone the repository and type from the main directory:

```
pip install -r requirements.txt
pip install .
```

### Uninstall

```
pip uninstall pywph
```

## Changelog

### v1.1

* New default discretization grid for the shift vector $\tau$
* New set of scaling moments $L$ (which replaced the old ones)

Version of the code used for [arXiv:2208.03538](https://arxiv.org/abs/2208.03538).
### v1.0

* Cross-WPH statistics added
* Smarter way to evaluate moments at different $\tau$
* Improved computation for non periodic boundary conditions data
### v0.9

First release. Version of the code used for [arXiv:2102.03160](https://arxiv.org/abs/2102.03160).
