# General
It is a generator of elementary particle decay events.
All particle data is taken from [Particle Data Group](https://pdg.lbl.gov/).

![Error of download image.](https://live.staticflickr.com/65535/52846770284_d352728b65_k.jpg)


## About ```decay.MyParticle```

This class represents the following attributes.

* ```MyParticle.particle```. This is a string storing the unique name of the particle.

* ```MyParticle.decays```. This is a list of decay options, containing the $\LaTeX$ code of the decay products and the probabilities of the corresponding decays. For ease of data processing, each item in this list is a dictionary with the following fields:
	
	* ``"latex"`` are decay products, in $\LaTeX$ format. 
	
	* ``"probability_wm"`` the probability of the corresponding decay, written as matisse
	
	* ``"delta_wm"`` the error of the probability of the corresponding decay, written as the mantissa
	
	* ``"log_mantiss"`` the order of probability (and error).
	
	  

## About ``MyParticle.gen``
The main method of the class. It has the following form:
```python
decay.MyParticle.gen(self, count_of_particles, with_open=True, progress_bar=True, dpi=1200)
```
When the with_open parameter is ``True``, the ``PNG`` file with the results opens immediately after the simulation ends.

The ``dpi`` parameter is responsible for the quality of the resulting image.



## About `data.json`

This file stores all kinds of particles and results of their decays in the same format like ``MyParticle.decays``.


# Requirements

Just do `pip install -r requirements.txt`. 

Also you will need $\LaTeX$ installed. For example, [MiKTeX](https://miktex.org/download) is fine. 
