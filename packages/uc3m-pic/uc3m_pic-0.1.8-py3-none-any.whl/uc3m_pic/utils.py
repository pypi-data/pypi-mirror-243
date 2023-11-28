import torch

def conv2d_output_size(input_size, kernel_size, padding=0, stride=1,
                          pool_kernel_size=1, pool_stride=1):
    '''
    Computes the output size of a convolutional layer, supposing square 
    dimensions in input, kernel, padding and stride, and a pooling layer with
    symmetric dimensions in kernel and stride.

    Parameters
    ----------
    input_size : int
        Input size 
    kernel_size : int
        Kernel size
    padding : int, optional
        Padding size. The default is 0.
    stride : int, optional
        Stride size. The default is 1.
    pool_kernel_size : int, optional
        Pooling kernel size. The default is 1.
    pool_stride : int, optional
        Pooling stride size. The default is 1.
    
    Returns
    -------
    pool_output : int
        Output size of the pooling layer
    '''
    
    conv_output = (input_size + 2*padding - kernel_size) // stride + 1
    pool_output = (conv_output - pool_kernel_size) // pool_stride + 1

    return pool_output


def train(model, dataloader, loss_fn, optimizer, lr_scheduler=None):
    
    '''
    Training loop

    Parameters
    ----------
    model : torch.nn.Module
        Model to train
    dataloader : torch.utils.data.DataLoader
        Dataloader with the training data
    loss_fn : torch.nn.Module
        Loss function
    optimizer : torch.optim.Optimizer
        Optimizer

    Returns
    -------
    None
    '''

    device = next(model.parameters()).device
    model.train()
    for x, y in dataloader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        y_pred = model(x)
        loss = loss_fn(torch.log(y_pred), y)
        loss.backward()
        optimizer.step()
    if lr_scheduler:
        lr_scheduler.step()


def test(model, dataloader, loss_fn, metrics_fn):

    '''
    Test loop

    Parameters
    ----------
    model : torch.nn.Module
        Model to test
    dataloader : torch.utils.data.DataLoader
        Dataloader with the testing data
    loss_fn : torch.nn.Module
        Loss function
    metrics_fn : torchmetrics.Metric
        Metric function

    Returns
    -------
    loss_fn : float
        Loss value
    metrics_fn : float
        Metric value
    '''
    
    device = next(model.parameters()).device
    model.eval()
    metrics_fn = metrics_fn.to(device)
    metrics_fn.reset()
    with torch.no_grad():
        loss = 0
        for x, y in dataloader:
            x, y = x.to(device), y.to(device)
            y_pred = model(x)
            loss += loss_fn(torch.log(y_pred), y).sum()
            metrics_fn.update(y_pred, y)
        
        loss = loss / len(dataloader.dataset)
        metrics = metrics_fn.compute()

    return loss, metrics