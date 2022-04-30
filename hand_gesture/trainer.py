import numpy as np
from tqdm import tqdm

import torch

from utils import plot


def accuracy(y_pred, y_true):
    _, top_class = y_pred.topk(1, dim=1)
    _, y_true = y_true.topk(1, dim=1)
    equals = top_class == y_true.view(*top_class.shape)
    return torch.sum(equals.type(torch.FloatTensor))


class Trainer:

    def __init__(self, criterion, optimizer, scheduler=None):
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f'Device: {self.device}\n')

    def train_batch_loop(self, model, dataloader):
        train_loss = 0.0
        train_acc  = 0.0

        for inputs, labels in tqdm(dataloader):
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            self.optimizer.zero_grad()
            logits = model(inputs)
            loss = self.criterion(logits, labels)
            loss.backward()
            self.optimizer.step()

            train_loss += loss.item()
            train_acc  += accuracy(logits, labels)
        
        return train_loss / len(dataloader), train_acc / len(dataloader.dataset)

    def valid_batch_loop(self, model, dataloader):
        val_loss = 0.0
        val_acc  = 0.0

        with torch.no_grad():
            for inputs, labels in tqdm(dataloader):
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                logits = model(inputs)
                loss = self.criterion(logits, labels)

                val_loss += loss.item()
                val_acc  += accuracy(logits, labels)
        
        return val_loss / len(dataloader), val_acc / len(dataloader.dataset)

    def train(self, model, train_dataloader, val_dataloader, epochs, model_path, save_weights_path='./hand_gesture/weights/model.pt'):
        model.to(self.device)

        best_epoch = 0
        val_min_loss = np.Inf
        val_max_acc  = 0.0

        train_loss_list, val_loss_list = [], []
        train_acc_list, val_acc_list   = [], []

        try:
            for epoch in range(epochs):
                model.train()
                train_loss, train_acc = self.train_batch_loop(model=model, dataloader=train_dataloader)

                model.eval()
                val_loss, val_acc = self.valid_batch_loop(model=model, dataloader=val_dataloader)

                if self.scheduler is not None:
                    self.scheduler.step(val_loss)

                if val_loss <= val_min_loss:
                    print('val_loss improved, saving model weight to {}'.format(save_weights_path))
                    torch.save(model.state_dict(), save_weights_path)
                    best_epoch = epoch+1
                    val_min_loss = val_loss
                    val_max_acc  = val_acc
                
                print('Epoch: {}'.format(epoch+1))
                print('   train_loss: {:.6f} train_acc: {:.6f}'.format(train_loss, train_acc))
                print('   val_loss  : {:.6f} val_acc  : {:.6f}'.format(val_loss, val_acc))
                train_loss_list.append(train_loss)
                val_loss_list.append(val_loss)
                train_acc_list.append(train_acc)
                val_acc_list.append(val_acc)

        except KeyboardInterrupt:
            pass
        
        print('\nThe best model is from epoch: {}'.format(best_epoch))
        print('   val_min_loss: {:.6f} val_max_acc: {:.6f}'.format(val_min_loss, val_max_acc))
        plot(train_data=train_loss_list, val_data=val_loss_list,
             name='loss', save_dir=model_path)
        plot(train_data=train_acc_list, val_data=val_acc_list,
             name='accuracy', save_dir=model_path)
