import argparse
from pathlib import Path

import yaml


# Configuration dictionary generator
def get_config(cfg_type):
    if cfg_type == "vq":
        return {
            "wandb": {"project": "VQTokenizer"},
            "data": {
                "pdb_dir": "./data",
                "patch_size": 8,
                "batch_size": 64,
                "num_workers": 12,
            },
            "model": {
                "hidden_dim": 768,
                "latent_dim": 512,
                "num_embeddings": 768,
                "nhead": 16,
                "learning_rate": 1e-3,
            },
            "trainer": {
                "max_epochs": 50,
                "accelerator": "auto",
                "checkpoint_dir": "./checkpoints",
                "checkpoint_name": "vqtokenizer-{epoch:02d}-{val_total_loss:.4f}",
                "save_top_k": 5,
                "monitor": "val_total_loss",
                "monitor_mode": "min",
                "log_every_n_steps": 100,
                "val_check_interval": 0.25,
                "final_model_path": "./weight/final_model.ckpt",
                "precision": "bf16-mixed",
                "strategy": "auto",
            },
        }
    elif cfg_type == "lfq":
        return {
            "wandb": {"project": "VQTokenizer"},
            "data": {
                "pdb_dir": "../data",
                "patch_size": 8,
                "lmdb_dir": "./LMDB",
                "batch_size": 64,
                "num_workers": 12,
            },
            "model": {
                "hidden_dim": 1024,
                "latent_dim": 8,
                "nhead": 16,
                "learning_rate": 4e-4,
                "temperature": 1.0,
                "commitment_cost": 0.25,
                "lr_peak": 4e-4,  # 峰值学习率
                "lr_min": 4e-5,  # 最小学习率
                "lr_warmup_ratio": 0.02,  # warmup步数占总步数的比例
                "lr_decay_ratio": 0.9,  # 衰减所占训练步数比例
                "weight_decay": 0.01,  # 权重衰减
            },
            "trainer": {
                "max_epochs": 50,
                "accelerator": "auto",
                "checkpoint_dir": "./checkpoints",
                "checkpoint_name": "lfqtokenizer-{epoch:02d}-{val_total_loss:.4f}",
                "save_top_k": 5,
                "monitor": "val_total_loss",
                "monitor_mode": "min",
                "log_every_n_steps": 100,
                "val_check_interval": 0.25,
                "final_model_path": "./weight/final_model.ckpt",
                "precision": "bf16-mixed",
                "strategy": "auto",
            },
        }
    else:
        raise ValueError("Argument 'type' must be either 'lfq' or 'vq'.")


def main():
    parser = argparse.ArgumentParser(description="Generate default training config file.")
    parser.add_argument("--type", required=True, choices=["lfq", "vq"], help="Config type: lfq or vq")
    args = parser.parse_args()
    cfg_type = args.type
    config = get_config(cfg_type)
    output_path = Path(f"config/{cfg_type}_train.yml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)
    print(f"Default config file generated: {output_path.resolve()}")


if __name__ == "__main__":
    main()
