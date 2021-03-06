import torch
import torch.nn as nn

def conv3x3(in_planes, out_planes, stride=1, padding=1):
    return nn.Conv2d(in_channels=in_planes, out_channels=out_planes, kernel_size=3, stride=stride, padding=padding)

def conv1x1(in_planes, out_planes, stride=1):
    return nn.Conv2d(in_channels=in_planes, out_channels=out_planes, kernel_size=1, stride=stride)

class BasicBlock(nn.Module):
    expansion = 1 

    def __init__(self, in_planes, out_planes, stride=1, downsample=None):
        super(BasicBlock, self).__init__()

        self.conv1 = conv3x3(in_planes, out_planes)       
        self.bn1 = nn.BatchNorm2d(out_planes)    

        self.conv2 = conv3x3(out_planes, out_planes)
        self.nb2 = nn.BatchNorm2d(out_planes)
        
        self.downsample = downsample
        self.relu = nn.ReLU()

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample != None:         # dimension을 맞춰줘야할 때 수행합니다.
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out

class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1, downsample=None):
        super(Bottleneck, self).__init__()

        self.conv1 = conv1x1(in_planes, planes)
        self.bn1 = nn.BatchNorm2d(planes)

        self.conv2 = conv3x3(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)
        
        self.conv3 = conv1x1(planes, planes*self.expansion)
        self.bn3 = nn.BatchNorm2d(planes*self.expansion)

        self.downsample = downsample
        self.relu = nn.ReLU()

    def forward(self, x):
        identity = x

        out = conv1(x)
        out = bn1(out)
        out = relu(out)

        out = conv2(out)
        out = bn2(out)
        out = relu(out)

        out = conv3(out)
        out = bn3(out)

        if self.downsample != None:         # dimension을 맞춰줘야할 때 수행합니다.
            identity = self.downsample(x)

        out += identity
        out = relu(out)

        return out

"""Bottleneck 테스트"""
myneck = Bottleneck(64, 64)
myneck

class ResNet(nn.Module):
    """ [ResNet 생성자]
    block           블록의 종류 (Basicblock or Bottleneck)
    layers          각 단계별 레이어 개수 (리스트 타입)
    num_classes     y 분류 개수
    """
    def __init__(self, block, layers, num_classes=1000):
        super(ResNet, self).__init__()

        self.inplanes = 64  # 첫 필터는 64개로 시작합니다.

        """ [conv1]
        in_channels = input 이미지의 채널은 3
        out_channels = 첫 필터는 64개(inplanes), 피쳐맵 크기?
        필터 사이즈=7x7, 스트라이드=2, 패딩=3
        """
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=self.inplanes, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(self.inplanes)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)

        """ [conv2_ ~ conv5_]
        _make_layers 함수로 각 층을 블록으로 쌓아 생성합니다.
        """
        self.conv2_ = self._make_layers(block, 64, layers[0], stride=1)
        self.conv3_ = self._make_layers(block, 128, layers[1], stride=2)
        self.conv4_ = self._make_layers(block, 256, layers[2], stride=2)
        self.conv5_ = self._make_layers(block, 512, layers[3], stride=2)

        self.fc = nn.Linear(512 * block.expansion, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d((1,1))

    """ [_make_layers()]
    블록들을 쌓아 각 층을 생성합니다.
    """
    def _make_layers(self, block, planes, num_of_blocks, stride):

        # 다운샘플 여부를 체크:
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                conv1x1(self.inplanes, planes * block.expansion, stride),
                nn.BatchNorm2d(planes * block.expansion)
            )

        # 층에 쌓여지는 레이어 객체 리스트 선언:
        layers = [] 

        # 첫 번째 레이어 append:
        layers.append(block(self.inplanes, planes, stride))

        # inplanes 값 갱신:
        self.inplanes = planes * block.expansion    

        # 나머지 레이어 append:
        for _ in range(1, num_of_blocks):
            layers.append(block(self.inplanes, planes))

        # 순서대로 쌓여진 모듈 반환:
        return nn.Sequential(*layers)

    def forward(self, x):

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.maxpool(out)

        out = self.conv2_(out)
        out = self.conv3_(out)
        out = self.conv4_(out)
        out = self.conv5_(out)

        out = self.avgpool(out)
        out = torch.flatten(out, 1)
        out = self.fc(out)

        return out

"""resnet 생성 테스트"""
mynet50 = ResNet(Bottleneck, [3, 4, 6, 3])
mynet50

def ResNet18():
    return ResNet(BasicBlock, [2, 2, 2, 2])

def ResNet34():
    return ResNet(BasicBlock, [3, 4, 6, 3])

def ResNet50():
    return ResNet(Bottleneck, [3, 4, 6, 3])

def ResNet101():
    return ResNet(Bottleneck, [3, 4, 23, 3])

def ResNet152():
    return ResNet(Bottleneck, [3, 8, 36, 3])

"""생성기 테스트"""
mynet101 = ResNet101()
mynet101
