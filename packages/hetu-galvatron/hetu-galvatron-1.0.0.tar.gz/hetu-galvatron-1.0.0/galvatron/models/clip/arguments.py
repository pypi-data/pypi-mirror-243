
def model_args(parser):
    group = parser.add_argument_group(title='our arguments')

    group.add_argument(
        "--model_size", type=str, default='vit-L-14', help="CLIP model type."
    )
    group.add_argument(
        "--num_hidden_layers_text", type=int, default=12, help="Number of layers"
    )
    group.add_argument(
        "--num_hidden_layers_vision", type=int, default=12, help="Number of layers"
    )

    return parser

def layernum_arg_names():
    return ['num_hidden_layers_vision', 'num_hidden_layers_text']