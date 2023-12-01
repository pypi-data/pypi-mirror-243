import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import glob
from rkm.circuit_utils import Circuit


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
    energy : str
        Type of energy function to use. Options are 'hopfield' and 'linear_circuit_i' with i=1,2,3
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
    energy : str
        Type of energy function to use. Options are 'hopfield' and 'linear_circuit_i' with i=1,2,3,5
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
        minMax_W=(-100, 100),
        energy='hopfield',
        optimizer='Adam',
        regularization=False,
        l1_factor=1e-7,
        l2_factor=1e-7,
        ground_v=1,
        ground_h=1,
    ):
        self.name = model_name
        self.device = 'cpu'
        self.k = k
        self.min_W, self.max_W = minMax_W
        self.energy = energy
        self.n_hidden = n_hin
        self.n_visible = n_vis
        self.epoch = 0
        self.errors_free_energy = []
        self.errors_loss = []
        self.regularization = regularization
        if self.regularization == 'l1':
            self.l1 = l1_factor
        elif self.regularization == 'l2':
            self.l2 = l2_factor
        self.optimizer = optimizer
        if self.optimizer == 'Adam':
            # Adam's momenta
            self.m_dW, self.m_dv, self.m_dh = 0, 0, 0
            self.v_dW, self.v_dv, self.v_dh = 0, 0, 0
            # Adam's parameters
            self.beta1 = 0.9
            self.beta2 = 0.999
            self.epsilon = 1e-8
        if self.energy == 'linear_circuit_4' or 'linear_circuit_5':
            # set the ground voltages. Using -1 naturally includes a hopfield term
            self.ground_v = ground_v
            self.ground_h = ground_h

        print('*** Initializing {}'.format(self.name))
        self.W = self.max_W * 0.1 * np.random.randn(n_hin, n_vis)
        self.v_bias = np.random.randn(n_vis)
        self.h_bias = np.random.randn(n_hin)

        if self.energy == 'linear_circuit_5':
            import networkx as nx
            # define the physical circuit for the minimization
            # NO NEED TO MAP TO THE CONDUCTANCES HERE. TO BE UPDATED
            # Extract the conductances from self and create a new graph with the connectivity of the
            # k_plus = self.k_pos()
            # k_minus = self.k_neg()
            # q_plus = self.v_bias_pos()
            # q_minus = self.v_bias_neg()
            # c_plus = self.h_bias_pos()
            # c_minus = self.h_bias_neg()

            # create an empty graph
            self.circuit = nx.Graph()

            # add two visible nodes for each original visible node and connect them to the hidden nodes and the bias node
            # One loop per each set of nodes to ensure the correct order in networkx
            for i in range(self.n_visible):
                self.circuit.add_node(i)  # positive visible node
            for i in range(self.n_visible):
                self.circuit.add_node(n_vis + i)  # negative visible node
            for j in range(self.n_hidden):
                self.circuit.add_node(2 * n_vis + j)  # positive hidden node
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
                    self.circuit.add_edge(i, 2 * n_vis + n_hin +
                                          j)  # , conductance=k_minus[j][i])
                    self.circuit.add_edge(n_vis + i, 2 * n_vis +
                                          j)  # , conductance=k_minus[j][i])
                    self.circuit.add_edge(n_vis + i, 2 * n_vis + n_hin +
                                          j)  # , conductance=k_plus[j][i])
                self.circuit.add_edge(i, 2 * n_vis +
                                      2 * n_hin)  # , conductance=q_plus[i])
                self.circuit.add_edge(n_vis + i, 2 * n_vis +
                                      2 * n_hin)  # , conductance=q_minus[i])

            for j in range(self.n_hidden
                           ):  # connect the bias node to all hidden nodes
                self.circuit.add_edge(2 * n_vis + j, 2 * n_vis + 2 * n_hin +
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
                (max_pos_vis - min_pos_vis) for pos in adjusted_positions_vis
            ]

            min_pos_hid = min(adjusted_positions_hid)
            max_pos_hid = max(adjusted_positions_hid)
            normalized_positions_hid = [
                (pos - min_pos_hid) * (self.n_hidden - 1) /
                (max_pos_hid - min_pos_hid) for pos in adjusted_positions_hid
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
                n_vis + i: (1, normalized_positions_vis[2 * i + 1] - shift_vis)
                for i in range(n_vis)
            })
            pos.update({
                2 * n_vis + j: (2, normalized_positions_hid[2 * j] - shift_hid)
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

            # Define the constraint matrix for clamped visible nodes and clamped hidden nodes
            # get the array of all visible, hidden, and bias nodes
            # v_nodes_plus = [node for node in list(self.circuit.graph.nodes) if node[1] == 'v' and node[-2] == '+']
            # v_nodes_minus = [node for node in list(self.circuit.graph.nodes) if node[1] == 'v' and node[-2] == '-']
            # h_nodes_plus = [node for node in list(self.circuit.graph.nodes) if node[1] == 'h' and node[-2] == '+']
            # h_nodes_minus = [node for node in list(self.circuit.graph.nodes) if node[1] == 'h' and node[-2] == '-']
            # g_nodes = [node for node in list(self.circuit.graph.nodes) if node[1] == 'g']
            # v_nodes_plus = np.arange(self.n_visible)
            # v_nodes_minus = np.arange(self.n_visible, 2*self.n_visible)
            # h_nodes_plus = np.arange(2*self.n_visible, 2*self.n_visible+self.n_hidden)
            # h_nodes_minus = np.arange(2*self.n_visible+self.n_hidden, 2*self.n_visible+2*self.n_hidden)
            # g_nodes = np.arange(2*self.n_visible+2*self.n_hidden, 2*self.n_visible+2*self.n_hidden+2)

            # find the indices of the visible nodes, hidden nodes, and bias nodes
            # self.v_indices_plus = [list(self.circuit.graph.nodes).index(node) for node in v_nodes_plus]
            # self.v_indices_minus = [list(self.circuit.graph.nodes).index(node) for node in v_nodes_minus]
            # self.h_indices_plus = [list(self.circuit.graph.nodes).index(node) for node in h_nodes_plus]
            # self.h_indices_minus = [list(self.circuit.graph.nodes).index(node) for node in h_nodes_minus]
            # self.g_indices = [list(self.circuit.graph.nodes).index(node) for node in g_nodes]

            # Store the indices of the visible nodes, hidden nodes, and bias nodes
            self.v_indices_plus = np.arange(self.n_visible)
            self.v_indices_minus = np.arange(self.n_visible,
                                             2 * self.n_visible)
            self.h_indices_plus = np.arange(2 * self.n_visible,
                                            2 * self.n_visible + self.n_hidden)
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

            AA, BB = np.meshgrid(self.v_indices_minus, self.h_indices_minus)
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

    def sample_from_p(self, p):
        return np.random.binomial(1, p, size=p.shape)

    def v_to_h(self, v):
        p_h = self._prob_h_given_v(v)
        sample_h = self.sample_from_p(p_h)
        return p_h, sample_h

    def h_to_v(self, h):
        p_v = self._prob_v_given_h(h)
        sample_v = self.sample_from_p(p_v)
        return p_v, sample_v

    def _free_energy_hopfield(self, v):
        vbias_term = np.dot(v, self.v_bias)
        wx_b = np.dot(v, self.W.T) + self.h_bias
        hidden_term = np.sum(np.log(1 + np.exp(wx_b)), axis=1)
        return -hidden_term - vbias_term

    def forward(self, v):
        pre_h1, h1 = self.v_to_h(v)

        h_ = h1
        for _ in range(self.k):
            pre_v_, v_ = self.h_to_v(h_)
            pre_h_, h_ = self.v_to_h(v_)

        return v, v_

    def train(self,
              train_data,
              max_epochs,
              lr,
              batches_per_epoch,
              batch_size,
              measure_F=False):
        """Train the model using the given data and parameters."""
        self.lr = lr
        if batches_per_epoch == -1:
            batches_per_epoch = int(train_data.shape[0] / batch_size)
        elif batches_per_epoch > int(train_data.shape[0] / batch_size):
            print(
                'Error: requested to use {} batches of size {} at every epoch, but only {} datapoints available'
                .format(batches_per_epoch, batch_size, train_data.shape[0]))
            return 0
        while self.epoch < max_epochs:
            loss_ = []
            free_energy_difference_ = []
            np.random.shuffle(train_data)
            for i in range(batches_per_epoch):
                if self.energy == 'linear_circuit_5':
                    # self._weights_to_conductances()
                    # set the conductances in the same order as they are internally stored
                    # conductances = [self.circuit.graph.edges[e]['conductance'] for e in self.circuit.graph.edges]
                    self.circuit.setConductances(
                        self._weights_to_conductances())
                batch = train_data[i * batch_size:(i + 1) * batch_size]
                v_data, v_model = self.forward(batch)

                # performance of the machine
                free_energy_difference = self.free_energy(
                    v_data) - self.free_energy(v_model)
                loss = (v_data - v_model)**2

                # Compute gradients
                h_data = self.v_to_h(v_data)[0]
                h_model = self.v_to_h(v_model)[0]
                dEdW_data, dEdv_bias_data, dEdh_bias_data = self.derivatives(
                    v_data, h_data)
                dEdW_model, dEdv_bias_model, dEdh_bias_model = self.derivatives(
                    v_model, h_model)

                # Average over batch
                dEdW_data = np.mean(dEdW_data, axis=0)
                dEdv_bias_data = np.mean(dEdv_bias_data, axis=0)
                dEdh_bias_data = np.mean(dEdh_bias_data, axis=0)
                dEdW_model = np.mean(dEdW_model, axis=0)
                dEdv_bias_model = np.mean(dEdv_bias_model, axis=0)
                dEdh_bias_model = np.mean(dEdh_bias_model, axis=0)

                # Update weights and biases
                if self.optimizer == 'Adam':
                    self.Adam_update(
                        self.epoch + 1,
                        dEdW_data,
                        dEdW_model,
                        dEdv_bias_data,
                        dEdv_bias_model,
                        dEdh_bias_data,
                        dEdh_bias_model,
                    )
                elif self.optimizer == 'SGD':
                    self.SGD_update(
                        dEdW_data,
                        dEdW_model,
                        dEdv_bias_data,
                        dEdv_bias_model,
                        dEdh_bias_data,
                        dEdh_bias_model,
                    )
                else:
                    self.SGD_update(
                        dEdW_data,
                        dEdW_model,
                        dEdv_bias_data,
                        dEdv_bias_model,
                        dEdh_bias_data,
                        dEdh_bias_model,
                    )

                loss_.append(loss)
                free_energy_difference_.append(free_energy_difference)
                # if measure_F:
                #     free_energy_difference = self.free_energy(v_data) - self.free_energy(v_model)
                #     free_energy_difference_.append(free_energy_difference)

                if self.energy != 'hopfield':
                    self.clip_weights()
                    self.clip_bias()

            self.epoch += 1
            err_loss = np.mean(loss_)
            err_free = np.mean(free_energy_difference_)
            self.errors_loss.append(err_loss)
            self.errors_free_energy.append(err_free)
            print('Epoch: %d , Error_loss: %f, Error_freeE: %f' %
                  (self.epoch, err_loss, err_free))

            # Store the model state
            with open('model_states/{}_t{}.pkl'.format(self.name, self.epoch),
                      'wb') as file:
                pickle.dump(self, file)

        print('*** Training finished')

    def SGD_update(
        self,
        dEdW_data,
        dEdW_model,
        dEdv_bias_data,
        dEdv_bias_model,
        dEdh_bias_data,
        dEdh_bias_model,
    ):
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        # Add regularization term
        if self.regularization == 'l2':
            dW += self.l2 * 2 * self.W
            dv += self.l2 * 2 * self.v_bias
            dh += self.l2 * 2 * self.h_bias
        elif self.regularization == 'l1':
            dW += self.l1 * np.sign(self.W)
            dv += self.l1 * np.sign(self.v_bias)
            dh += self.l1 * np.sign(self.h_bias)
        self.W = self.W + self.lr * dW
        self.v_bias = self.v_bias + self.lr * dv
        self.h_bias = self.h_bias + self.lr * dh
        # return self.W, self.v_bias, self.h_bias

    def Adam_update(
        self,
        t,
        dEdW_data,
        dEdW_model,
        dEdv_bias_data,
        dEdv_bias_model,
        dEdh_bias_data,
        dEdh_bias_model,
    ):
        # Gradients
        dW = -dEdW_data + dEdW_model
        dv = -dEdv_bias_data + dEdv_bias_model
        dh = -dEdh_bias_data + dEdh_bias_model
        # Add regularization term
        if self.regularization == 'l2':
            dW += self.l2 * 2 * self.W
            dv += self.l2 * 2 * self.v_bias
            dh += self.l2 * 2 * self.h_bias
        elif self.regularization == 'l1':
            dW += self.l1 * np.sign(self.W)
            dv += self.l1 * np.sign(self.v_bias)
            dh += self.l1 * np.sign(self.h_bias)
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
                                     (np.sqrt(v_dW_corr) + self.epsilon))
        self.v_bias = self.v_bias + self.lr * (
            m_dv_corr / (np.sqrt(v_dv_corr) + self.epsilon))
        self.h_bias = self.h_bias + self.lr * (
            m_dh_corr / (np.sqrt(v_dh_corr) + self.epsilon))

    def reconstruct(self, data):
        v_data, v_model = self.forward(data)
        return v_data, v_model

    def generate(self, n_samples, h_binarized=False):
        if h_binarized:
            h = np.where(
                np.random.rand(n_samples, self.n_hidden) > 0.5, 1.0, 0.0)
        else:
            h = np.random.rand(n_samples, self.n_hidden)
        _, v = self.h_to_v(h)
        _, v_model = self.forward(v)
        return v_model

    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))

    def clip_weights(self):
        self.W = np.clip(self.W, self.min_W, self.max_W)

    def clip_bias(self):
        self.v_bias = np.clip(self.v_bias, self.min_W, self.max_W)
        self.h_bias = np.clip(self.h_bias, self.min_W, self.max_W)

    def _prob_h_given_v(self, v):
        if self.energy == 'linear_circuit_5':
            # PERFORM CIRCUIT MINIMIZATION
            sol = self._circuit_minimization_visible_clamped(v)
            # h = sol[:,self.h_indices_plus]
            h = (sol[:, self.h_indices_plus] + 1 -
                 sol[:, self.h_indices_minus]) / 2
            return self.sigmoid(h)
        return self.sigmoid(self.delta_eh(v))

    def _prob_v_given_h(self, h):
        if self.energy == 'linear_circuit_5':
            # PERFORM CIRCUIT MINIMIZATION
            sol = self._circuit_minimization_hidden_clamped(h)
            # v = sol[:,self.v_indices_plus]
            v = (sol[:, self.v_indices_plus] + 1 -
                 sol[:, self.v_indices_minus]) / 2
            return self.sigmoid(v)
        return self.sigmoid(self.delta_ev(h))

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

    def delta_eh(self, v):
        if self.energy == 'hopfield':
            return self._delta_eh_hopfield(v)
        # elif self.energy == 'linear_circuit_1':
        #     return self._delta_eh_linear_circuit_1(v)
        # elif self.energy == 'linear_circuit_2':
        #     return self._delta_eh_linear_circuit_2(v)
        # elif self.energy == 'linear_circuit_3':
        #     return self._delta_eh_linear_circuit_3(v)
        elif self.energy == 'linear_circuit_4':
            return self._delta_eh_linear_circuit_4(v)

    def delta_ev(self, h):
        if self.energy == 'hopfield':
            return self._delta_ev_hopfield(h)
        elif self.energy == 'linear_circuit_1':
            return self._delta_ev_linear_circuit_1(h)
        elif self.energy == 'linear_circuit_2':
            return self._delta_ev_linear_circuit_2(h)
        elif self.energy == 'linear_circuit_3':
            return self._delta_ev_linear_circuit_3(h)
        elif self.energy == 'linear_circuit_4':
            return self._delta_ev_linear_circuit_4(h)

    def _delta_eh_hopfield(self, v):
        return np.dot(v, self.W.T) + self.h_bias

    def _delta_ev_hopfield(self, h):
        return np.dot(h, self.W) + self.v_bias

    # def _delta_ev_linear_circuit_1(self,h):
    #     return np.dot(h-0.5,self.W) - 1.5*self.v_bias

    # def _delta_eh_linear_circuit_1(self,v):
    #     return np.dot(v-0.5,self.W.T) - 1.5*self.h_bias

    # def _delta_ev_linear_circuit_2(self,h):
    #     return np.dot(h-0.5,self.k_pos()-self.k_neg()) - 1.5*(self.v_bias_pos()-self.v_bias_neg())

    # def _delta_eh_linear_circuit_2(self,v):
    #     return np.dot(v-0.5,(self.k_pos()-self.k_neg()).T) - 1.5*self.h_bias_constrained()

    # def _delta_ev_linear_circuit_3(self,h):
    #     return np.dot(2*h-1,self.k_pos()-self.k_neg()) - 1.5*(self.v_bias_pos()-self.v_bias_neg())

    # def _delta_eh_linear_circuit_3(self,v):
    #     return np.dot(2*v-1,(self.k_pos()-self.k_neg()).T) - 1.5*(self.h_bias_pos()-self.h_bias_neg())

    def _delta_ev_linear_circuit_4(self, h):
        return (np.dot(2 * h - 1,
                       self.k_pos() - self.k_neg()) - self.v_bias_pos() *
                (0.5 - self.ground_v) + self.v_bias_neg() *
                (0.5 - self.ground_v))

    def _delta_eh_linear_circuit_4(self, v):
        return (np.dot(2 * v - 1, (self.k_pos() - self.k_neg()).T) -
                self.h_bias_pos() * (0.5 - self.ground_h) + self.h_bias_neg() *
                (0.5 - self.ground_h))

    def derivatives(self, v, h):
        if self.energy == 'hopfield':
            return self.derivatives_hopfield(v, h)
        elif self.energy == 'linear_circuit_1':
            return self.derivatives_linear_circuit_1(v, h)
        elif self.energy == 'linear_circuit_2':
            return self.derivatives_linear_circuit_2(v, h)
        elif self.energy == 'linear_circuit_3':
            return self.derivatives_linear_circuit_3(v, h)
        elif self.energy == 'linear_circuit_4':
            return self.derivatives_linear_circuit_4(v, h)
        elif self.energy == 'linear_circuit_5':
            return self.derivatives_linear_circuit_4(v, h)

    # CHANGE THIS FUNCTION TO USE THE CORRECT FREE ENERGY
    def free_energy(self, v):
        if self.energy == 'hopfield':
            return self._free_energy_hopfield(v)
        elif self.energy == 'linear_circuit_1':
            return self._free_energy_hopfield(v)
        elif self.energy == 'linear_circuit_2':
            return self._free_energy_hopfield(v)
        elif self.energy == 'linear_circuit_3':
            return self._free_energy_hopfield(v)
        elif self.energy == 'linear_circuit_4':
            return self._free_energy_hopfield(v)
        elif self.energy == 'linear_circuit_5':
            return self._free_energy_hopfield(v)

    def derivatives_hopfield(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        dEdW = -np.einsum('ij,ik->ijk', h, v)
        dEdv_bias = -v
        dEdh_bias = -h
        return dEdW, dEdv_bias, dEdh_bias

    # def derivatives_linear_circuit_1(self,v,h):
    #     # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
    #     v_square = (v**2)[:, np.newaxis, :]
    #     h_square = (h**2)[:, :, np.newaxis]
    #     dEdW = -np.einsum('ij,ik->ijk', h, v) + 0.5*v_square + 0.5*h_square
    #     dEdv_bias = v + 0.5*v**2
    #     dEdh_bias = h + 0.5*h**2
    #     return dEdW, dEdv_bias, dEdh_bias

    # def derivatives_linear_circuit_2(self,v,h):
    #     # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
    #     v_square = (v**2)[:, np.newaxis, :]
    #     vneg_square = ((1-v)**2)[:, np.newaxis, :]
    #     h_square = (h**2)[:, :, np.newaxis]
    #     dEdk_pos = (-np.einsum('ij,ik->ijk', h, v) + 0.5*v_square + 0.5*h_square)
    #     dEdk_neg = (-np.einsum('ij,ik->ijk', h, 1-v) + 0.5*vneg_square + 0.5*h_square)
    #     dkdw_pos = self.dk_pos()[np.newaxis, :, :]
    #     dkdw_neg = self.dk_neg()[np.newaxis, :, :]
    #     dEdW = dEdk_pos*dkdw_pos + dEdk_neg*dkdw_neg

    #     dEdv_bias_pos = v + 0.5*v**2
    #     dEdv_bias_neg = (1-v) + 0.5*(1-v)**2
    #     dv_biasdv_pos = self.dv_bias_pos()[np.newaxis, :]
    #     dv_biasdv_neg = self.dv_bias_neg()[np.newaxis, :]
    #     dEdv_bias = dEdv_bias_pos*dv_biasdv_pos + dEdv_bias_neg*dv_biasdv_neg

    #     dEdh_bias_const = h + 0.5*h**2
    #     dh_biasdh_const = self.dh_bias_constrained()[np.newaxis, :]
    #     dEdh_bias = dEdh_bias_const*dh_biasdh_const

    #     return dEdW, dEdv_bias, dEdh_bias

    # def derivatives_linear_circuit_3(self,v,h):
    #     # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
    #     v_square = (v**2)[:, np.newaxis, :]
    #     vneg_square = ((1-v)**2)[:, np.newaxis, :]
    #     h_square = (h**2)[:, :, np.newaxis]
    #     hneg_square = ((1-h)**2)[:, :, np.newaxis]
    #     dEdk_pos = (-np.einsum('ij,ik->ijk', h, v) + 0.5*v_square + 0.5*h_square) + (-np.einsum('ij,ik->ijk', 1-h, 1-v) + 0.5*vneg_square + 0.5*hneg_square)
    #     dEdk_neg = (-np.einsum('ij,ik->ijk', h, 1-v) + 0.5*vneg_square + 0.5*h_square) + (-np.einsum('ij,ik->ijk', 1-h, v) + 0.5*v_square + 0.5*hneg_square)
    #     dkdw_pos = self.dk_pos()[np.newaxis, :, :]
    #     dkdw_neg = self.dk_neg()[np.newaxis, :, :]
    #     dEdW = dEdk_pos*dkdw_pos + dEdk_neg*dkdw_neg

    #     dEdv_bias_pos = v + 0.5*v**2
    #     dEdv_bias_neg = (1-v) + 0.5*(1-v)**2
    #     dv_biasdv_pos = self.dv_bias_pos()[np.newaxis, :]
    #     dv_biasdv_neg = self.dv_bias_neg()[np.newaxis, :]
    #     dEdv_bias = dEdv_bias_pos*dv_biasdv_pos + dEdv_bias_neg*dv_biasdv_neg

    #     dEdh_bias_pos = h + 0.5*h**2
    #     dEdh_bias_neg = (1-h) + 0.5*(1-h)**2
    #     dh_biasdh_pos = self.dh_bias_pos()[np.newaxis, :]
    #     dh_biasdh_neg = self.dh_bias_neg()[np.newaxis, :]
    #     dEdh_bias = dEdh_bias_pos*dh_biasdh_pos + dEdh_bias_neg*dh_biasdh_neg
    #     return dEdW, dEdv_bias, dEdh_bias

    def derivatives_linear_circuit_4(self, v, h):
        # h has shape (N, n_h) and v has shape (N, n_v), we want result to have shape (N, n_h, n_v)
        v_square = (v**2)[:, np.newaxis, :]
        vneg_square = ((1 - v)**2)[:, np.newaxis, :]
        h_square = (h**2)[:, :, np.newaxis]
        hneg_square = ((1 - h)**2)[:, :, np.newaxis]
        dEdk_pos = (-np.einsum('ij,ik->ijk', h, v) + 0.5 * v_square +
                    0.5 * h_square) + (-np.einsum('ij,ik->ijk', 1 - h, 1 - v) +
                                       0.5 * vneg_square + 0.5 * hneg_square)
        dEdk_neg = (-np.einsum('ij,ik->ijk', h, 1 - v) + 0.5 * vneg_square +
                    0.5 * h_square) + (-np.einsum('ij,ik->ijk', 1 - h, v) +
                                       0.5 * v_square + 0.5 * hneg_square)
        dkdw_pos = self.dk_pos()[np.newaxis, :, :]
        dkdw_neg = self.dk_neg()[np.newaxis, :, :]
        dEdW = dEdk_pos * dkdw_pos + dEdk_neg * dkdw_neg

        dEdv_bias_pos = -self.ground_v * v + 0.5 * v**2
        dEdv_bias_neg = -self.ground_v * (1 - v) + 0.5 * (1 - v)**2
        dv_biasdv_pos = self.dv_bias_pos()[np.newaxis, :]
        dv_biasdv_neg = self.dv_bias_neg()[np.newaxis, :]
        dEdv_bias = dEdv_bias_pos * dv_biasdv_pos + dEdv_bias_neg * dv_biasdv_neg

        dEdh_bias_pos = -self.ground_h * h + 0.5 * h**2
        dEdh_bias_neg = -self.ground_h * (1 - h) + 0.5 * (1 - h)**2
        dh_biasdh_pos = self.dh_bias_pos()[np.newaxis, :]
        dh_biasdh_neg = self.dh_bias_neg()[np.newaxis, :]
        dEdh_bias = dEdh_bias_pos * dh_biasdh_pos + dEdh_bias_neg * dh_biasdh_neg
        return dEdW, dEdv_bias, dEdh_bias

    def k_pos(self):
        return np.piecewise(self.W, [self.W > 0, self.W <= 0],
                            [lambda weight: weight, 0])

    def k_neg(self):
        return np.piecewise(self.W, [self.W < 0, self.W >= 0],
                            [lambda weight: -weight, 0])

    def dk_pos(self):
        return np.piecewise(self.W, [self.W > 0, self.W <= 0],
                            [lambda weight: 1, 0])

    def dk_neg(self):
        return np.piecewise(self.W, [self.W < 0, self.W >= 0],
                            [lambda weight: -1, 0])

    def v_bias_pos(self):
        return np.piecewise(self.v_bias, [self.v_bias > 0, self.v_bias <= 0],
                            [lambda weight: weight, 0])

    def v_bias_neg(self):
        return np.piecewise(
            self.v_bias,
            [self.v_bias < 0, self.v_bias >= 0],
            [lambda weight: -weight, 0],
        )

    def dv_bias_pos(self):
        return np.piecewise(self.v_bias, [self.v_bias > 0, self.v_bias <= 0],
                            [lambda weight: 1, 0])

    def dv_bias_neg(self):
        return np.piecewise(self.v_bias, [self.v_bias < 0, self.v_bias >= 0],
                            [lambda weight: -1, 0])

    def h_bias_constrained(self):
        return np.abs(self.h_bias)

    def dh_bias_constrained(self):
        return np.piecewise(self.h_bias, [self.h_bias > 0, self.h_bias <= 0],
                            [lambda weight: 1, -1])

    def h_bias_pos(self):
        return np.piecewise(self.h_bias, [self.h_bias > 0, self.h_bias <= 0],
                            [lambda weight: weight, 0])

    def h_bias_neg(self):
        return np.piecewise(
            self.h_bias,
            [self.h_bias < 0, self.h_bias >= 0],
            [lambda weight: -weight, 0],
        )

    def dh_bias_pos(self):
        return np.piecewise(self.h_bias, [self.h_bias > 0, self.h_bias <= 0],
                            [lambda weight: 1, 0])

    def dh_bias_neg(self):
        return np.piecewise(self.h_bias, [self.h_bias < 0, self.h_bias >= 0],
                            [lambda weight: -1, 0])

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


def load_rbm(name):
    # Check if you have model load points
    filename_list = glob.glob('model_states/{}_t*.pkl'.format(name))
    if len(filename_list) > 0:
        all_loadpoints = sorted(
            [int(x.split('_t')[-1].split('.pkl')[0]) for x in filename_list])
        last_epoch = all_loadpoints[-1]
        print(
            '** Model trained up to epoch {}, so I load it'.format(last_epoch))
        with open('model_states/{}_t{}.pkl'.format(name, last_epoch),
                  'rb') as file:
            rbm = pickle.load(file)
        # And remove all the previous loadpoints
        for x in all_loadpoints[:-1]:
            os.remove('model_states/{}_t{}.pkl'.format(name, x))
        return True, rbm
    else:
        print('** No load points for {}'.format(name))
        return False, []


def show_and_save(file_name,
                  img,
                  cmap='gray',
                  vmin=None,
                  vmax=None,
                  save=False):
    # npimg = np.transpose(img.numpy(),(1,2,0))
    f = './%s.png' % file_name
    plt.title(file_name)
    plt.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax)
    if save:
        plt.imsave(f, img, cmap=cmap, vmin=vmin, vmax=vmax)


def make_grid(array, nrow=8, padding=2):
    N = array.shape[0]
    H = array.shape[1]
    W = array.shape[2]
    grid_h = int(np.ceil(N / float(nrow)))
    grid_w = nrow
    grid = np.zeros(
        [grid_h * (H + padding) + padding, grid_w * (W + padding) + padding])
    k = 0
    for y in range(grid_h):
        for x in range(grid_w):
            if k < N:
                grid[
                    y * (H + padding):y * (H + padding) + H,
                    x * (W + padding):x * (W + padding) + W,
                ] = array[k]
                k = k + 1
    return grid
