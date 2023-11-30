import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Adam
from transformers import T5Config, T5ForConditionalGeneration
from dataloader import DataLoaderForT5
from tqdm import tqdm
import numpy as np
from galvatron.utils import set_seed, print_loss
from galvatron.core import initialize_galvatron, GalvatronProfiler
from galvatron.models.t5.hf_configs import t5_hf_configs, set_model_config
from galvatron.models.t5.arguments import model_args

def model_forward(model, input_ids, attention_mask, labels):
    return model(input_ids=input_ids, attention_mask=attention_mask, labels=labels).loss

def train(args):
    cuda_condition = torch.cuda.is_available()
    device = torch.device("cuda:%d"%args.gpu_id if cuda_condition else "cpu")

    config = T5Config.from_pretrained(t5_hf_configs(args.model_size))
    config = set_model_config(config, args, False)
    print(config)

    print("Creating Model...")
    model = T5ForConditionalGeneration(config)
    model.to(device)
    
    print("Creating Dataloader...")
    dataset = DataLoaderForT5(args, device)
    trainloader = DataLoader(
        dataset=dataset,
        batch_size=args.global_train_batch_size,
        shuffle=False
    )
    
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
            
            input_ids, attention_mask, labels = batch
            
            profiler.profile_memory(iter, "Before Forward")

            loss = model_forward(model, input_ids, attention_mask, labels)

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