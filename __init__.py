# Checkpoint Config Loader
# Created by DarkDinDoN
# Version: 0.0.1

import comfy.samplers
from nodes import CheckpointLoaderSimple, MAX_RESOLUTION


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
            steps_total = 0

        out = super().load_checkpoint(**kwargs)
        print(out)
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
    "CheckpointAutomaticConfig": "Checkpoint Automatic Loader"
}
