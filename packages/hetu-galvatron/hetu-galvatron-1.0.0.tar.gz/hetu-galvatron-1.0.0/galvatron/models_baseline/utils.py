
import torch
import numpy as np
import random
from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import checkpoint_wrapper, CheckpointImpl

def wrap_modules_checkpoint(module_list, checkpoint_flags, wrap_block_name=None):
    m = module_list
    assert len(m) == len(checkpoint_flags)
    for i in range(len(m)):
        if checkpoint_flags[i]:
            if wrap_block_name is not None:
                m[i] = apply_ckpt(m[i], checkpoint_wrapper, wrap_block_name)
            else:
                m[i] = checkpoint_wrapper(m[i])
    return module_list

def set_seed():
    seed = 123
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

def print_param_num(model):
    print("Total number of paramerters in networks is {}  ".format(sum(x.numel() for x in model.parameters())))

class CommGroup(object):
    def __init__(self, ranks):
        assert isinstance(ranks, list) or isinstance(ranks, range), 'Rank list or range should be provided to create a CommGroup!'
        self.ranks = sorted(list(set(list(ranks))))
        self.size = len(self.ranks)
        self.group = torch.distributed.new_group(self.ranks)
    def has_rank(self, rank):
        if rank in self.ranks:
            self.intra_group_id = self.ranks.index(rank)
            return True
        return False
    def allgather(self, input):
        return gather_from_group(input, self.group)
    def split(self, input):
        return split_to_group(input, self.group)
    
    def print(self):
        print(self.ranks, end = ' ')
