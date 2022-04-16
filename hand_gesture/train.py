import torch
from torch import nn

from dataset import get_dataloader
from model import HandGestureModel
from trainer import Trainer
from config import data_path, batch_size, lr, epochs, gamma


train_dataloader, val_dataloader = get_dataloader(data_path=data_path, batch_size=batch_size)

model = HandGestureModel()

criterion = nn.BCELoss() # CrossEntropyLoss, BCELoss
optimizer = torch.optim.Adam(params=model.parameters(), lr=lr)
scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer=optimizer, gamma=gamma)

trainer = Trainer(criterion=criterion, optimizer=optimizer, scheduler=scheduler)
trainer.train(model=model, train_dataloader=train_dataloader, val_dataloader=val_dataloader,
              epochs=epochs, save_weights_path='./hand_gesture/weights/model_norm.pt')
