import os
import glob
import shutil


def create_new_kg(select_datasets=["FB15k-237","Countries-S1", "Countries-S2", "Countries-S3", "UMLS", "KINSHIP"],
                  knowledge_graph_dir="KGs"):
    """

    Parameters
    ----------
    select_datasets: a list of strings indicating the name of a subfolder under knowledge_graph_dir
    knowledge_graph_dir:

    Returns
    -------

    """
    path_of_new_dataset_directory = f"{knowledge_graph_dir}/Combined"
    if os.path.exists(path_of_new_dataset_directory):
        shutil.rmtree(path_of_new_dataset_directory)

    os.makedirs(path_of_new_dataset_directory)
    path_of_train_set_of_new_dataset = f"{path_of_new_dataset_directory}/train.txt"
    with open(path_of_train_set_of_new_dataset, "w") as writer:
        for idv_dataset in os.listdir(knowledge_graph_dir):
            if idv_dataset == "README":
                continue
            # (1) Directory name of a specified data
            kg_dataset = knowledge_graph_dir + "/" + idv_dataset

            if idv_dataset in select_datasets:
                for sing_train_txt in os.listdir(kg_dataset):
                    if sing_train_txt == "train.txt":
                        print(
                            f"Reading {kg_dataset}/{sing_train_txt} and writhing into {path_of_train_set_of_new_dataset}")
                        with open(f"{kg_dataset}/{sing_train_txt}", "r") as r:
                            for i in r.readlines():
                                writer.write(i)
    return path_of_train_set_of_new_dataset

if __name__ == '__main__':
    create_new_kg()
