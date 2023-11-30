import torch
from torch import nn
from torch.optim import Adam
from transformers import T5Config, T5ForConditionalGeneration
from dataloader import DataLoaderForT5
from tqdm import tqdm
import os
from galvatron.utils import set_seed, distributed_dataloader, print_loss
from galvatron.core import initialize_galvatron, GalvatronProfiler
from galvatron.models.t5.T5Model_hybrid_parallel import get_hybrid_parallel_configs, construct_hybrid_parallel_model
from galvatron.models.t5.hf_configs import t5_hf_configs, set_model_config, model_name, model_layer_configs
from galvatron.models.t5.arguments import model_args

def loss_func(labels, outputs):
    loss_fct = nn.CrossEntropyLoss(ignore_index=-100)
    logits = outputs[0]
    labels = labels[0]
    loss = loss_fct(logits.view(-1, logits.size(-1)), labels.view(-1))
    return loss

def train(args):
    local_rank = args.local_rank
    rank = torch.distributed.get_rank()
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    world_size = torch.distributed.get_world_size()

    config = T5Config.from_pretrained(t5_hf_configs(args.model_size))
    config = set_model_config(config, args)
    if local_rank == 0:
        print(config)
    
    hybrid_parallel_configs = get_hybrid_parallel_configs(model_config=config, training_args=args)
    if local_rank == 0:
        print("Creating Model...")
    t5_model = T5ForConditionalGeneration(config)
    model = construct_hybrid_parallel_model(
        model=t5_model, 
        model_config=config, 
        training_args=args, 
        hybrid_parallel_configs=hybrid_parallel_configs
    )
    
    # from galvatron.models.t5 import t5_model_hp
    # model = t5_model_hp(config, args)
    
    if local_rank == 0:
        print("Creating Dataset...")
    trainloader = distributed_dataloader(
        dataset=DataLoaderForT5(args, device),
        global_bsz=args.global_train_batch_size,
        shuffle=True,
        args=args
    )
    
    optimizer = Adam(model.parameters(), lr=args.lr, weight_decay=args.adam_weight_decay)

    path = os.path.dirname(os.path.abspath(__file__))
    profiler = GalvatronProfiler(args)
    profiler.set_profiler_dist(path, model_layer_configs(config), model_name(config))
    
    profiler.profile_memory(0, "After creating model")
    if local_rank == 0:
        print("Start training...")
    for ep in range(args.epochs):
        if not args.check_loss and not args.profile:
            trainloader = tqdm(trainloader)
        for iter, batch in enumerate(trainloader):
            profiler.profile_time_start(iter)
            profiler.profile_memory(iter, "Before Forward")

            input_ids, attention_mask, labels = batch
            batch = [[input_ids, labels, attention_mask], [labels]]
            
            loss = model.forward_backward(batch, iter, profiler, loss_func)
            
            profiler.profile_memory(iter, "After Backward")
            
            optimizer.step()
            
            profiler.profile_memory(iter, "After optimizer_step")
            
            optimizer.zero_grad()
            
            print_loss(args, loss, ep, iter)

            profiler.post_profile_memory(iter)
            profiler.profile_time_end(iter)

if __name__ == '__main__':
    args = initialize_galvatron(model_args, mode='train_dist')
    set_seed()
    train(args)