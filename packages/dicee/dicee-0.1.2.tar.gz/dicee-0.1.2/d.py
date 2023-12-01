from dicee.executer import Execute
from dicee.config import Namespace
args = Namespace()
args.dataset_dir = 'KGs/UMLS'
args.model = 'Keci'
args.p = 0
args.q = 1
args.embedding_dim = 32
args.scoring_technique = 'KvsAll'
args.optim = 'Adam'
args.num_epochs = 500
args.batch_size = 1024
args.lr = 0.1
args.input_dropout_rate = 0.0
args.hidden_dropout_rate = 0.0
args.feature_map_dropout_rate = 0.0
args.byte_pair_encoding = True
args.read_only_few = None
args.sample_triples_ratio = None
args.trainer = 'PL'
result = Execute(args).start()

"""
assert result['Train']['MRR'] >= 0.88
assert result['Val']['MRR'] >= 0.78
assert result['Test']['MRR'] >= 0.78


Took 0.0189 secs | Current Memory Usage  604.05 in MB
Total Runtime: 66.459 seconds
Evaluate Keci on BPE Train set: Evaluate Keci on BPE Train set
{'H@1': 0.9297354294478528, 'H@3': 0.9895513803680982, 'H@10': 0.9994248466257669, 'MRR': 0.9598961065242699}
Evaluate Keci on BPE Validation set: Evaluate Keci on BPE Validation set
{'H@1': 0.7331288343558282, 'H@3': 0.9003067484662577, 'H@10': 0.9716257668711656, 'MRR': 0.8227809934517264}
Evaluate Keci on BPE Test set: Evaluate Keci on BPE Test set
{'H@1': 0.7322239031770046, 'H@3': 0.9062027231467473, 'H@10': 0.9757942511346445, 'MRR': 0.8275301849930883}
Total Runtime: 67.560 seconds
0.9598961065242699
0.8275301849930883

Process finished with exit code 0
"""