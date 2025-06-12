import torch
import torch.nn.functional as F
import torch.nn as nn
import string

CHARSET = string.digits + string.ascii_lowercase
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
idx2char = {i: c for i, c in enumerate(CHARSET)}

modelpath = 'ResNet95.pth'
import torchvision.models as models

from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


class Captcha(nn.Module):

    def __init__(self, num_classes=len(CHARSET), pretrained=True):
        super().__init__()
        backbone = models.resnet18(pretrained=pretrained)
        self.features = nn.Sequential(*list(backbone.children())[:-1])
        self.fc_shared = nn.Linear(512, 512)
        self.head0 = nn.Linear(512, num_classes)
        self.head1 = nn.Linear(512, num_classes)
        self.head2 = nn.Linear(512, num_classes)
        self.head3 = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = nn.functional.relu(self.fc_shared(x))
        out0 = self.head0(x)
        out1 = self.head1(x)
        out2 = self.head2(x)
        out3 = self.head3(x)
        return out0, out1, out2, out3


def load():
    model = Captcha().to(device)
    orig_state = torch.load(modelpath, map_location=device)
    new_state = {}

    for k, v in orig_state.items():
        if k.startswith('head'):
            num, rest = k[4], k[5:]
            new_key = f'head{num}{rest}'
            new_state[new_key] = v
        else:
            new_state[k] = v
    model.load_state_dict(new_state)
    model.eval()
    return model
