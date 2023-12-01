[![Python application test](https://github.com/SCiarella/circuit-rbm/actions/workflows/test.yaml/badge.svg)](https://github.com/SCiarella/circuit-rbm/actions/workflows/test.yaml)

# circuit-rbm
RBM implementation in physical circuits

# To do list
- [x] GPU implementation  
- [ ] new datasets (Simone)
- [x] implementation of second ground to model real Hopfield units (not needed anymore ?)
- [x] implementation of double hidden nodes (energy='linear_circuit_3')
- [x] implementation of approximated network with large values of ground in order to dominate the quadratic term :white_check_mark: (energy='linear_circuit_4')
- [ ] write notes/paper (https://www.overleaf.com/project/646f5e5c40f932520678c415)
- [x] Improve plotting
- [x] Fix the circuit models in the pytorch class
- [ ] Implement metric to evaluate energy consumption or something on the physical size (Marcelo)
- [x] Implement metric to evaluate algorithmic efficiency  
I now report reconstruction error, energy (*has to be implemented for circuit (Marcelo)*), energy mse, covariance error, 3rd moment error, MSE on power spectrum, adversarial accuracy indicator, Frechet Inception Distance (based on an autoencoder), entropy (using gzip)
- [x] Implement Autoencoder for comparison
- [ ] Implement energy function for the circuit (Marcelo)
- [ ] Fix linear_circuit_4 and test for easier data
- [ ] (Marcelo) get access to a GPU in order to use pytorch implementation
- [x] test the NReLU units with *linear_circuit_4*
- [ ] (Simone) *linear_circuit_4* at T-->0
- [ ] (Marcelo) implement linear_circuit_5 with pytorch


# Remarks
- There are problems with *linear_circuit_4* : in PCD it seems that it starts learning (pattern appears in the weights), but then the weights explode and patterns are lost
- weights tend to grow very large over time, and maybe this is destabilizing
- If RND gradient estimation is used, the generation looks nice except that some sample have inverted colors
## Generation
Reading the literature more carefully, it looks like contrastive divergence does not generalize well at all!
From the paper of Decelle: "Finally, we want to mention that it is particularly surprising that the CD recipe (with short k) is still used [41, 42, 43, 39]. As shown, RBMs trained with CD are not able to generate proper samples from scratch."
For this reason I have implemented Persistent contrastive divergence (PCD) and Random sampling (RDM).
Another fundamental ingredient for the generalization is the *gradient centering*, that I have implemented and tested for Hopfield.

## Comparison with autoencoder
The (variational) autoencoder performs similarly well in reconstructing, so we have to compare it with our energy-based model. I see these significant differences:
- (1) *Training*: vae will be trained with coupled learning, RBM with 'resistors-PCD'. I am not sure which one is 'better' in practice.
- (2) *Sampling*: vae needs a more complex sampling method (compared to RBM) in the bottleneck layer for generating the data, i.e. you need to define some kind of gaussian latent space representation, use it for the training and then you can use it for generation. If you try to generate from white noise, the results are awful (check figure_AE* directory). In RBM the generation is much easier because you randomly turn on units with the noise generator and you do not directly need to know and use the noise distribution.
- (3) *Size*: vae is at least twice as large as a RBM (also in terms of resistors).

Overall (2) and (3) are in favor of our energy-based models, while (1) is and open question.

## Training algorithms
For the *linear_circuit_4* it seems that PCD has problems (weights grow too large?), while RND can generate sample.
I believe this is not a bug (because PCD works for Hopfield), but instead it is a problem related to the energy function of the circuit in some way.
Instead RND generates good sample (some with inverted colors), but still a significant growth of the weights over time can be seen, and I believe this is what is destabilizing PCD.
Side question: in experiments, how inconvenient it is to use RND instead of PCD?
