from dicee import Execute, KGE
from dicee.config import Namespace
import shutil
import pandas as pd
from dicee.static_funcs import create_recipriocal_triples, get_er_vocab
from dicee.eval_static_funcs import evaluate_link_prediction_performance_with_bpe_reciprocals
from combine_knowledge_graph import create_new_kg

# (0) Generate a directory containing a concat version of given knowledge graphs
path_of_merged_kg = create_new_kg(
    select_datasets=[  # "FB15k-237",
        "Countries-S1", "Countries-S2", "Countries-S3",
        "UMLS",
        "KINSHIP"],
    knowledge_graph_dir="KGs")
# (1) Train a KGE with byte pair encoding.
args = Namespace()
args.model = "Keci"
args.p = 0
args.q = 1
args.num_epochs = 1
args.lr = 0.001
args.path_single_kg = path_of_merged_kg
args.scoring_technique = 'KvsAll'
args.eval_model = 'train_val_test'
args.byte_pair_encoding = True
result = Execute(args).start()
# (2) Load a pre-trained model.
model = KGE(result["path_experiment_folder"])


def prepare_dataset_for_eval(p):
    # Evaluate on UMLS
    train_triples = create_recipriocal_triples(pd.read_csv(p + "/train.txt",
                                                           sep="\s+",
                                                           header=None, usecols=[0, 1, 2],
                                                           names=['subject', 'relation', 'object'],
                                                           dtype=str)).values.tolist()
    valid_triples = create_recipriocal_triples(pd.read_csv(p + "/valid.txt",
                                                           sep="\s+",
                                                           header=None, usecols=[0, 1, 2],
                                                           names=['subject', 'relation', 'object'],
                                                           dtype=str)).values.tolist()
    test_triples = create_recipriocal_triples(pd.read_csv(p + "/test.txt",
                                                          sep="\s+",
                                                          header=None, usecols=[0, 1, 2],
                                                          names=['subject', 'relation', 'object'],
                                                          dtype=str)).values.tolist()
    all_triples = train_triples + valid_triples + test_triples

    set_entities = set()
    for i in train_triples + valid_triples + test_triples:
        set_entities.add(i[0])
        set_entities.add(i[2])
    return train_triples, valid_triples, test_triples, sorted(list(set_entities)), get_er_vocab(all_triples)


# (3) Prepare train, valid, test datasets of a given path of a directory of knowledge graph
train_set, valid_set, test_st, entities, er_vocab = prepare_dataset_for_eval(p="KGs/UMLS")
# (4) Eval
results = evaluate_link_prediction_performance_with_bpe_reciprocals(model, within_entities=entities,
                                                                    triples=train_set,
                                                                    er_vocab=er_vocab)
print("Train:", results)
results = evaluate_link_prediction_performance_with_bpe_reciprocals(model,
                                                                    within_entities=entities,
                                                                    triples=valid_set,
                                                                    er_vocab=er_vocab)
print("Val:", results)
results = evaluate_link_prediction_performance_with_bpe_reciprocals(model, within_entities=entities,
                                                                    triples=test_st,
                                                                    er_vocab=er_vocab)

print("Test:", results)
