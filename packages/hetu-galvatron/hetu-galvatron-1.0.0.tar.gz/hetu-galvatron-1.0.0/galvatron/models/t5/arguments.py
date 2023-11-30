
def model_args(parser):
    group = parser.add_argument_group(title='Model Arguments')

    group.add_argument(
        "--model_size", type=str, default='t5-large', help="Model size.", choices=['t5-base', 't5-large']
    )
    group.add_argument(
        "--hidden_size", type=int, default=1024, help="Hidden size of transformer model",
    )
    group.add_argument(
        "--num_encoder_layers", type=int, default=24, help="Number of encoder layers"
    )
    group.add_argument(
        "--num_decoder_layers", type=int, default=24, help="Number of decoder layers"
    )
    group.add_argument(
        "-a", "--num_attention_heads", type=int, default=16, help="Number of attention heads",
    )
    group.add_argument(
        "-s", "--seq_length", type=int, default=512, help="Maximum sequence len"
    )
    group.add_argument(
        "--vocab_size", type=int, default=32128, help="Total number of vocab"
    )
    group.add_argument("--max_predictions_per_seq", type=int, default=20)
    return parser

def layernum_arg_names():
    return ['num_encoder_layers', 'num_decoder_layers']