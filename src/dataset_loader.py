# src/dataset_loader.py
import os
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

class SolarDataset(Dataset):
    def __init__(self, csv_path, processed_root="data/processed", image_size=512, augment=False):
        self.df = pd.read_csv(csv_path)
        self.processed_root = processed_root
        self.image_size = image_size

        # Basic transforms (resize + normalization)
        base = [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            # Normalize to ImageNet stats (works well for transfer learning)
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ]

        if augment:
            self.transform = transforms.Compose([
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(degrees=10),
                transforms.ColorJitter(brightness=0.2, contrast=0.2),
                transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
                *base
            ])
        else:
            self.transform = transforms.Compose(base)

    def __len__(self):
        return len(self.df)

    def _resolve_path(self, filename, dataset_name):
        # Images under: data/processed/<dataset_name>/images/<filename>
        return os.path.join(self.processed_root, dataset_name, "images", filename)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        filename = row["filename"]
        label = int(row["solar_present"])
        dataset_name = row["dataset_name"]

        img_path = self._resolve_path(filename, dataset_name)
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)

        return image, label, filename, dataset_name