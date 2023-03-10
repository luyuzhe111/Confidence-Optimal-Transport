import torch
import torch.nn as nn
import os
import pickle
from tqdm import tqdm
import contextlib


def evaluation(net, testloader):
    net.eval()
    criterion = nn.CrossEntropyLoss()
    test_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for _, (inputs, targets) in enumerate(tqdm(testloader)):
            inputs, targets = inputs.cuda(), targets.cuda()
            outputs = net(inputs)
            loss = criterion(outputs, targets)
            test_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
    return test_loss / total, 100. * correct / total


def baseline_evaluation(net, testloader, val_loader, t, t_vec, net2):
    net.eval()
    net2.eval()
    criterion = nn.CrossEntropyLoss()
    metrics = torch.tensor([0.0] * 4)
    test_loss = 0
    correct = 0
    total = 0

    print('compute baselines...')
    with torch.no_grad():
        for _, (inputs, targets) in enumerate(tqdm(testloader)):
            inputs, targets = inputs.cuda(), targets.cuda()
            outputs = net(inputs)
            outputs2 = net2(inputs)

            # ConfScore
            softmax = nn.Softmax(dim=1)
            loss = torch.max(softmax(outputs), dim=1)[0]
            metrics[0] += loss.sum().item()

            # Entropy
            loss = torch.sum(-softmax(outputs) * torch.log2(softmax(outputs)), dim=1)
            metrics[1] += loss.sum().item()

            # ATC
            s_softmax = torch.sum(softmax(outputs) * torch.log2(softmax(outputs)), dim=1)
            loss = s_softmax < t
            metrics[2] += loss.sum().item()

            # Test loss
            loss = criterion(outputs, targets)
            test_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            _, predicted2 = outputs2.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)

            # AgreeScore
            metrics[3] += predicted.eq(predicted2).sum().item()

    return metrics / total, test_loss / total, 100 * correct / total


def compute_t(net, iid_loader):
    net.eval()
    misclassified = 0
    res = []
    with torch.no_grad():
        for _, (inputs, targets) in enumerate(tqdm(iid_loader)):
            inputs, targets = inputs.cuda(), targets.cuda()
            outputs = net(inputs)
            _, predicted = outputs.max(1)
            misclassified += targets.size(0) - predicted.eq(targets).sum().item()
            softmax = nn.Softmax(dim=1)
            res.append(torch.sum(softmax(outputs) * torch.log2(softmax(outputs)), dim=1))
    s_softmax = torch.cat(res)

    sorted_s_softmax = torch.sort(s_softmax)[0]
    return sorted_s_softmax[misclassified - 1] + 1e-9


def compute_t_vec(net, iid_loader):
    net.eval()
    misclassified = 0
    res = []
    with torch.no_grad():
        for _, (inputs, targets) in enumerate(tqdm(iid_loader)):
            inputs, targets = inputs.cuda(), targets.cuda()
            outputs = net(inputs)
            _, predicted = outputs.max(1)
            misclassified += targets.size(0) - predicted.eq(targets).sum().item()
            res.append(outputs)

    logits = torch.cat(res)

    sorted_logits = torch.sort(logits, dim=0)[0]
    return sorted_logits[misclassified - 1, :] + 1e-9


def gather_outputs(model, dataloader, device, cache_dir):
    if os.path.exists(cache_dir):
        print('loading cached result from', cache_dir)
        data = pickle.load( open(cache_dir, "rb" ))
        acts, preds, tars = data['act'], data['pred'], data['tar']
        return acts.to(device), preds.to(device), tars.to(device)
    else:
        preds = []
        acts = []
        tars = []
        print('computing result for', cache_dir)
        with torch.no_grad():
            for inputs, targets in tqdm(dataloader):
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)

                _, predicted = outputs.max(1)

                act = outputs

                preds.append(predicted)
                acts.append(act)
                tars.extend(targets)
        
        act, pred, tar = torch.concat(acts), torch.concat(preds), torch.as_tensor(tars, device=device)

        data = {'act': act.cpu(), 'pred': pred.cpu(), 'tar': tar.cpu()}
        pickle.dump( data, open( cache_dir, "wb" ) )

    return act, pred, tar