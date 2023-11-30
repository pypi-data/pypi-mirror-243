
def model_args(parser):
    group = parser.add_argument_group(title='Model Arguments')

    group.add_argument(
        "--model_size", type=str, default='vit-large', help="Model size.", choices=['vit-large', 'vit-huge', 'vit-huge-48']
    )
    group.add_argument(
        "--hidden_size", type=int, default=1024, help="Hidden size of transformer model",
    )
    group.add_argument(
        "--num_hidden_layers", type=int, default=24, help="Number of layers"
    )
    group.add_argument(
        "-a", "--num_attention_heads", type=int, default=16, help="Number of attention heads",
    )
    group.add_argument(
        "-s", "--seq_length", type=int, default=196, help="Maximum sequence len"
    )
    group.add_argument(
        "--image_size", type=int, default=224, help="Input image size."
    )
    group.add_argument(
        "--patch_size", type=int, default=16, help="Patch size of ViT."
    )
    group.add_argument(
        "--num_channels", type=int, default=3, help="Number of channels."
    )
    group.add_argument(
        "--num_classes", type=int, default=1000, help="Number of labels for image classification."
    )
    return parser

def layernum_arg_names():
    return ['num_hidden_layers']