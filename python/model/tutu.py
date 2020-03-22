from io import BytesIO

import requests
import torch
from PIL import Image
from torchvision import transforms

from .classes import imagnet_classes


def is_cat(url):
    response = requests.get(url)
    input_image = Image.open(BytesIO(response.content))
    model = torch.hub.load('pytorch/vision', 'mobilenet_v2', pretrained=True)
    model.eval()

    # input_image = Image.open('cat.jpg')
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model

    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(input_batch)
    # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
    # print(output[1])
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    # print(torch.nn.functional.softmax(output[0], dim=0))
    return imagnet_classes[float(torch.argmax(output[0]))].find('cat') != -1
