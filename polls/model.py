from torch import nn
from torchvision import transforms, datasets, models


class mymodel(nn.Module):
    def __init__(self, class_num):
        super(mymodel, self).__init__()
        self.model = models.resnet50(pretrained=True)
        self.fc = nn.Linear(2048, class_num)

    def forward(self, x):
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)

        x = self.model.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x
