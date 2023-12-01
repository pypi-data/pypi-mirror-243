import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import pickle
import glob
import torch
import torch.nn.init as init
import networkx as nx
from .circuit_utils import Circuit


class RBM(object):
    """Class for generic Restricted Boltzmann Machine (RBM)

    Parameters
    ----------
    model_name : str
        Name of the model
    n_vis : int
        Number of visible units
    n_hin : int
        Number of hidden units
    k : int
        Number of Gibbs sampling steps
    minMax_W : tuple
        Tuple containing the minimum and maximum values for the weights
    energy_type : str
        Type of energy_type function to use. Options are 'hopfield' and 'linear_circuit_i' with i=1,2,3
    optimizer : str
        Type of optimizer to use. Options are 'Adam' and 'SGD'
    regularization : bool
        Whether to use regularization or not
    l1_factor : float
        L1 regularization factor
    l2_factor : float
        L2 regularization factor

    Attributes
    ----------
    name : str
        Name of the model
    W : array-like, shape (n_hin, n_vis)
        Weight matrix
    v_bias : array-like, shape (n_vis,)
        Visible bias vector
    h_bias : array-like, shape (n_hin,)
        Hidden bias vector
    k : int
        Number of Gibbs sampling steps
    min_W : float
        Minimum value for the weights
    max_W : float
        Maximum value for the weights
    energy_type : str
        Type of energy_type function to use. Options are 'hopfield' and 'linear_circuit_i' with i=4,5
    n_hidden : int
        Number of hidden units
    n_visible : int
        Number of visible units
    epoch : int
        Current epoch
    errors_free_energy : list
        List containing the free energy difference between data and model
    errors_loss : list
        List containing the loss between data and model
    regularization : bool
        Whether to use regularization or not
    l1 : float
        L1 regularization factor
    l2 : float
        L2 regularization factor
    optimizer : str
        Type of optimizer to use. Options are 'Adam' and 'SGD'
    lr : float
        Learning rate
    m_dW : float
        Adam's momentum for the weights
    m_dv : float
        Adam's momentum for the visible bias
    m_dh : float
        Adam's momentum for the hidden bias
    v_dW : float
        Adam's velocity for the weights
    v_dv : float
        Adam's velocity for the visible bias
    v_dh : float
        Adam's velocity for the hidden bias
    beta1 : float
        Adam's beta1 parameter
    beta2 : float
        Adam's beta2 parameter
    epsilon : float
        Adam's epsilon parameter
    """

    def __init__(
        self,
        model_name,
        n_vis=784,
        n_hin=50,
        k=1,
        lr=0.01,
        max_epochs=200000,
        minMax_W=(-100, 100),
        energy_type='hopfield',
        optimizer='Adam',
        regularization=False,
        l1_factor=1e-7,
        l2_factor=1e-7,
        ground_v=1,
        ground_h=1,
        batch_size=64,
        train_algo='CD',
        centering=False,
        average_data=None,
        sampling_model_beta=1,
        nrelu=False,
        mytype=torch.double,
    ):
        self.name = model_name
        print('*** Initializing {}'.format(self.name))
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        # Set default dtype
        self.mytype = mytype
        torch.set_default_dtype(self.mytype)
        print('The model is working on the following device: {}'.format(
            self.device))
        self.k = k
        self.max_epochs = max_epochs
        self.lr = lr
        self.min_W, self.max_W = torch.Tensor(minMax_W).to(self.device)
        self.energy_type = energy_type
        self.n_hidden = n_hin
        self.n_visible = n_vis
        self.model_beta = sampling_model_beta
        # Quantities to store
        self.epoch = 0
        self.regularization = regularization
        if self.regularization == 'l1':
            self.l1 = l1_factor
        elif self.regularization == 'l2':
            self.l2 = l2_factor
        self.optimizer = optimizer
        # Initialize weights
        self.W = torch.randn(
            (
                n_hin,
                n_vis,
            ),
            dtype=self.mytype,
            device=self.device,
        )
        self.v_bias = torch.zeros((n_vis, ),
                                  dtype=self.mytype,
                                  device=self.device)
        self.h_bias = torch.randn((n_hin, ),
                                  dtype=self.mytype,
                                  device=self.device)
        # Make weights contiguous
        self.W = self.W.contiguous()
        self.v_bias = self.v_bias.contiguous()
        self.h_bias = self.h_bias.contiguous()
        ## Initialize with normal distribution
        init.xavier_normal_(self.W)
        init.normal_(self.v_bias)
        init.normal_(self.h_bias)
        if average_data is not None:
            # Initialize the visible bias from data frequency
            self.v_bias = (torch.log(average_data / (1 - average_data) +
                                     1e-5).to(self.device).to(self.mytype))
        if self.optimizer == 'Adam':
            # Adam's momenta
            self.m_dW = 0 * self.W
            self.m_dv = 0 * self.v_bias
            self.m_dh = 0 * self.h_bias
            self.v_dW = 0 * self.W
            self.v_dv = 0 * self.v_bias
            self.v_dh = 0 * self.h_bias
            # Adam's parameters
            self.beta1 = 0.9
            self.beta2 = 0.999
            self.epsilon = 1e-8
        if self.energy_type != 'hopfield':
            self.ground_v = ground_v
            self.ground_h = ground_h
            self._update_circuit_variables()
            if self.energy_type == 'linear_circuit_5':
                # Create the circuit
                self.circuit = nx.Graph()

                # add two visible nodes for each original visible node and connect them to the hidden nodes and the bias node
                # One loop per each set of nodes to ensure the correct order in networkx
                for i in range(self.n_visible):
                    self.circuit.add_node(i)  # positive visible node
                for i in range(self.n_visible):
                    self.circuit.add_node(n_vis + i)  # negative visible node
                for j in range(self.n_hidden):
                    self.circuit.add_node(2 * n_vis +
                                          j)  # positive hidden node
                for j in range(self.n_hidden):
                    self.circuit.add_node(2 * n_vis + n_hin +
                                          j)  # negative hidden node

                # add bias nodes
                self.circuit.add_node(2 * n_vis + 2 * n_hin)
                self.circuit.add_node(2 * n_vis + 2 * n_hin + 1)

                # add edges
                for i in range(self.n_visible):
                    for j in range(self.n_hidden):
                        self.circuit.add_edge(i, 2 * n_vis +
                                              j)  # , conductance=k_plus[j][i])
                        self.circuit.add_edge(
                            i, 2 * n_vis + n_hin +
                            j)  # , conductance=k_minus[j][i])
                        self.circuit.add_edge(
                            n_vis + i,
                            2 * n_vis + j)  # , conductance=k_minus[j][i])
                        self.circuit.add_edge(n_vis + i, 2 * n_vis + n_hin +
                                              j)  # , conductance=k_plus[j][i])
                    self.circuit.add_edge(
                        i, 2 * n_vis + 2 * n_hin)  # , conductance=q_plus[i])
                    self.circuit.add_edge(
                        n_vis + i,
                        2 * n_vis + 2 * n_hin)  # , conductance=q_minus[i])

                for j in range(self.n_hidden
                               ):  # connect the bias node to all hidden nodes
                    self.circuit.add_edge(2 * n_vis + j,
                                          2 * n_vis + 2 * n_hin +
                                          1)  # , conductance=c_plus[j])
                    self.circuit.add_edge(2 * n_vis + n_hin + j,
                                          2 * n_vis + 2 * n_hin +
                                          1)  # , conductance=c_minus[j])

                # assign the positions into three columns: bias, visible, hidden. All the columns are aligned horizontally.
                shift_vis = (self.n_visible - 1) / 2
                shift_hid = (self.n_hidden - 1) / 2

                spacing = 0.3
                adjusted_positions_vis = [(i + j * spacing)
                                          for i in range(self.n_visible)
                                          for j in range(2)]
                adjusted_positions_hid = [(i + j * spacing)
                                          for i in range(self.n_hidden)
                                          for j in range(2)]

                # normalize the positions to span 0 to (self.n_visible - 1) for visible and (self.n_hidden - 1) for hidden
                min_pos_vis = min(adjusted_positions_vis)
                max_pos_vis = max(adjusted_positions_vis)
                normalized_positions_vis = [
                    (pos - min_pos_vis) * (self.n_visible - 1) /
                    (max_pos_vis - min_pos_vis)
                    for pos in adjusted_positions_vis
                ]

                min_pos_hid = min(adjusted_positions_hid)
                max_pos_hid = max(adjusted_positions_hid)
                normalized_positions_hid = [
                    (pos - min_pos_hid) * (self.n_hidden - 1) /
                    (max_pos_hid - min_pos_hid)
                    for pos in adjusted_positions_hid
                ]

                pos = {
                    2 * n_vis + 2 * n_hin: (0, 0),
                    2 * n_vis + 2 * n_hin + 1: (3, 0)
                }
                pos.update({
                    i: (1, normalized_positions_vis[2 * i] - shift_vis)
                    for i in range(n_vis)
                })
                pos.update({
                    n_vis + i:
                    (1, normalized_positions_vis[2 * i + 1] - shift_vis)
                    for i in range(n_vis)
                })
                pos.update({
                    2 * n_vis + j:
                    (2, normalized_positions_hid[2 * j] - shift_hid)
                    for j in range(n_hin)
                })
                pos.update({
                    2 * n_vis + n_hin + j: (
                        2,
                        normalized_positions_hid[2 * j + 1] - shift_hid,
                    )
                    for j in range(n_hin)
                })

                # Set the positions of the nodes as attributes
                nx.set_node_attributes(self.circuit, pos, 'pos')

                circuit = Circuit(self.circuit)
                self.circuit = circuit

                # Store the indices of the visible nodes, hidden nodes, and bias nodes
                self.v_indices_plus = np.arange(self.n_visible)
                self.v_indices_minus = np.arange(self.n_visible,
                                                 2 * self.n_visible)
                self.h_indices_plus = np.arange(
                    2 * self.n_visible, 2 * self.n_visible + self.n_hidden)
                self.h_indices_minus = np.arange(
                    2 * self.n_visible + self.n_hidden,
                    2 * self.n_visible + 2 * self.n_hidden,
                )
                self.g_indices = np.arange(
                    2 * self.n_visible + 2 * self.n_hidden,
                    2 * self.n_visible + 2 * self.n_hidden + 2,
                )

                # Store the indices of the edges mapping from the ordered interactions to the edge list of networkx
                AA, BB = np.meshgrid(self.v_indices_plus, self.h_indices_plus)
                C1 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.v_indices_minus,
                                     self.h_indices_minus)
                C2 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.v_indices_plus, self.h_indices_minus)
                C3 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.v_indices_minus, self.h_indices_plus)
                C4 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.v_indices_plus, self.g_indices[0])
                C5 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.v_indices_minus, self.g_indices[0])
                C6 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.h_indices_plus, self.g_indices[1])
                C7 = np.column_stack((AA.ravel(), BB.ravel()))

                AA, BB = np.meshgrid(self.h_indices_minus, self.g_indices[1])
                C8 = np.column_stack((AA.ravel(), BB.ravel()))

                C = np.concatenate((C1, C2, C3, C4, C5, C6, C7, C8), axis=0)
                edgelist = np.array(self.circuit.graph.edges)

                edge_indexmap = []
                # For each row in edgelist, find the row in C that matches
                for row in edgelist:
                    # Use broadcasting to find the row in A
                    # np.all with axis 1 makes sure all elements in a row are equal
                    index = np.where((C == row).all(axis=1))[0][0]
                    edge_indexmap.append(index)

                self.edge_indexmap = np.array(edge_indexmap)

                self.Q_visible_clamped = self.circuit.constraint_matrix(
                    np.concatenate((self.v_indices_plus, self.v_indices_minus,
                                    self.g_indices)))
                self.Q_hidden_clamped = self.circuit.constraint_matrix(
                    np.concatenate((self.h_indices_plus, self.h_indices_minus,
                                    self.g_indices)))

                self.min_conductance = 0

        self.train_algo = train_algo
        self.batch_size = batch_size
        if self.train_algo == 'PCD':
            # Initialize the persistent chains
            self.persistent_chains = (torch.where(
                torch.rand(self.batch_size, self.n_visible) > 0.5, 1.0,
                0.0).to(self.device).to(self.mytype))
        self.centering = centering
        if self.centering:
            if average_data.shape[0] != n_vis:
                print(
                    'Error: you need to provide the average of the data to center the gradient'
                )
                sys.exit()
            # Initialize the offsets for the gradient centering
            self.ov = average_data.to(self.device)
            self.oh = self.h_bias * 0 + 0.5
            self.batch_ov = self.v_bias * 0
            self.batch_oh = self.h_bias * 0
            # And the sliding factors
            self.slv = 0.01
            self.slh = 0.01
        else:
            self.ov = 0
            self.oh = 0
        # Epochs at which to store the model
        num_points = 50
        self.t_to_save = sorted(
            list(
                set(
                    np.round(
                        np.logspace(np.log10(1), np.log10(self.max_epochs),
                                    num_points)).astype(int).tolist())))
        # *** If True I am using the NReLU
        self.nrelu = nrelu
        if self.nrelu:
            print('ERROR: NReLU not fully implemented')
            sys.exit()

    def pretrain(self, pretrained_model):
        # Check if you have model load points
        filename_list = glob.glob(
            'model_states/{}_t*.pkl'.format(pretrained_model))
        if len(filename_list) > 0:
            all_loadpoints = sorted([
                int(x.split('_t')[-1].split('.pkl')[0]) for x in filename_list
            ])
            last_epoch = all_loadpoints[-1]
            print('** Using as pretraining model {} at epoch {}'.format(
                pretrained_model, last_epoch))
            with open(
                    'model_states/{}_t{}.pkl'.format(pretrained_model,
                                                     last_epoch),
                    'rb') as file:
                temp_model = pickle.load(file)
                # *** Import pretrained parameters
                self.W = temp_model.W.to(self.mytype)
                self.h_bias = temp_model.h_bias.to(self.mytype)
                self.v_bias = temp_model.v_bias.to(self.mytype)
        else:
            print('** No load points for {}'.format(pretrained_model))

    def v_to_h(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'linear_circuit_5':
            return self.Bernoulli_v_to_h(v, beta)
        else:
            if beta > 1000:
                # I assume we are at T=0
                return self.Deterministic_v_to_h(v, beta)
            elif self.nrelu:
                return self.NReLU_v_to_h(v, beta)
            else:
                return self.Bernoulli_v_to_h(v, beta)

    def h_to_v(self, h, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'linear_circuit_5':
            return self.Bernoulli_h_to_v(h, beta)
        else:
            if beta > 1000:
                # I assume we are at T=0
                return self.Deterministic_h_to_v(h, beta)
            elif self.nrelu:
                return self.NReLU_h_to_v(h, beta)
            else:
                return self.Bernoulli_h_to_v(h, beta)

    def Deterministic_v_to_h(self, v, beta):
        h = (self.delta_eh(v) > 0).to(v.dtype)
        return h, h

    def Deterministic_h_to_v(self, h, beta):
        v = (self.delta_ev(h) > 0).to(h.dtype)
        return v, v

    def Bernoulli_v_to_h(self, v, beta):
        p_h = self._prob_h_given_v(v, beta)
        sample_h = torch.bernoulli(p_h)
        return p_h, sample_h

    def Bernoulli_h_to_v(self, h, beta):
        p_v = self._prob_v_given_h(h, beta)
        sample_v = torch.bernoulli(p_v)
        return p_v, sample_v

    def NReLU_v_to_h(self, v, beta):
        # out = max(0, x + N(0,sigma(x)))
        x = self.model_beta * self.delta_eh(v)
        activation = x + torch.sqrt(self.my_sigmoid(x)) * torch.randn(
            x.shape, device=self.device)
        sample_h = torch.clip(activation, 0, 1)
        return x, sample_h

    def NReLU_h_to_v(self, h, beta=1):
        x = self.model_beta * self.delta_ev(h)
        # activation = x + x.std()*torch.randn(x.shape, device=self.device)
        activation = x + torch.sqrt(self.my_sigmoid(x)) * torch.randn(
            x.shape, device=self.device)
        sample_v = torch.clip(activation, 0, 1)  # visible is binary
        return x, sample_v

    # The parameters of the 'diode'-sigmoid are hard coded
    def my_sigmoid(self, x, xscale=5, xshift=2.5):
        scaled_x = x * xscale
        shifted_x = scaled_x - xshift
        clipped_x = torch.clip(shifted_x, -10, 10)
        sigmoid_approx = (clipped_x + 10) / 20
        return sigmoid_approx

    def _free_energy_hopfield(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        vbias_term = torch.mv(v, self.v_bias) * beta
        wx_b = torch.mm(v, self.W.t()) + self.h_bias
        hidden_term = torch.sum(torch.log(1 + torch.exp(wx_b * beta)), axis=1)
        return -hidden_term - vbias_term

    def _energy_hopfield(self, v, h):
        energy = (-(torch.mm(v, self.W.t()) * h).sum(1) -
                  torch.mv(v, self.v_bias) - torch.mv(h, self.h_bias))
        return energy

    def _energy_linear_circuit_4(self, v, h):
        # ****** TO BE DONE! ******
        print('Warning: not implemented')
        energy = (-(torch.mm(v, self.W.t()) * h).sum(1) -
                  torch.mv(v, self.v_bias) - torch.mv(h, self.h_bias))
        return energy

    def forward(self, v, k, beta=None):
        if beta is None:
            beta = self.model_beta
        pre_h1, h1 = self.v_to_h(v, beta)
        h_ = h1
        for _ in range(k):
            pre_v_, v_ = self.h_to_v(h_, beta)
            pre_h_, h_ = self.v_to_h(v_, beta)
        return v_

    def train(
        self,
        train_data,
        test_data=[],
        print_error=False,
        print_test_error=False,
    ):
        """Train the model using the given data and parameters."""
        while self.epoch < self.max_epochs:
            self.tstep_keepup()
            # permutation = torch.randperm(train_data.size(0))
            # train_data = train_data[permutation]
            for _, v_data in enumerate(train_data):
                # n_batches = int(train_data.shape[0]/self.batch_size)
                # for bi in range(n_batches):
                #    v_data = train_data[bi*self.batch_size:(bi+1)*self.batch_size]
                start_time = time.time()
                if self.energy_type == 'linear_circuit_5':
                    # self._weights_to_conductances()
                    # set the conductances in the same order as they are internally stored
                    # conductances = [self.circuit.graph.edges[e]['conductance'] for e in self.circuit.graph.edges]
                    self.circuit.setConductances(
                        self._weights_to_conductances())
                if self.train_algo == 'PCD':
                    # Update the chain after every batch
                    self.persistent_chains = self.forward(
                        self.persistent_chains, self.k)
                    v_model = self.persistent_chains
                elif self.train_algo == 'RDM':
                    # This algo uses random samples
                    # But since we want to train with the same exact protocol that we will use for generation,
                    ## we random sample from the hidden and not the visible
                    # h_rnd = torch.randint(high=2, size=(self.batch_size, self.n_hidden), device=self.device, dtype=self.mytype)
                    # _, v_model = self.h_to_v(h_rnd)
                    v_model = torch.randint(
                        high=2,
                        size=(self.batch_size, self.n_visible),
                        device=self.device,
                        dtype=self.mytype,
                    )
                    # v_model = torch.bernoulli(0.5*torch.ones(size=(self.batch_size, self.n_visible), device=self.device, dtype=self.mytype))
                    #### This version has problems
                    ###random_tensor = torch.rand(self.batch_size, self.n_visible, device=self.device, dtype=self.mytype)
                    ###v_model = self.forward(torch.where(random_tensor > 0.5, 1.0, 0.0), self.k)
                    v_model = self.forward(v_model, self.k)
                elif self.train_algo == 'CD':
                    v_model = self.forward(v_data, self.k)

                # Apply model
                h_data = self.v_to_h(v_data)[0]
                h_model = self.v_to_h(v_model)[0]

                # Apply centering
                if self.centering:
                    self.batch_ov = v_data.mean(0)
                    self.batch_oh = h_data.mean(0)
                    # update with sliding
                    self.ov = (1 -
                               self.slv) * self.ov + self.slv * self.batch_ov
                    self.oh = (1 -
                               self.slh) * self.oh + self.slh * self.batch_oh

                # Compute gradients
                partial_gradients_data = self.derivatives(v_data, h_data)
                partial_gradients_model = self.derivatives(v_model, h_model)

                # Average gradient over batch
                partial_gradients_data = self.average_gradients(
                    partial_gradients_data)
                partial_gradients_model = self.average_gradients(
                    partial_gradients_model)

                # Update weights and biases
                if self.optimizer == 'Adam':
                    self.Adam_update(
                        self.epoch + 1,
                        partial_gradients_data,
                        partial_gradients_model,
                    )
                elif self.optimizer == 'SGD':
                    self.SGD_update(
                        partial_gradients_data,
                        partial_gradients_model,
                    )

                self.tstep_keepup()

                self.epoch += 1

                # Store the model state
                if self.epoch in self.t_to_save:
                    with open(
                            'model_states/{}_t{}.pkl'.format(
                                self.name, self.epoch), 'wb') as file:
                        pickle.dump(self, file)

                if self.epoch % 100 == 0:
                    t = time.time() - start_time
                    if print_error:
                        v_model = self.forward(v_data, 1)
                        rec_error_train = ((v_model -
                                            v_data)**2).mean(1).mean(0)
                        if not print_test_error:
                            print('Epoch: %d , train-err %.5g , time: %f' %
                                  (self.epoch, rec_error_train, t))
                        else:
                            t_model = self.forward(test_data, 1)
                            rec_error_test = (((t_model -
                                                test_data)**2).mean(1).mean(0))
                            print(
                                'Epoch: %d , Test-err %.5g , train-err %.5g , time: %f'
                                % (self.epoch, rec_error_test, rec_error_train,
                                   t))
                    else:
                        print('Epoch: %d , time: %f' % (self.epoch, t))

        print('*** Training finished')

    def tstep_keepup(self):
        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables()
        else:
            self.W_t = self.W.t()

    def average_gradients(self, gradients):
        average_gradients = []
        for g in gradients:
            average_gradients.append(torch.mean(g, dim=0))
        return average_gradients

    def SGD_update(
        self,
        partial_gradient_data,
        partial_gradient_model,
    ):
        # Get the correct gradients
        dEdW_data = partial_gradient_data[0]
        dEdW_model = partial_gradient_model[0]
        dEdv_bias_data = partial_gradient_data[1]
        dEdv_bias_model = partial_gradient_model[1]
        dEdh_bias_data = partial_gradient_data[2]
        dEdh_bias_model = partial_gradient_model[2]
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        if self.centering:
            dv = dv - torch.matmul(self.oh, dW)
            dh = dh - torch.matmul(self.ov, dW.t())
        # Add regularization term
        if self.regularization == 'l2':
            dW += self.l2 * 2 * self.W
            dv += self.l2 * 2 * self.v_bias
            dh += self.l2 * 2 * self.h_bias
        elif self.regularization == 'l1':
            dW += self.l1 * torch.sign(self.W)
            dv += self.l1 * torch.sign(self.v_bias)
            dh += self.l1 * torch.sign(self.h_bias)
        # Update parameters in-place
        # and clip
        gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(dh)
        myclip = (self.lr * 10.0) / gnorm if gnorm > 10 else self.lr
        self.W.add_(myclip * dW)
        self.v_bias.add_(myclip * dv)
        self.h_bias.add_(myclip * dh)

    def Adam_update(
        self,
        t,
        partial_gradient_data,
        partial_gradient_model,
    ):
        # Get the correct gradients
        dEdW_data = partial_gradient_data[0]
        dEdW_model = partial_gradient_model[0]
        dEdv_bias_data = partial_gradient_data[1]
        dEdv_bias_model = partial_gradient_model[1]
        dEdh_bias_data = partial_gradient_data[2]
        dEdh_bias_model = partial_gradient_model[2]
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        if self.centering:
            dv = dv - torch.matmul(self.oh, dW)
            dh = dh - torch.matmul(self.ov, dW.t())
        # Add regularization term
        if self.regularization == 'l2':
            dW += self.l2 * 2 * self.W
            dv += self.l2 * 2 * self.v_bias
            dh += self.l2 * 2 * self.h_bias
        elif self.regularization == 'l1':
            dW += self.l1 * torch.sign(self.W)
            dv += self.l1 * torch.sign(self.v_bias)
            dh += self.l1 * torch.sign(self.h_bias)
        # momentum beta1
        self.m_dW = self.beta1 * self.m_dW + (1 - self.beta1) * dW
        self.m_dv = self.beta1 * self.m_dv + (1 - self.beta1) * dv
        self.m_dh = self.beta1 * self.m_dh + (1 - self.beta1) * dh
        # momentum beta2
        self.v_dW = self.beta2 * self.v_dW + (1 - self.beta2) * (dW**2)
        self.v_dv = self.beta2 * self.v_dv + (1 - self.beta2) * (dv**2)
        self.v_dh = self.beta2 * self.v_dh + (1 - self.beta2) * (dh**2)
        # bias correction
        m_dW_corr = self.m_dW / (1 - self.beta1**t)
        m_dv_corr = self.m_dv / (1 - self.beta1**t)
        m_dh_corr = self.m_dh / (1 - self.beta1**t)
        v_dW_corr = self.v_dW / (1 - self.beta2**t)
        v_dv_corr = self.v_dv / (1 - self.beta2**t)
        v_dh_corr = self.v_dh / (1 - self.beta2**t)
        # Update
        self.W = self.W + self.lr * (m_dW_corr /
                                     (torch.sqrt(v_dW_corr) + self.epsilon))
        self.v_bias = self.v_bias + self.lr * (
            m_dv_corr / (torch.sqrt(v_dv_corr) + self.epsilon))
        self.h_bias = self.h_bias + self.lr * (
            m_dh_corr / (torch.sqrt(v_dh_corr) + self.epsilon))

    def reconstruct(self, data, k, beta=None):
        if beta is None:
            beta = self.model_beta
        self.tstep_keepup()
        data = torch.Tensor(data).to(self.device).to(self.mytype)
        v_model = self.forward(data, k)
        return data.detach().cpu().numpy(), v_model.detach().cpu().numpy()

    def generate(self,
                 n_samples,
                 k,
                 h_binarized=True,
                 from_visible=True,
                 beta=None):
        if beta is None:
            beta = self.model_beta
        self.tstep_keepup()
        if from_visible:
            v = torch.randint(
                high=2,
                size=(n_samples, self.n_visible),
                device=self.device,
                dtype=self.mytype,
            )
        else:
            if h_binarized:
                h = torch.randint(
                    high=2,
                    size=(n_samples, self.n_hidden),
                    device=self.device,
                    dtype=self.mytype,
                )
            else:
                h = torch.rand(n_samples,
                               self.n_hidden,
                               device=self.device,
                               dtype=self.mytype)
            _, v = self.h_to_v(h)
        v_model = self.forward(v, k, beta)
        return v_model.detach().cpu().numpy()

    def clip_weights(self):
        self.W = torch.clip(self.W, self.min_W, self.max_W)
        self.W_t = self.W.t()

    def clip_bias(self):
        self.v_bias = torch.clip(self.v_bias, self.min_W, self.max_W)
        self.h_bias = torch.clip(self.h_bias, self.min_W, self.max_W)

    def _prob_h_given_v(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'linear_circuit_5':
            # Circuit minimization
            sol = self._circuit_minimization_visible_clamped(v)
            # h = sol[:,self.h_indices_plus]
            h = (sol[:, self.h_indices_plus] + 1 -
                 sol[:, self.h_indices_minus]) / 2
            # The probability is the outcome of the circuit
            # convert to pytorch tensor
            h = torch.Tensor(h).to(self.device).to(self.mytype)
            return torch.sigmoid(beta * h)
        else:
            return torch.sigmoid(beta * self.delta_eh(v))

    def _prob_v_given_h(self, h, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'linear_circuit_5':
            # Circuit minimization
            sol = self._circuit_minimization_hidden_clamped(h)
            # v = sol[:,self.v_indices_plus]
            v = (sol[:, self.v_indices_plus] + 1 -
                 sol[:, self.v_indices_minus]) / 2
            # The probability is the outcome of the circuit
            # convert to pytorch tensor
            v = torch.Tensor(v).to(self.device).to(self.mytype)
            return torch.sigmoid(beta * v)
        return torch.sigmoid(beta * self.delta_ev(h))

    def delta_eh(self, v):
        if self.energy_type == 'hopfield':
            return self._delta_eh_hopfield(v)
        elif self.energy_type == 'linear_circuit_4':
            return self._delta_eh_linear_circuit_4(v)

    def delta_ev(self, h):
        if self.energy_type == 'hopfield':
            return self._delta_ev_hopfield(h)
        elif self.energy_type == 'linear_circuit_4':
            return self._delta_ev_linear_circuit_4(h)

    # **** Hopfield transfer functions
    def _delta_eh_hopfield(self, v):
        return torch.mm(v, self.W_t) + self.h_bias

    def _delta_ev_hopfield(self, h):
        return torch.mm(h, self.W) + self.v_bias

    # **** linear_circuit_4 transfer functions
    def _delta_ev_linear_circuit_4(self, h):
        return torch.mm(torch.mul(h, 2) - 1, self._k_diff) + self._vb_posneg

    def _delta_eh_linear_circuit_4(self, v):
        return torch.mm(torch.mul(v, 2) - 1, self._k_diff_t) + self._hb_posneg

    def _update_circuit_variables(self):
        self._k_pos = self.k_pos()
        self._k_neg = self.k_neg()
        self._v_bias_pos = self.v_bias_pos()
        self._v_bias_neg = self.v_bias_neg()
        self._h_bias_pos = self.h_bias_pos()
        self._h_bias_neg = self.h_bias_neg()
        self._k_diff = self._k_pos - self._k_neg
        self._k_diff_t = self._k_diff.t()
        self._v_bias_pos_diff = self._v_bias_pos * (0.5 - self.ground_v)
        self._v_bias_neg_diff = self._v_bias_neg * (0.5 - self.ground_v)
        self._h_bias_pos_diff = self._h_bias_pos * (0.5 - self.ground_h)
        self._h_bias_neg_diff = self._h_bias_neg * (0.5 - self.ground_h)
        self._vb_posneg = -self._v_bias_pos_diff + self._v_bias_neg_diff
        self._hb_posneg = -self._h_bias_pos_diff + self._h_bias_neg_diff

    def derivatives(self, v, h):
        if self.energy_type == 'hopfield':
            return self.derivatives_hopfield(v, h)
        elif (self.energy_type == 'linear_circuit_4'
              or self.energy_type == 'linear_circuit_5'):
            return self.derivatives_linear_circuit_4(v, h)

    # CHANGE THIS FUNCTION TO USE THE CORRECT FREE ENERGY
    def free_energy(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        if self.energy_type == 'hopfield':
            return self._free_energy_hopfield(v, beta)
        elif self.energy_type == 'linear_circuit_4':
            return self._free_energy_hopfield(v)

    def energy(self, v, h):
        if self.energy_type == 'hopfield':
            return self._energy_hopfield(v, h)
        elif self.energy_type == 'linear_circuit_4':
            return self._energy_linear_circuit_4(v, h)

    def derivatives_hopfield(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        if self.centering:
            dEdW = -torch.einsum('ij,ik->ijk', h - self.oh, v - self.ov)
        else:
            dEdW = -torch.einsum('ij,ik->ijk', h, v)
        dEdv_bias = -v
        dEdh_bias = -h
        return (dEdW, dEdv_bias, dEdh_bias)

    def derivatives_linear_circuit_4(self, v, h):
        v_square = torch.square(v).unsqueeze(1)
        vneg_square = torch.square(1 - v).unsqueeze(1)
        h_square = torch.square(h).unsqueeze(2)
        hneg_square = torch.square(1 - h).unsqueeze(2)
        dEdk_pos = (-torch.einsum('ij,ik->ijk', h, v) + 0.5 * v_square + 0.5 *
                    h_square) + (-torch.einsum('ij,ik->ijk', 1 - h, 1 - v) +
                                 0.5 * vneg_square + 0.5 * hneg_square)
        dEdk_neg = (-torch.einsum('ij,ik->ijk', h, 1 - v) + 0.5 * vneg_square +
                    0.5 * h_square) + (-torch.einsum('ij,ik->ijk', 1 - h, v) +
                                       0.5 * v_square + 0.5 * hneg_square)
        dkdw_pos = self.dk_pos().unsqueeze(0)
        dkdw_neg = self.dk_neg().unsqueeze(0)
        dEdW = dEdk_pos * dkdw_pos + dEdk_neg * dkdw_neg
        dEdv_bias_pos = -self.ground_v * v + 0.5 * torch.square(v)
        dEdv_bias_neg = -self.ground_v * (1 - v) + 0.5 * torch.square(1 - v)
        dv_biasdv_pos = self.dv_bias_pos().unsqueeze(0)
        dv_biasdv_neg = self.dv_bias_neg().unsqueeze(0)
        dEdv_bias = dEdv_bias_pos * dv_biasdv_pos + dEdv_bias_neg * dv_biasdv_neg
        dEdh_bias_pos = -self.ground_h * h + 0.5 * torch.square(h)
        dEdh_bias_neg = -self.ground_h * (1 - h) + 0.5 * torch.square(1 - h)
        dh_biasdh_pos = self.dh_bias_pos().unsqueeze(0)
        dh_biasdh_neg = self.dh_bias_neg().unsqueeze(0)
        dEdh_bias = dEdh_bias_pos * dh_biasdh_pos + dEdh_bias_neg * dh_biasdh_neg
        return (dEdW, dEdv_bias, dEdh_bias)

    def _circuit_minimization_visible_clamped(self, v):
        # # convert weights to conductances
        # self._weights_to_conductances()
        # # set the conductances in the same order as they are internally stored
        # conductances = [self.circuit.graph.edges[e]['conductance'] for e in self.circuit.graph.edges]
        # self.circuit.setConductances(conductances)
        f = np.concatenate(
            (v, 1 - v, np.tile([self.ground_v, self.ground_h],
                               (v.shape[0], 1))),
            axis=1)
        return np.array(
            [self.circuit.solve(self.Q_visible_clamped, fi) for fi in f])

    def _circuit_minimization_hidden_clamped(self, h):
        # # convert weights to conductances
        # self._weights_to_conductances()
        # # set the conductances in the same order as they are internally stored
        # conductances = [self.circuit.graph.edges[e]['conductance'] for e in self.circuit.graph.edges]
        # self.circuit.setConductances(conductances)
        f = np.concatenate(
            (h, 1 - h, np.tile([self.ground_v, self.ground_h],
                               (h.shape[0], 1))),
            axis=1)
        return np.array(
            [self.circuit.solve(self.Q_hidden_clamped, fi) for fi in f])

    def _weights_to_conductances(self):
        """Function to transform weights to conductances. Used for power
        minimization in the real circuits.

        Returns:
            Conductances of the circuit.
        """
        k_plus = self.k_pos().ravel()
        k_minus = self.k_neg().ravel()
        q_plus = self.v_bias_pos()
        q_minus = self.v_bias_neg()
        c_plus = self.h_bias_pos()
        c_minus = self.h_bias_neg()
        # update the conductances
        # # USE UPDATE FUNCTION INSTEAD OF ADD_EDGE
        # for i in range(self.n_visible):
        #     for j in range(self.n_hidden):
        #         # interactions between visible and hidden units
        #         # self.circuit.add_edge(f'$v_{i}^+$', f'$h_{j}^+$', conductance=k_plus[j][i])
        #         self.circuit.graph.edges[f'$v_{i}^+$',f'$h_{j}^+$']['conductance'] = k_plus[j][i]
        #         self.circuit.graph.edges[f'$v_{i}^+$',f'$h_{j}^-$']['conductance'] = k_minus[j][i]
        #         self.circuit.graph.edges[f'$v_{i}^-$',f'$h_{j}^+$']['conductance'] = k_minus[j][i]
        #         self.circuit.graph.edges[f'$v_{i}^-$',f'$h_{j}^-$']['conductance'] = k_plus[j][i]

        #         # self.circuit.add_edge(f'$v_{i}^+$', f'$h_{j}^-$', conductance=k_minus[j][i])
        #         # self.circuit.add_edge(f'$v_{i}^-$', f'$h_{j}^+$', conductance=k_minus[j][i])
        #         # self.circuit.add_edge(f'$v_{i}^-$', f'$h_{j}^-$', conductance=k_plus[j][i])
        #     # interactions between visible and ground_visible
        #     # self.circuit.add_edge(f'$v_{i}^+$', r'$g_v$', conductance=q_plus[i])
        #     # self.circuit.add_edge(f'$v_{i}^-$', r'$g_v$', conductance=q_minus[i])
        #     self.circuit.graph.edges[f'$v_{i}^+$',r'$g_v$']['conductance'] = q_plus[i]
        #     self.circuit.graph.edges[f'$v_{i}^-$',r'$g_v$']['conductance'] = q_minus[i]

        # for j in range(self.n_hidden):
        #     # interactions between hidden and ground_hidden
        #     # self.circuit.add_edge(r'$g_h$', f'$h_{j}^+$', conductance=c_plus[j])
        #     # self.circuit.add_edge(r'$g_h$', f'$h_{j}^-$', conductance=c_minus[j])
        #     self.circuit.graph.edges[r'$g_h$',f'$h_{j}^+$']['conductance'] = c_plus[j]
        #     self.circuit.graph.edges[r'$g_h$',f'$h_{j}^-$']['conductance'] = c_minus[j]

        # Concatenate all the conductances according to the edge_indexmap
        conductances = np.concatenate(
            (k_plus, k_plus, k_minus, k_minus, q_plus, q_minus, c_plus,
             c_minus))[self.edge_indexmap]
        # if conductances are too small, set them to a minimum value
        conductances[conductances <
                     self.min_conductance] = self.min_conductance
        return conductances

    # ***** Get high-level circuit weights
    def k_pos(self):
        return torch.relu(self.W)

    def k_neg(self):
        return torch.relu(-self.W)

    def dk_pos(self):
        return (self.W > 0).to(self.W.dtype)

    def dk_neg(self):
        return -(self.W < 0).to(self.W.dtype)

    def v_bias_pos(self):
        return torch.relu(self.v_bias)

    def v_bias_neg(self):
        return torch.relu(-self.v_bias)

    def dv_bias_pos(self):
        return (self.v_bias > 0).to(self.v_bias.dtype)

    def dv_bias_neg(self):
        return -(self.v_bias < 0).to(self.v_bias.dtype)

    # ***** Get high-level circuit bias
    def h_bias_pos(self):
        return torch.relu(self.h_bias)

    def h_bias_neg(self):
        return torch.relu(-self.h_bias)

    def dh_bias_pos(self):
        return (self.h_bias > 0).to(self.h_bias.dtype)

    def dh_bias_neg(self):
        return -(self.h_bias < 0).to(self.h_bias.dtype)

    # **** PLOTTING
    def plot_weights(self, t):
        Ndata = self.W.shape[0]
        # Reshape the matrix into a 3D array
        data_3d = self.W.detach().cpu().numpy().reshape(Ndata, 28, 28)
        # Determine the number of rows and columns for the subplot grid
        num_rows = int(np.ceil(np.sqrt(Ndata)))
        num_cols = int(np.ceil(Ndata / num_rows))
        # Create a figure and axis for the plot
        fig, ax = plt.subplots(nrows=num_rows,
                               ncols=num_cols,
                               figsize=(10, 10))
        # Iterate over the submatrices and plot them
        for i in range(Ndata):
            row = i // num_cols
            col = i % num_cols
            ax[row, col].imshow(data_3d[i], cmap='magma')
            ax[row, col].axis('off')
        # Remove empty subplots if the number of submatrices doesn't fill the entire grid
        if num_rows * num_cols > Ndata:
            for i in range(Ndata, num_rows * num_cols):
                row = i // num_cols
                col = i % num_cols
                fig.delaxes(ax[row, col])
        # Adjust the spacing between subplots
        plt.suptitle('Weights epoch {}'.format(t))
        plt.subplots_adjust(wspace=0.05, hspace=0.05, top=0.9)
        # Get the minimum and maximum values from the data
        vmin = np.min(self.W.detach().cpu().numpy())
        vmax = np.max(self.W.detach().cpu().numpy())
        # Create a dummy image for the colorbar
        dummy_img = np.zeros((1, 1))  # Dummy image with all zeros
        # Add a colorbar using the dummy image as the mappable
        cax = fig.add_axes([0.93, 0.15, 0.02, 0.7])  # Position of the colorbar
        plt.colorbar(plt.imshow(dummy_img, cmap='magma', vmin=vmin, vmax=vmax),
                     cax=cax)
        # Adjust the height of the colorbar axes to match the height of the figure
        cax.set_aspect('auto')

    # ** Plotting bias
    def plot_bias(self, t):
        h_bias = self.h_bias.detach().cpu().numpy()
        v_bias = self.v_bias.detach().cpu().numpy()
        # Set up the figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        # Plot histogram for hidden biases
        ax1.hist(h_bias, bins=20, color='blue', edgecolor='black')
        ax1.set_xlabel('Values')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Hidden Biases epoch {}'.format(t))
        # Plot histogram for visible biases
        ax2.hist(v_bias, bins=20, color='red', edgecolor='black')
        ax2.set_xlabel('Values')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Visible Biases epoch {}'.format(t))
        # Adjust layout for better readability
        plt.tight_layout()


#############********************************
# Class for the convolutional RBM model
class convolutional_RBM(RBM):

    def __init__(
        self,
        model_name,
        n_vis=784,
        n_hin=50,
        k=1,
        lr=0.01,
        max_epochs=200000,
        minMax_W=(-100, 100),
        energy_type='hopfield',
        optimizer='Adam',
        regularization=False,
        l1_factor=1e-7,
        l2_factor=1e-7,
        ground_v=1,
        ground_h=1,
        batch_size=64,
        train_algo='CD',
        centering=False,
        average_data=None,
        sampling_model_beta=1,
        nrelu=False,
        mytype=torch.double,
        half_kernel_size=1,
    ):
        # Initialize base class parameters
        super(convolutional_RBM, self).__init__(
            model_name,
            n_vis,
            n_vis,
            k,
            lr,
            max_epochs,
            minMax_W,
            energy_type,
            optimizer,
            regularization,
            l1_factor,
            l2_factor,
            ground_v,
            ground_h,
            batch_size,
            train_algo,
            centering,
            average_data,
            sampling_model_beta,
            nrelu,
            mytype,
        )
        # Initialize new parameters
        self.half_kernel_size = half_kernel_size
        # self.W = self.W.to_sparse()

        # Create the adjacency matrix for each input data,
        # assuming that they are stored as row_i + N*column_j
        # * Note that we also assume closed boundaries
        self.nvis_sqrt = int(np.sqrt(self.n_visible))
        self.adjacency_mat = torch.zeros((n_vis, n_vis), device=self.device)
        for i in range(n_vis):
            column = int(np.floor(i / self.nvis_sqrt))
            row = int(i - self.nvis_sqrt * column)
            self.add_neigh(self.adjacency_mat, row, column)
        # self.adjacency_mat = self.adjacency_mat.to_sparse()

    def add_neigh(self, adjacency_mat, row, column):
        my_id = row + column * self.nvis_sqrt
        for i in range(row - self.half_kernel_size,
                       row + self.half_kernel_size + 1):
            for j in range(column - self.half_kernel_size,
                           column + self.half_kernel_size + 1):
                if i >= 0 and i < self.nvis_sqrt and j >= 0 and j < self.nvis_sqrt:
                    neigh_id = i + j * self.nvis_sqrt
                    adjacency_mat[my_id, neigh_id] = 1

    def after_step_keepup(self):
        if isinstance(self, convolutional_RBM):
            self.W = self.adjacency_mat * self.W

        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables()
        else:
            self.W_t = self.W.t()


################################################################
# Class for the fitlering RBM model
class filtering_RBM(RBM):

    def __init__(
        self,
        model_name,
        n_vis=784,
        n_hin=50,
        k=1,
        lr=0.01,
        max_epochs=200000,
        minMax_W=(-100, 100),
        energy_type='hopfield',
        optimizer='Adam',
        regularization=False,
        l1_factor=1e-7,
        l2_factor=1e-7,
        ground_v=1,
        ground_h=1,
        batch_size=64,
        train_algo='CD',
        centering=False,
        average_data=None,
        sampling_model_beta=1,
        nrelu=False,
        use_mask=False,
        mytype=torch.double,
        is_conditional=False,
    ):
        # Initialize base class parameters
        super(convolutional_RBM, self).__init__(
            model_name,
            n_vis,
            n_vis,
            k,
            lr,
            max_epochs,
            minMax_W,
            energy_type,
            optimizer,
            regularization,
            l1_factor,
            l2_factor,
            ground_v,
            ground_h,
            batch_size,
            train_algo,
            centering,
            average_data,
            sampling_model_beta,
            nrelu,
            mytype,
        )
        # Initialize new parameters
        # If true, add conditional layer
        self.is_conditional = is_conditional
        # Initialize weights
        if is_conditional:
            self.D = torch.randn(
                (
                    n_hin,
                    n_vis,
                ),
                dtype=self.mytype,
                device=self.device,
            )
            self.D = self.D.contiguous()
            init.xavier_normal_(self.D)

        # use mask for recommendation systems
        self.use_mask = use_mask

    # Function to average the gradients, excluding the masked elements
    def maskedmean(self, x):
        mask_sum = (x != 0).to(torch.int).sum(dim=0)

        # Check if any element in mask_sum is zero
        if (mask_sum == 0).any():
            # print("Warning: Zero elements in mask_sum. Replacing with 1.")
            # Replace zero elements with 1 in mask_sum
            mask_sum = torch.where(mask_sum == 0, 1, mask_sum)

        return torch.div(x.sum(dim=0), mask_sum)

    def tstep_keepup(self):
        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables(self.is_conditional)
        else:
            self.W_t = self.W.t()
        if self.is_conditional:
            self.D_t = self.D.t()

    def _update_circuit_variables(self):
        self._k_pos = self.k_pos()
        self._k_neg = self.k_neg()
        self._v_bias_pos = self.v_bias_pos()
        self._v_bias_neg = self.v_bias_neg()
        self._h_bias_pos = self.h_bias_pos()
        self._h_bias_neg = self.h_bias_neg()
        self._k_diff = self._k_pos - self._k_neg
        self._k_diff_t = self._k_diff.t()
        self._v_bias_pos_diff = self._v_bias_pos * (0.5 - self.ground_v)
        self._v_bias_neg_diff = self._v_bias_neg * (0.5 - self.ground_v)
        self._h_bias_pos_diff = self._h_bias_pos * (0.5 - self.ground_h)
        self._h_bias_neg_diff = self._h_bias_neg * (0.5 - self.ground_h)
        self._vb_posneg = -self._v_bias_pos_diff + self._v_bias_neg_diff
        self._hb_posneg = -self._h_bias_pos_diff + self._h_bias_neg_diff
        if self.is_conditional:
            self._D_pos = self.D_pos()
            self._D_neg = self.D_neg()
            self._D_diff = self._D_pos - self._D_neg
            self._D_diff_t = self._D_diff.t()

    def SGD_update(
        self,
        partial_gradient_data,
        partial_gradient_model,
    ):
        # Get the correct gradients
        dEdW_data = partial_gradient_data[0]
        dEdW_model = partial_gradient_model[0]
        dEdv_bias_data = partial_gradient_data[1]
        dEdv_bias_model = partial_gradient_model[1]
        dEdh_bias_data = partial_gradient_data[2]
        dEdh_bias_model = partial_gradient_model[2]
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        if self.is_conditional:
            dEdD_data = partial_gradient_data[3]
            dEdD_model = partial_gradient_model[3]
            dD = -dEdD_data + dEdD_model
        if self.centering:
            dv = dv - torch.matmul(self.oh, dW)
            dh = dh - torch.matmul(self.ov, dW.t())
        # Add regularization term
        if self.regularization == 'l2':
            dW += self.l2 * 2 * self.W
            dv += self.l2 * 2 * self.v_bias
            dh += self.l2 * 2 * self.h_bias
        elif self.regularization == 'l1':
            dW += self.l1 * torch.sign(self.W)
            dv += self.l1 * torch.sign(self.v_bias)
            dh += self.l1 * torch.sign(self.h_bias)
        # Update parameters in-place
        # and clip
        if self.is_conditional:
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(
                dh) + torch.norm(dD)
        else:
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(dh)
        myclip = (self.lr * 10.0) / gnorm if gnorm > 10 else self.lr
        self.W.add_(myclip * dW)
        self.v_bias.add_(myclip * dv)
        self.h_bias.add_(myclip * dh)
        if self.is_conditional:
            self.D.add_(self.lr * dD * myclip)

    def delta_eh(self, v):
        if self.energy_type == 'hopfield':
            if self.use_mask:
                return self._delta_eh_hopfield_masked(v)
            else:
                return self._delta_eh_hopfield(v)
        elif self.energy_type == 'linear_circuit_4':
            if self.use_mask:
                return self._delta_eh_linear_circuit_4_masked(v)
            else:
                return self._delta_eh_linear_circuit_4(v)

    def delta_ev(self, h):
        if self.energy_type == 'hopfield':
            if self.use_mask:
                return self._delta_ev_hopfield_masked(h)
            else:
                return self._delta_ev_hopfield(h)
        elif self.energy_type == 'linear_circuit_4':
            if self.use_mask:
                return self._delta_ev_linear_circuit_4_masked(h)
            else:
                return self._delta_ev_linear_circuit_4(h)

    # **** Hopfield transfer functions
    def _delta_eh_hopfield(self, v):
        return torch.mm(v, self.W_t) + self.h_bias

    def _delta_ev_hopfield(self, h):
        return torch.mm(h, self.W) + self.v_bias

    # **** (masked) Hopfield transfer functions
    def _delta_eh_hopfield_masked(self, v):
        #        Wtm = self.W_t *self.mask.unsqueeze(-1)
        #        return torch.bmm(v.unsqueeze(1), Wtm).squeeze(1) + self.h_bias + torch.mm(self.mask , self.D_t)
        if self.is_conditional:
            return (torch.mm(v * self.mask, self.W_t) + self.h_bias +
                    torch.mm(self.mask, self.D_t))
        else:
            return torch.mm(v * self.mask, self.W_t) + self.h_bias

    def _delta_ev_hopfield_masked(self, h):
        return torch.mm(h, self.W) + self.v_bias

    # **** linear_circuit_4 transfer functions
    def _delta_ev_linear_circuit_4(self, h):
        return torch.mm(torch.mul(h, 2) - 1, self._k_diff) + self._vb_posneg

    def _delta_eh_linear_circuit_4(self, v):
        return torch.mm(torch.mul(v, 2) - 1, self._k_diff_t) + self._hb_posneg

    # **** (masked) linear_circuit_4 transfer functions
    def _delta_ev_linear_circuit_4_masked(self, h):
        return torch.mm(torch.mul(h, 2) - 1, self._k_diff) + self._vb_posneg

    def _delta_eh_linear_circuit_4_masked(self, v):
        if self.is_conditional:
            return (torch.mm(torch.mul(v * self.mask, 2) - 1, self._k_diff_t) +
                    self._hb_posneg +
                    torch.mm(torch.mul(self.mask, 2) - 1, self._D_diff_t))
        else:
            return (torch.mm(torch.mul(v * self.mask, 2) - 1, self._k_diff_t) +
                    self._hb_posneg)

    def derivatives_hopfield(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        if self.centering:
            dEdW = -torch.einsum('ij,ik->ijk', h - self.oh, v - self.ov)
        else:
            dEdW = -torch.einsum('ij,ik->ijk', h, v * self.mask)
        dEdv_bias = -v * self.mask
        dEdh_bias = -h
        if self.is_conditional:
            dEdD = -torch.einsum('ij,ik->ijk', h, self.mask)
        # They have to be renormalized according to the size of the mask
        # masksizefactor = self.n_visible/self.mask.sum(-1)
        if self.is_conditional:
            return (dEdW, dEdv_bias, dEdh_bias, dEdD)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, dEdD#*masksizefactor.unsqueeze(1).unsqueeze(1)
        else:
            return (dEdW, dEdv_bias, dEdh_bias, None)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, None

    def derivatives_linear_circuit_4(self, v, h):
        torch.square(v).unsqueeze(1)
        torch.square(1 - v).unsqueeze(1)
        negh = 1 - h
        h_square = torch.square(h).unsqueeze(2)
        hneg_square = torch.square(negh).unsqueeze(2)
        v_masked = v * self.mask
        negv_masked = 1 - v_masked
        v_square_masked = torch.square(v_masked).unsqueeze(1)
        vneg_square_masked = torch.square(1 - v_masked).unsqueeze(1)

        ein_h_vm = torch.einsum('ij,ik->ijk', h, v_masked)
        ein_negh_vm = torch.einsum('ij,ik->ijk', negh, v_masked)
        ein_h_negvm = torch.einsum('ij,ik->ijk', h, negv_masked)
        ein_negh_negvm = torch.einsum('ij,ik->ijk', negh, negv_masked)

        dEdk_pos = 0.5 * (
            (-2 * ein_h_vm + v_square_masked + h_square) +
            (-2 * ein_negh_negvm + vneg_square_masked + hneg_square))
        dEdk_neg = 0.5 * ((-2 * ein_h_negvm + vneg_square_masked + h_square) +
                          (-2 * ein_negh_vm + v_square_masked + hneg_square))
        dkdw_pos = self.dk_pos().unsqueeze(0)
        dkdw_neg = self.dk_neg().unsqueeze(0)
        dEdW = dEdk_pos * dkdw_pos + dEdk_neg * dkdw_neg

        dEdv_bias_pos = -self.ground_v * v_masked + 0.5 * torch.square(
            v_masked)
        dEdv_bias_neg = -self.ground_v * negv_masked + 0.5 * torch.square(
            negv_masked)
        dv_biasdv_pos = self.dv_bias_pos().unsqueeze(0)
        dv_biasdv_neg = self.dv_bias_neg().unsqueeze(0)
        dEdv_bias = dEdv_bias_pos * dv_biasdv_pos + dEdv_bias_neg * dv_biasdv_neg

        dEdh_bias_pos = -self.ground_h * h + 0.5 * torch.square(h)
        dEdh_bias_neg = -self.ground_h * (negh) + 0.5 * torch.square(negh)
        dh_biasdh_pos = self.dh_bias_pos().unsqueeze(0)
        dh_biasdh_neg = self.dh_bias_neg().unsqueeze(0)
        dEdh_bias = dEdh_bias_pos * dh_biasdh_pos + dEdh_bias_neg * dh_biasdh_neg

        if self.is_conditional:
            ## No this gradient is wrong! (this is same shape as W, but it is not like this in C-RBM)
            negm = 1 - self.mask
            m_square = torch.square(self.mask).unsqueeze(1)
            mneg_square = torch.square(negm).unsqueeze(1)

            ein_h_m = torch.einsum('ij,ik->ijk', h, self.mask)
            ein_h_negm = torch.einsum('ij,ik->ijk', h, negm)
            ein_negh_m = torch.einsum('ij,ik->ijk', negh, self.mask)
            ein_negh_negm = torch.einsum('ij,ik->ijk', negh, negm)

            dEdD_pos = 0.5 * ((-2 * ein_h_m + m_square + h_square) +
                              (-2 * ein_negh_negm + mneg_square + hneg_square))
            dEdD_neg = 0.5 * ((-2 * ein_h_negm + mneg_square + h_square) +
                              (-2 * ein_negh_m + m_square + hneg_square))
            dDdw_pos = self.dD_pos().unsqueeze(0)
            dDdw_neg = self.dD_neg().unsqueeze(0)
            dEdD = dEdD_pos * dDdw_pos + dEdD_neg * dDdw_neg

            # negm = 1-self.mask
            # dEdD = torch.einsum('ij,ik->ijk',dEdh_bias_pos*dh_biasdh_pos, self.mask) + torch.einsum('ij,ik->ijk',dEdh_bias_neg*dh_biasdh_neg, negm)

        # They have to be renormalized according to the size of the mask
        # masksizefactor = self.n_visible/self.mask.sum(-1)
        if self.is_conditional:
            return (dEdW, dEdv_bias, dEdh_bias, dEdD)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, dEdD#*masksizefactor.unsqueeze(1).unsqueeze(1)
        else:
            return (dEdW, dEdv_bias, dEdh_bias, None)
            # return dEdW*masksizefactor.unsqueeze(1).unsqueeze(1), dEdv_bias*masksizefactor.unsqueeze(1), dEdh_bias, None

    # ***** Get high-level conditional weights
    def D_pos(self):
        return torch.relu(self.D)

    def D_neg(self):
        return torch.relu(-self.D)

    def dD_pos(self):
        return (self.D > 0).to(self.D.dtype)

    def dD_neg(self):
        return -(self.D < 0).to(self.D.dtype)


################################
# Class for continuous RBM, used for CelebA
class continuous_RBM(RBM):

    def __init__(
        self,
        model_name,
        n_vis=784,
        n_hin=50,
        k=1,
        lr=0.01,
        max_epochs=200000,
        minMax_W=(-100, 100),
        energy_type='hopfield',
        optimizer='Adam',
        regularization=False,
        l1_factor=1e-7,
        l2_factor=1e-7,
        ground_v=1,
        ground_h=1,
        batch_size=64,
        train_algo='CD',
        centering=False,
        average_data=None,
        sampling_model_beta=1,
        nrelu=False,
        mytype=torch.double,
    ):
        # Initialize base class parameters
        super(continuous_RBM, self).__init__(
            model_name,
            n_vis,
            n_vis,
            k,
            lr,
            max_epochs,
            minMax_W,
            energy_type,
            optimizer,
            regularization,
            l1_factor,
            l2_factor,
            ground_v,
            ground_h,
            batch_size,
            train_algo,
            centering,
            average_data,
            sampling_model_beta,
            nrelu,
            mytype,
        )
        # Initialize new parameters
        self.logsigma_sq = torch.zeros((n_vis, ),
                                       dtype=self.mytype,
                                       device=self.device)

    def pretrain(self, pretrained_model):
        # Check if you have model load points
        filename_list = glob.glob(
            'model_states/{}_t*.pkl'.format(pretrained_model))
        if len(filename_list) > 0:
            all_loadpoints = sorted([
                int(x.split('_t')[-1].split('.pkl')[0]) for x in filename_list
            ])
            last_epoch = all_loadpoints[-1]
            print('** Using as pretraining model {} at epoch {}'.format(
                pretrained_model, last_epoch))
            with open(
                    'model_states/{}_t{}.pkl'.format(pretrained_model,
                                                     last_epoch),
                    'rb') as file:
                temp_model = pickle.load(file)
                # *** Import pretrained parameters
                self.W = temp_model.W.to(self.mytype)
                self.h_bias = temp_model.h_bias.to(self.mytype)
                self.v_bias = temp_model.v_bias.to(self.mytype)
                self.logsigma_sq = temp_model.logsigma_sq.to(self.mytype)
        else:
            print('** No load points for {}'.format(pretrained_model))

    def v_to_h(self, v, beta=None):
        if beta is None:
            beta = self.model_beta
        return self.GaussBernoulli_v_to_h(v, beta)

    def h_to_v(self, h, beta=None):
        if beta is None:
            beta = self.model_beta
        return self.GaussBernoulli_h_to_v(h, beta)

    def GaussBernoulli_v_to_h(self, v, beta):
        if self.energy_type == 'hopfield':
            p_h = self._prob_h_given_v(v / self.sigma_sq, beta)
        else:
            p_h = self._prob_h_given_v(v, beta)
        sample_h = torch.bernoulli(p_h)
        return p_h, sample_h

    def GaussBernoulli_h_to_v(self, h, beta):
        if self.energy_type == 'hopfield':
            mean = self.delta_ev(h)
            sample_v = mean + torch.randn_like(mean) * self.sigma
        else:
            mean = self.delta_ev(h) * self.sigma_sq
            sample_v = mean + torch.randn_like(mean) * self.sigma

        return None, sample_v

    def tstep_keepup(self):
        if self.energy_type != 'hopfield':
            self.clip_weights()
            self.clip_bias()
            self._update_circuit_variables()
        else:
            self.W_t = self.W.t()
            self.sigma_sq = torch.exp(self.logsigma_sq)
            self.sigma = torch.sqrt(self.sigma_sq)

    def SGD_update(
        self,
        partial_gradient_data,
        partial_gradient_model,
    ):
        # Get the correct gradients
        dEdW_data = partial_gradient_data[0]
        dEdW_model = partial_gradient_model[0]
        dEdv_bias_data = partial_gradient_data[1]
        dEdv_bias_model = partial_gradient_model[1]
        dEdh_bias_data = partial_gradient_data[2]
        dEdh_bias_model = partial_gradient_model[2]
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        if self.energy_type == 'hopfield':
            dEds_data = partial_gradient_data[3]
            dEds_model = partial_gradient_model[3]
            ds = -dEds_data + dEds_model
        # Update parameters in-place
        # and clip
        if self.energy_type == 'hopfield':
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(
                dh) + torch.norm(ds)
        else:
            gnorm = torch.norm(dW) + torch.norm(dv) + torch.norm(dh)
        myclip = (self.lr * 10.0) / gnorm if gnorm > 10 else self.lr
        self.W.add_(dW * myclip)
        self.v_bias.add_(dv * myclip)
        self.h_bias.add_(dh * myclip)
        if self.energy_type == 'hopfield':
            self.logsigma_sq.add_(ds * myclip)

    def generate(self,
                 n_samples,
                 k,
                 h_binarized=True,
                 from_visible=False,
                 beta=None):
        if beta is None:
            beta = self.model_beta
        self.tstep_keepup()
        if from_visible:
            # generate from continuous random visible
            v = torch.randn(size=(n_samples, self.n_visible),
                            device=self.device,
                            dtype=self.mytype)
        else:
            if h_binarized:
                h = torch.randint(
                    high=2,
                    size=(n_samples, self.n_hidden),
                    device=self.device,
                    dtype=self.mytype,
                )
            else:
                h = torch.rand(n_samples,
                               self.n_hidden,
                               device=self.device,
                               dtype=self.mytype)
            _, v = self.h_to_v(h)
        v_model = self.forward(v, k, beta)
        return v_model.detach().cpu().numpy()

    def _update_circuit_variables(self):
        self._k_pos = self.k_pos()
        self._k_neg = self.k_neg()
        self._v_bias_pos = self.v_bias_pos()
        self._v_bias_neg = self.v_bias_neg()
        self._h_bias_pos = self.h_bias_pos()
        self._h_bias_neg = self.h_bias_neg()
        self._k_diff = self._k_pos - self._k_neg
        self._k_diff_t = self._k_diff.t()
        self._v_bias_pos_diff = self._v_bias_pos * (0.5 - self.ground_v)
        self._v_bias_neg_diff = self._v_bias_neg * (0.5 - self.ground_v)
        self._h_bias_pos_diff = self._h_bias_pos * (0.5 - self.ground_h)
        self._h_bias_neg_diff = self._h_bias_neg * (0.5 - self.ground_h)
        self._vb_posneg = -self._v_bias_pos_diff + self._v_bias_neg_diff
        self._hb_posneg = -self._h_bias_pos_diff + self._h_bias_neg_diff
        # for the gaussian units
        self.sigma = torch.pow(
            self._k_pos.sum(0) + self._k_neg.sum(0) + self._v_bias_pos, -0.5)
        self.sigma_sq = self.sigma * self.sigma

    def derivatives_hopfield(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        v_diff = v - self.v_bias
        v_over_sigma = v / self.sigma_sq

        if self.centering:
            dEdW = -torch.einsum('ij,ik->ijk', h - self.oh,
                                 v - self.ov) / self.sigma_sq
        else:
            dEdW = -torch.einsum('ij,ik->ijk', h, v_over_sigma)
        dEdv_bias = -(v_diff) / self.sigma_sq
        dEdh_bias = -h
        # dEds = -( (v-self.v_bias)**2/self.sigma_sq.unsqueeze(0)*0.5 - torch.mm(h,self.W)*v/self.sigma_sq.unsqueeze(0))
        dEds = -0.5 * (v_diff**2) / self.sigma_sq + torch.mm(
            h, self.W) * v_over_sigma
        return (dEdW, dEdv_bias, dEdh_bias, dEds)

    def derivatives_linear_circuit_4(self, v, h):
        v_square = torch.square(v).unsqueeze(1)
        vneg_square = torch.square(1 - v).unsqueeze(1)

        h_square = torch.square(h).unsqueeze(2)
        hneg_square = torch.square(1 - h).unsqueeze(2)

        dEdk_pos = (-torch.einsum('ij,ik->ijk', h, v) + 0.5 * v_square + 0.5 *
                    h_square) + (-torch.einsum('ij,ik->ijk', 1 - h, 1 - v) +
                                 0.5 * vneg_square + 0.5 * hneg_square)
        dEdk_neg = (-torch.einsum('ij,ik->ijk', h, 1 - v) + 0.5 * vneg_square +
                    0.5 * h_square) + (-torch.einsum('ij,ik->ijk', 1 - h, v) +
                                       0.5 * v_square + 0.5 * hneg_square)

        dkdw_pos = self.dk_pos().unsqueeze(0)
        dkdw_neg = self.dk_neg().unsqueeze(0)

        dEdW = dEdk_pos * dkdw_pos + dEdk_neg * dkdw_neg

        dEdv_bias_pos = -self.ground_v * v + 0.5 * torch.square(v)
        dEdv_bias_neg = -self.ground_v * (1 - v) + 0.5 * torch.square(1 - v)

        dv_biasdv_pos = self.dv_bias_pos().unsqueeze(0)
        dv_biasdv_neg = self.dv_bias_neg().unsqueeze(0)

        dEdv_bias = dEdv_bias_pos * dv_biasdv_pos + dEdv_bias_neg * dv_biasdv_neg
        dEdh_bias_pos = -self.ground_h * h + 0.5 * torch.square(h)
        dEdh_bias_neg = -self.ground_h * (1 - h) + 0.5 * torch.square(1 - h)

        dh_biasdh_pos = self.dh_bias_pos().unsqueeze(0)
        dh_biasdh_neg = self.dh_bias_neg().unsqueeze(0)
        dEdh_bias = dEdh_bias_pos * dh_biasdh_pos + dEdh_bias_neg * dh_biasdh_neg

        return (dEdW, dEdv_bias, dEdh_bias, None)
