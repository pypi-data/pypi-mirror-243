import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from transformers import SwinConfig, SwinForImageClassification
from dataloader import DataLoaderForSwin
from tqdm import tqdm
import numpy as np
from galvatron.utils import set_seed, print_loss
from galvatron.core import initialize_galvatron, GalvatronProfiler
from galvatron.models.swin.hf_configs import vit_hf_configs, set_model_config
from galvatron.models.swin.arguments import model_args

def model_forward(model, pixel_values, labels):
    return model(pixel_values=pixel_values, labels=labels).loss

def train(args):
    cuda_condition = torch.cuda.is_available()
    device = torch.device("cuda:%d"%args.gpu_id if cuda_condition else "cpu")

    config = SwinConfig.from_pretrained(vit_hf_configs(args.model_size))
    config = set_model_config(config, args, False)
    print(config)

    print("Creating Model...")
    model = SwinForImageClassification(config)
    model.to(device)
    
    print("Creating Dataloader...")
    dataset = DataLoaderForSwin(config, device)
    trainloader = DataLoader(
        dataset=dataset,
        batch_size=args.global_train_batch_size,
        shuffle=False
    )
    print(config.num_labels)
    
    optimizer = Adam(model.parameters(), lr=args.lr, weight_decay=args.adam_weight_decay)

    profiler = GalvatronProfiler(args)
    profiler.set_profiler_single()

    profiler.profile_memory(0, "After creating model")
    print("Start training...")
    for ep in range(args.epochs):
        if not args.check_loss and not args.profile:
            trainloader = tqdm(trainloader)
        for iter, batch in enumerate(trainloader):
            profiler.profile_time_start(iter)
            
            pixel_values, labels = batch
            
            profiler.profile_memory(iter, "Before Forward")

            loss = model_forward(model, pixel_values, labels)

            profiler.profile_memory(iter, "After Forward")

            loss.backward()

            profiler.profile_memory(iter, "After Backward")
            
            optimizer.step()

            profiler.profile_memory(iter, "After optimizer_step")
            
            optimizer.zero_grad()

            print_loss(args, loss, ep, iter)
            
            profiler.post_profile_memory(iter)
            profiler.profile_time_end(iter)

if __name__ == '__main__':
    args = initialize_galvatron(model_args, mode='train')
    set_seed()
    train(args)