import unittest
import torch.utils.data
from irisml.tasks.load_torchvision_dataset import Task


class TestLoadTorchvisionDataset(unittest.TestCase):
    def test_notfound(self):
        with self.assertRaises(RuntimeError):
            Task(Task.Config(name='unknown_dataset')).execute(Task.Inputs())

    def test_dry_run(self):
        outputs = Task(Task.Config(name='fake_dataset')).dry_run(Task.Inputs())
        self.assertIsInstance(outputs.train_dataset, torch.utils.data.Dataset)
        self.assertIsInstance(outputs.val_dataset, torch.utils.data.Dataset)
        self.assertGreater(outputs.num_classes, 0)
        self.assertIsNotNone(outputs.class_names)
        self.assertEqual(len(outputs.class_names), outputs.num_classes)
