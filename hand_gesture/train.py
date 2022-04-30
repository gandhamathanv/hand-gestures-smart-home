import torch
from torch import nn

import os
from datetime import datetime

from dataset import get_dataloader
from model import HandGestureModel
from trainer import Trainer
from config import model_dir, data_path, batch_size, lr, epochs, gamma


today = datetime.now().strftime('%Y-%m-%d')
num_version = len([ver for ver in os.listdir(model_dir) 
                   if ver.startswith(today)])
version = f'{today}-{num_version}'
model_path = os.path.join(model_dir, version)
os.mkdir(model_path)
save_weights_path = os.path.join(model_path, 'model.pt')

train_dataloader, val_dataloader = get_dataloader(data_path=data_path, batch_size=batch_size)

model = HandGestureModel()

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=lr)
scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer=optimizer, gamma=gamma)

trainer = Trainer(criterion=criterion, optimizer=optimizer, scheduler=scheduler)
trainer.train(model=model, train_dataloader=train_dataloader, val_dataloader=val_dataloader,
              epochs=epochs, model_path=model_path, save_weights_path=save_weights_path)
