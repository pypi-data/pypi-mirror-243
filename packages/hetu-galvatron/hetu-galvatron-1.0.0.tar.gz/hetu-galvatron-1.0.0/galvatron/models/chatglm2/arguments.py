
def model_args(parser):
    group = parser.add_argument_group(title='Model Arguments')

    group.add_argument(
        "--model_size", type=str, default='chatglm2-6b', help="Model size.", choices=['chatglm2-6b']
    )
    group.add_argument(
        "--hidden_size", type=int, default=4096, help="Hidden size of transformer model",
    )
    group.add_argument(
        "--ffn_hidden_size", type=int, default=13696, help="Hidden size of transformer feed-forward network",
    )
    group.add_argument(
        "--num_hidden_layers", type=int, default=28, help="Number of layers"
    )
    group.add_argument(
        "-a", "--num_attention_heads", type=int, default=32, help="Number of attention heads",
    )
    group.add_argument(
        "-s", "--seq_length", type=int, default=2048, help="Maximum sequence len"
    )
    group.add_argument(
        "--vocab_size", type=int, default=65024, help="Total number of vocab"
    )
    group.add_argument("--max_predictions_per_seq", type=int, default=20)
    parser.add_argument(
        "--multi_query_attention", type=int, default=1, help="Apply multi-query attention", choices=[0, 1]
    )
    return parser

def layernum_arg_names():
    return ['num_hidden_layers']