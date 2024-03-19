import torch
from torchvision import transforms
from PIL import Image
import sys
import os
import torch.nn as nn
# # F:\\bachelor\\7th sem\\project\\eye-disease\\backend\\config\\uploads\\1708501704039-_0_4015166.jpg
# # F:\bachelor\7th sem\project\eye-disease\backend\config\uploads\1708505969175-_0_4015166.jpg
# # from algorithm.model import CNN

# class CNN(nn.Module):
#     def __init__(self, NUMBER_OF_CLASSES):
#         super(CNN, self).__init__()
#         self.conv_layers = nn.Sequential(
#             nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=2),
#             nn.BatchNorm2d(16),
#             nn.LeakyReLU(),
#             nn.MaxPool2d(kernel_size=2, stride=2),
#             nn.Conv2d(in_channels=16, out_channels=32,
#                       kernel_size=3, stride=2),
#             nn.BatchNorm2d(32),
#             nn.LeakyReLU(),
#             nn.MaxPool2d(kernel_size=2, stride=2),
#             nn.Conv2d(in_channels=32, out_channels=64,
#                       kernel_size=3, stride=2),
#             nn.BatchNorm2d(64),
#             nn.LeakyReLU(),
#             nn.MaxPool2d(kernel_size=2, stride=2),
#         )

#         self.dense_layers = nn.Sequential(
#             nn.Dropout(0.2),
#             nn.Linear(64 * 3 * 3, 128),
#             nn.ReLU(),
#             nn.Dropout(0.2),
#             nn.Linear(128, NUMBER_OF_CLASSES),
#         )

#     def forward(self, x):
#         x = self.conv_layers(x)
#         x = x.view(x.size(0), -1)
#         x = self.dense_layers(x)

#         return x
class CNN6(nn.Module):
    def __init__(self, NUMBER_OF_CLASSES):
        super(CNN6, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=2),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=3, stride=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=64, out_channels=128,
                      kernel_size=3, stride=2),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.dense_layers = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(128 * 3 * 3, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, NUMBER_OF_CLASSES),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.dense_layers(x)

        return x

# def predict(path):
#     disease = {0 : "Cataract", 1 : "Normal"}
#     # print(os.getcwd())
#     predictions = None
#     model = CNN(2)
#     relative_path = os.path.join("DP_backend","alogirthm")
#     model_path = os.path.join(os.getcwd(), relative_path, "eyepredict.pt")
#     model.load_state_dict(torch.load(model_path))
#     # # model = torch.load("algorithm/model.pt")
#     model.eval()
#     transform = transforms.Compose([
#         transforms.Resize((256,256)),
#         transforms.ToTensor()
#     ])

#     image_path = path
#     # print(image_path)
#     # image = Image.open(image_path)
#     # image_path = r'F:\bachelor\7th sem\project\eye-disease\dataset\normal\2329_right.jpg'
#     normalized_path = os.path.normpath(image_path)
#     image = Image.open(normalized_path)
#     image = transform(image)
#     image_tensor = image.unsqueeze(0)
#     # print(image_tensor.shape)
#     # print(image_tensor)
#     with torch.no_grad():
#         outputs = model(image_tensor)
#         _, predicted = torch.max(outputs, 1)
#         # print(outputs)
#         predictions = predicted.item()
#     return disease[predictions]

def predict(path):
    disease = {0 : "Cataract", 1 : "Glaucoma", 2 : "Normal"}
    # print(os.getcwd())
    predictions = None
    # model = CNN5(3)
    relative_path = os.path.join("DP_backend","alogirthm")
    model_path = os.path.join(os.getcwd(), relative_path, "cnn6.pt")
    # model.load_state_dict(torch.load(model_path))
    model = torch.load(model_path)
    model.eval()
    transform = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.ToTensor()
    ])

    image_path = path
    # print(image_path)
    # image = Image.open(image_path)
    # image_path = r'F:\bachelor\7th sem\project\eye-disease\dataset\normal\2329_right.jpg'
    normalized_path = os.path.normpath(image_path)
    image = Image.open(normalized_path)
    image = transform(image)
    image_tensor = image.unsqueeze(0)
    # print(image_tensor.shape)
    # print(image_tensor)
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        # print(outputs)
        predictions = predicted.item()
    return disease[predictions]
    
    
