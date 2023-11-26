import argparse
import logging
import os
import random

import hkkang_utils.file as file_utils
from torch.backends import cudnn
from utils.utils import *

from DBAnomTransformer.solver import Solver

logger = logging.getLogger("main")


def main(config):
    cudnn.benchmark = True
    # Create directories if not exist
    if not os.path.exists(config.model_dir_path):
        mkdir(config.model_dir_path)

    # Create solver
    solver = Solver(vars(config))

    # Run solver
    if config.mode == "train":
        solver.train()
    elif config.mode == "test":
        solver.test()
    elif config.mode == "infer":
        # Load data to infer
        data_path = "dataset/EDA/raw_data/workload_spike_1.csv"
        # Perform inference
        score, is_anomaly, anomaly_cause = solver.infer(data_path=data_path)
        # Save result
        result = {
            "score": score,
            "is_anomaly": is_anomaly,
            "anomaly_cause": anomaly_cause,
        }
        file_utils.write_json_file(result, "results/EDA/result.json")
    return solver


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--num_epochs", type=int, default=20)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--win_size", type=int, default=25)
    parser.add_argument("--input_c", type=int, default=200)
    parser.add_argument("--output_c", type=int, default=200)
    parser.add_argument("--batch_size", type=int, default=1024)
    parser.add_argument("--pretrained_model", type=str, default=None)
    parser.add_argument("--dataset", type=str, default="DBS")
    parser.add_argument(
        "--mode", type=str, default="train", choices=["train", "test", "infer"]
    )
    parser.add_argument("--dataset_path", type=str, default=None)
    parser.add_argument("--model_dir_path", type=str, default="checkpoints")
    parser.add_argument("--anormly_ratio", type=float, default=0.5)
    parser.add_argument("--step_size", type=int, default=25)
    parser.add_argument("--random_seed", type=int, default=25)
    parser.add_argument("--find_best", type=bool, default=True)
    parser.add_argument("--add_stats", type=bool, default=False)
    parser.add_argument("--output_path", type=str, default="results/")
    parser.add_argument("--add_classifier", type=bool, default=False)
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s %(levelname)s %(name)s] %(message)s",
        datefmt="%m/%d %H:%M:%S",
        level=logging.INFO,
    )

    # Parse arguments
    config = parse_args()
    args = vars(config)
    random.seed(args["random_seed"])
    logger.info("------------ Options -------------")
    for k, v in sorted(args.items()):
        logger.info("%s: %s" % (str(k), str(v)))
    logger.info("-------------- End ----------------")
    main(config)
