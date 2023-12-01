import unittest
import torch
from rkm.rbm_pytorch import RBM


class TestRBM(unittest.TestCase):

    def setUp(self):
        self.rbm = RBM('test_model', n_vis=10, n_hin=5)

    def test_init(self):
        self.assertEqual(self.rbm.name, 'test_model')
        self.assertEqual(self.rbm.n_visible, 10)
        self.assertEqual(self.rbm.n_hidden, 5)
        self.assertIsInstance(self.rbm.W, torch.Tensor)
        self.assertIsInstance(self.rbm.v_bias, torch.Tensor)
        self.assertIsInstance(self.rbm.h_bias, torch.Tensor)

    def test_weights(self):
        self.assertEqual(self.rbm.W.shape, (5, 10))
        self.assertEqual(self.rbm.v_bias.shape, (10, ))
        self.assertEqual(self.rbm.h_bias.shape, (5, ))

    def test_device(self):
        self.assertEqual(
            self.rbm.device,
            torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
        )

    def test_model_beta(self):
        self.assertEqual(self.rbm.model_beta, 1)

    def test_regularization(self):
        self.assertFalse(self.rbm.regularization)
        self.assertFalse(hasattr(self.rbm, 'l1'))
        self.assertFalse(hasattr(self.rbm, 'l2'))

    def test_optimizer(self):
        self.assertEqual(self.rbm.optimizer, 'Adam')
        self.assertEqual(self.rbm.beta1, 0.9)
        self.assertEqual(self.rbm.beta2, 0.999)
        self.assertEqual(self.rbm.epsilon, 1e-8)

    def test_weights_initialization(self):
        self.assertTrue(
            torch.all(torch.logical_and(self.rbm.W >= -100, self.rbm.W
                                        <= 100)))
        self.assertTrue(
            torch.all(
                torch.logical_and(self.rbm.h_bias >= -100, self.rbm.h_bias
                                  <= 100)))


if __name__ == '__main__':
    unittest.main()
