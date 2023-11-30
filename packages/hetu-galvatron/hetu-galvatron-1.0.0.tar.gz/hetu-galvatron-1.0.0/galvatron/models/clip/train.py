import torch
from torch.utils.data import DataLoader
from torch.optim import Adam
from transformers import CLIPModel, CLIPConfig
from dataloader import DataLoaderForCLIP
from tqdm import tqdm
from galvatron.utils import set_seed, print_loss, print_param_num
from galvatron.core import initialize_galvatron, GalvatronProfiler
from galvatron.models.clip.hf_configs import clip_hf_configs, set_model_config
from galvatron.models.clip.arguments import model_args

def model_forward(model, input_ids, attention_mask, pixel_values):
    loss = model(input_ids=input_ids, 
                 attention_mask=attention_mask, 
                 pixel_values=pixel_values, 
                 return_loss=True).loss
    return loss

def train(args):
    cuda_condition = torch.cuda.is_available()
    device = torch.device("cuda:%d"%args.gpu_id if cuda_condition else "cpu")

    config = CLIPConfig.from_pretrained(clip_hf_configs(args.model_size))
    set_model_config(config, args)
    print(config)
    
    print("Creating Model...")
    model = CLIPModel(config)
    print_param_num(model)
    model.to(device)
    
    print("Creating Dataloader...")
    dataset = DataLoaderForCLIP(config, device)
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
            
            input_ids, attention_mask, pixel_values = batch
            
            profiler.profile_memory(iter, "Before Forward")

            loss = model_forward(model, input_ids, attention_mask, pixel_values)

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