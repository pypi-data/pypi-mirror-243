import dataclasses
import typing
import PIL.Image
import torch
import torch.utils.data
import torchvision.datasets
import irisml.core


class Task(irisml.core.TaskBase):
    """Load a dataset from torchvision package.

    Data will be downloaded to the current directory. Downloading will be skipped if the data is in the current directory.

    Only Image classification data is supported for now.

    Config:
        name (str): Name of the dataset. See https://pytorch.org/vision/main/datasets.html for the list of supported datasets.
    """
    VERSION = '0.1.1'

    @dataclasses.dataclass
    class Config:
        name: str

    @dataclasses.dataclass
    class Outputs:
        train_dataset: torch.utils.data.Dataset
        val_dataset: torch.utils.data.Dataset
        num_classes: int
        class_names: typing.Optional[typing.List[str]]

    def execute(self, inputs):
        if not hasattr(torchvision.datasets, self.config.name):
            raise RuntimeError(f"Dataset {self.config.name} is not supported.")

        dataset_class = getattr(torchvision.datasets, self.config.name)

        train_dataset = dataset_class('.', train=True, download=True)
        val_dataset = dataset_class('.', train=False, download=True)
        class_names = None
        if hasattr(train_dataset, 'classes'):
            num_classes = len(train_dataset.classes)
            class_names = train_dataset.classes
        else:
            label_set = set()
            for i in range(len(train_dataset)):
                _, label = train_dataset[i]
                label_set.add(label)
            num_classes = len(label_set)

        return self.Outputs(train_dataset=train_dataset, val_dataset=val_dataset, num_classes=num_classes, class_names=class_names)

    def dry_run(self, inputs):
        return self.Outputs(train_dataset=FakeDataset(100, 5), val_dataset=FakeDataset(100, 5), num_classes=5, class_names=['a', 'b', 'c', 'd', 'e'])


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, num_images, num_classes):
        self._num_images = num_images
        self._num_classes = num_classes

    def __len__(self):
        return self._num_images

    def __getitem__(self, index):
        if index >= self._num_images:
            raise IndexError()

        class_id = index % self._num_classes
        return PIL.Image.new('RGB', (32, 32), color=(class_id, class_id, class_id)), torch.tensor(class_id)
