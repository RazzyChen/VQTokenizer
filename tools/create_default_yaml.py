import argparse
from pathlib import Path

import yaml


# 配置字典生成函数
def get_config(cfg_type):
    if cfg_type == "vq":
        return {
            "wandb": {"project": "VQTokenizer"},
            "data": {"pdb_dir": "./data", "patch_size": 8, "batch_size": 64, "num_workers": 12},
            "model": {"hidden_dim": 768, "latent_dim": 512, "num_embeddings": 768, "nhead": 16, "learning_rate": 1e-3},
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
                "precision": "fp16-mixed",
                "strategy": "ddp",
            },
        }
    elif cfg_type == "lfq":
        return {
            "wandb": {"project": "LFQTokenizer"},
            "data": {"pdb_dir": "./data", "patch_size": 8, "batch_size": 64, "num_workers": 12},
            "model": {
                "hidden_dim": 768,
                "latent_dim": 512,
                "num_embeddings": 768,
                "nhead": 16,
                "learning_rate": 1e-3,
                "temperature": 1.0,
                "commitment_cost": 0.25,
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
                "precision": "fp16-mixed",
                "strategy": "ddp",
            },
        }
    else:
        raise ValueError("type 参数必须为 'lfq' 或 'vq'")


def main():
    parser = argparse.ArgumentParser(description="生成默认训练 config")
    parser.add_argument("--type", required=True, choices=["lfq", "vq"], help="config 类型: lfq 或 vq")
    args = parser.parse_args()
    cfg_type = args.type
    config = get_config(cfg_type)
    output_path = Path(f"config/{cfg_type}_train.yml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)
    print(f"{cfg_type}_train.yml at {output_path.resolve()}")


if __name__ == "__main__":
    main()
