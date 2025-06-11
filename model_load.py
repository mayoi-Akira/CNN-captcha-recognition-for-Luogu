import torch
from torchvision import transforms
import torch.nn.functional as F
import torch.nn as nn
import string

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])
CHARSET = string.digits + string.ascii_lowercase
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
idx2char = {i: c for i, c in enumerate(CHARSET)}
modelpath = '8302.pth'


class CaptchaCNN(nn.Module):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.pool3 = nn.MaxPool2d(2)
        self.fc = nn.Linear(128 * 4 * 11, 512)
        self.heads = nn.ModuleList(
            [nn.Linear(512, len(CHARSET)) for _ in range(4)])

    def forward(self, x):
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.pool3(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc(x))
        return tuple(head(x) for head in self.heads)


def load():
    model = CaptchaCNN().to(device)
    orig_state = torch.load(modelpath, map_location=device)
    new_state = {}

    for k, v in orig_state.items():
        if k.startswith('head'):
            num, rest = k[4], k[5:]
            new_key = f'heads.{num}{rest}'
            new_state[new_key] = v
        else:
            new_state[k] = v
    model.load_state_dict(new_state)
    model.eval()
    return model
