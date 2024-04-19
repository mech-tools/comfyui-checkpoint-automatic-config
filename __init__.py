# Checkpoint Automatic Config
# Created by DarkDinDoN

import os
import yaml
import comfy.samplers
from nodes import CheckpointLoaderSimple, MAX_RESOLUTION

script_dir = os.path.dirname(__file__)


class CheckpointAutomaticConfig(CheckpointLoaderSimple):
    @classmethod
    def INPUT_TYPES(s):
        types = super().INPUT_TYPES()
        types["required"].update({
            "automatic_config": ("BOOLEAN", {"default": True}),
            "steps_total": ("INT", {
                "default": 5,
                "min": 1,
                "max": MAX_RESOLUTION,
                "step": 1,
            }),
            "cfg": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 0.1,
                    }),
            "sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
            "scheduler": (comfy.samplers.KSampler.SCHEDULERS,),
        })
        return types

    RETURN_TYPES = CheckpointLoaderSimple.RETURN_TYPES + (
        "INT",
        "FLOAT",
        comfy.samplers.KSampler.SAMPLERS,
        comfy.samplers.KSampler.SCHEDULERS
    )

    RETURN_NAMES = CheckpointLoaderSimple.RETURN_TYPES + (
        "STEPS",
        "CFG",
        "SAMPLER",
        "SCHEDULER"
    )

    def load_checkpoint(self, automatic_config, steps_total, cfg, sampler_name, scheduler, **kwargs):
        if automatic_config:
            with open(os.path.join(script_dir, "models_config.yaml"), 'r') as stream:
                config_file = yaml.safe_load(stream)
            if kwargs["ckpt_name"] in config_file:
                steps_total = config_file[kwargs["ckpt_name"]]["steps_total"]
                cfg = config_file[kwargs["ckpt_name"]]["cfg"]
                sampler_name = config_file[kwargs["ckpt_name"]]["sampler_name"]
                scheduler = config_file[kwargs["ckpt_name"]]["scheduler"]
                print(
                    "======== Applying checkpoint automatic configuration: steps: {} | cfg: {} | sampler: {} | scheduler: {} ========".format(steps_total, cfg, sampler_name, scheduler))
            else:
                raise Exception(
                    "Automatic checkpoint configuration: unknown checkpoint. Disable \"automatic_config\" to use this checkpoint.")

        out = super().load_checkpoint(**kwargs)
        return out + (
            steps_total,
            cfg,
            sampler_name,
            scheduler
        )

    CATEGORY = "Checkpoint Config Loader"


NODE_CLASS_MAPPINGS = {
    "CheckpointAutomaticConfig": CheckpointAutomaticConfig
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CheckpointAutomaticConfig": "Checkpoint Automatic Config"
}
