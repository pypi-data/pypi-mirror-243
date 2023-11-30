
def model_args(parser):
    group = parser.add_argument_group(title='Model Arguments')

    group.add_argument(
        "--model_size", type=str, default='swin-huge-32', help="Model size.", choices=['swin-huge-32', 'swin-huge-48']
    )
    group.add_argument(
        "--drop_path_rate", type=float, default=0.2, help="Drop path rate."
    )
    group.add_argument(
        "--embed_dim", type=int, default=320, help="Embed dim.",
    )
    group.add_argument(
        "-s", "--seq_length", type=int, default=196, help="Maximum sequence len"
    )
    group.add_argument(
        "--depths", nargs='+', type=int, default=[1], help="Depths."
    )
    group.add_argument(
        "--num_heads", nargs='+', type=int, default=[2], help="Num heads."
    )
    group.add_argument(
        "--window_size", type=int, default=7, help="Window size."
    )
    group.add_argument(
        "--image_size", type=int, default=224, help="Input image size."
    )
    group.add_argument(
        "--patch_size", type=int, default=16, help="Patch size of Swin Transformer."
    )
    group.add_argument(
        "--num_channels", type=int, default=3, help="Number of channels."
    )
    group.add_argument(
        "--num_classes", type=int, default=1000, help="Number of labels for image classification."
    )
    return parser

def layernum_arg_names():
    return ['depths']