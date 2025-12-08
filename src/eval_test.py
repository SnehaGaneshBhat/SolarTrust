# src/eval_test.py
import torch, numpy as np
from torch.utils.data import DataLoader
from torch import nn
from dataset_loader import SolarDataset
from utils import accuracy, f1_binary
from torchvision import models

def build_model(num_classes=2):
    model = models.resnet18(weights=None)  # we'll load trained weights
    in_feats = model.fc.in_features
    model.fc = nn.Linear(in_feats, num_classes)
    return model

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    test_ds = SolarDataset(csv_path="data/test_split.csv", augment=False)
    test_loader = DataLoader(test_ds, batch_size=32, shuffle=False, num_workers=0)

    model = build_model(num_classes=2).to(device)
    state_dict = torch.load("trained_model/best_model.pt", map_location=device)
    model.load_state_dict(state_dict)
    model.eval()

    all_preds, all_labels = [], []
    with torch.no_grad():
        for images, labels, _, _ in test_loader:
            images = images.to(device)
            outputs = model(images)
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.append(preds)
            all_labels.append(labels.numpy())

    all_preds = np.concatenate(all_preds)
    all_labels = np.concatenate(all_labels)

    print(f"Test accuracy: {accuracy(all_preds, all_labels):.4f}")
    print(f"Test F1: {f1_binary(all_preds, all_labels):.4f}")

if __name__ == "__main__":
    main()