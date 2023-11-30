import unittest
import torch
import PIL.Image
from irisml.tasks.create_torchvision_transform_v2 import Task


class TestCreateTorvhsionTransformV2(unittest.TestCase):
    def test_simple(self):
        config = Task.Config(["Resize((256, 256), 'InterpolationMode.BICUBIC')", "CenterCrop(224)"])
        outputs = Task(config).execute(Task.Inputs())

        image = PIL.Image.new('RGB', (500, 500))
        targets = torch.tensor(3)
        image, targets = outputs.transform(image, targets)

        self.assertIsInstance(image, torch.Tensor)
        self.assertEqual(image.shape, (3, 224, 224))
        self.assertIsInstance(targets, torch.Tensor)
        self.assertEqual(targets, torch.tensor(3))

    def test_object_detection(self):
        config = Task.Config(["Resize((250, 250), 'InterpolationMode.BICUBIC')", "CenterCrop(125)"], task_type='object_detection')
        outputs = Task(config).execute(Task.Inputs())

        image = PIL.Image.new('RGB', (500, 500))
        targets = torch.tensor([[0, 0, 0.5, 0.5, 1.0], [3, 0.25, 0.25, 0.75, 0.75], [5, 0.75, 1.0, 0.75, 1.0]])
        image, targets = outputs.transform(image, targets)

        self.assertIsInstance(image, torch.Tensor)
        self.assertEqual(image.shape, (3, 125, 125))
        self.assertIsInstance(targets, torch.Tensor)
        self.assertLess((targets - torch.tensor([[0, 0, 0.5, 0.5, 1.0], [3, 0, 0, 1.0, 1.0]])).abs().max(), 1e-2)

    def test_phrase_grounding(self):
        config = Task.Config(["Resize((250, 250), 'InterpolationMode.BICUBIC')", "CenterCrop(125)"], task_type='phrase_grounding')
        outputs = Task(config).execute(Task.Inputs())

        image = PIL.Image.new('RGB', (500, 500))
        targets = [((0, 4), torch.tensor([[0, 0.5, 0.5, 1.0]])),
                   ((5, 7), torch.tensor([[0.25, 0.25, 0.75, 0.75], [0.75, 1.0, 0.75, 1.0]])),
                   ((8, 12), torch.tensor([[0.75, 1.0, 0.75, 1.0]]))]
        (caption, image), targets = outputs.transform(('This is a test.', image), targets)

        self.assertIsInstance(image, torch.Tensor)
        self.assertEqual(image.shape, (3, 125, 125))
        self.assertEqual(caption, 'This is a test.')
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), 2)
        self.assertEqual(targets[0][0], (0, 4))
        self.assertLess((targets[0][1] - torch.tensor([[0, 0.5, 0.5, 1.0]])).abs().max(), 1e-2)
        self.assertEqual(targets[1][0], (5, 7))
        self.assertLess((targets[1][1] - torch.tensor([[0, 0, 1.0, 1.0]])).abs().max(), 1e-2)
