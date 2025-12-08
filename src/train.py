# src/train.py
import os
import time
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import models

from dataset_loader import SolarDataset
from utils import set_seed, accuracy, f1_binary

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def build_model(num_classes=2):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    # Replace the final layer
    in_feats = model.fc.in_features
    model.fc = nn.Linear(in_feats, num_classes)
    return model

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    for images, labels, _, _ in loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
    return running_loss / len(loader.dataset)

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    all_preds = []
    all_labels = []

    for images, labels, _, _ in loader:
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        preds = outputs.argmax(dim=1)
        all_preds.append(preds.cpu().numpy())
        all_labels.append(labels.cpu().numpy())

    all_preds = np.concatenate(all_preds)
    all_labels = np.concatenate(all_labels)

    acc = accuracy(all_preds, all_labels)
    f1 = f1_binary(all_preds, all_labels)

    return (running_loss / len(loader.dataset)), acc, f1

def main():
    set_seed(42)
    device = get_device()
    os.makedirs("trained_model", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Datasets and loaders
    train_ds = SolarDataset(csv_path="data/train_split.csv", augment=True)
    val_ds = SolarDataset(csv_path="data/val_split.csv", augment=False)

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=0)

    # Model, loss, optimizer
    model = build_model(num_classes=2).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    best_f1 = -1.0
    log_path = os.path.join("logs", f"train_{int(time.time())}.txt")
    with open(log_path, "w") as logf:
        for epoch in range(1, 11):  # 10 epochs baseline
            train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
            val_loss, val_acc, val_f1 = evaluate(model, val_loader, criterion, device)

            line = f"Epoch {epoch:02d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_acc={val_acc:.4f} | val_f1={val_f1:.4f}"
            print(line)
            logf.write(line + "\n")

            if val_f1 > best_f1:
                best_f1 = val_f1
                torch.save(model.state_dict(), os.path.join("trained_model", "best_model.pt"))

    print(f"Best val F1: {best_f1:.4f}")
    print("Training complete. Model saved to trained_model/best_model.pt")

if __name__ == "__main__":
    main()