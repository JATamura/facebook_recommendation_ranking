import torch
import os
import pandas as pd
from ordered_set import OrderedSet
from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision.io import read_image

class image_dataset(Dataset):
    
    def __init__(self, images_file, products_file, img_dir, transform=None, target_transform=None):
        self.create_encoder(products_file)
        self.img_labels = self.label_images(images_file, products_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label

    def create_encoder(self, products_file):
        products = pd.read_csv(products_file, lineterminator="\n")
        self.encoder = {}
        i = 0
        for category in OrderedSet(products["category"]):
            self.encoder[category] = i
            i+=1

    def label_images(self, images_file, products_file):
        images = pd.read_csv(images_file)
        products = pd.read_csv(products_file, lineterminator="\n")
        annotations = {"image": [], "label": []}
        for image in images.values[:1000]:
            annotations["image"].append(image[1])
            annotations["label"].append(self.encoder[products[products["id"]==image[2]]["category"].values[0]])
        annotations_df = pd.DataFrame(annotations)
        print(annotations_df)
    

if __name__ == '__main__':
    data = image_dataset("images.csv", "products.csv", "cleaned_images/")
