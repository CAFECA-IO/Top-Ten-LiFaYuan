prompt_text_1 = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "cfg": 8,
            "denoise": 1,
            "latent_image": [
                "5",
                0
            ],
            "model": [
                "4",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "sampler_name": "euler",
            "scheduler": "normal",
            "seed": 8566257,
            "steps": 20
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "dreamshaper_8.safetensors"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "batch_size": 1,
            "height": 512,
            "width": 512
        }
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "masterpiece best quality girl"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "bad hands"
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        }
    }
}
"""

prompt_text_2 = """
{
  "client_id": "c020352da0054f058571d77b8ae64cd7",
  "prompt": {
    "2": {
      "inputs": {
        "seed": 119518652754456,
        "steps": 20,
        "cfg": 7,
        "sampler_name": "ddpm",
        "scheduler": "normal",
        "denoise": 1,
        "preview_method": "auto",
        "vae_decode": "true",
        "model": ["4", 0],
        "positive": ["8", 0],
        "negative": ["15", 2],
        "latent_image": ["15", 3],
        "optional_vae": ["15", 4]
      },
      "class_type": "KSampler (Efficient)"
    },
    "4": {
      "inputs": {
        "model_name": "v3_sd15_mm.ckpt",
        "beta_schedule": "sqrt_linear (AnimateDiff)",
        "motion_scale": 1.08,
        "apply_v2_models_properly": true,
        "model": ["15", 0],
        "context_options": ["6", 0]
      },
      "class_type": "ADE_AnimateDiffLoaderWithContext"
    },
    "6": {
      "inputs": {
        "context_length": 16,
        "context_stride": 1,
        "context_overlap": 2,
        "closed_loop": false,
        "fuse_method": "pyramid",
        "use_on_equal_length": false,
        "start_percent": 0,
        "guarantee_steps": 1
      },
      "class_type": "ADE_LoopedUniformContextOptions"
    },
    "7": {
      "inputs": {
        "frame_rate": 8,
        "loop_count": 0,
        "filename_prefix": "AnimateDiff",
        "format": "video/h264-mp4",
        "pix_fmt": "yuv420p",
        "crf": 22,
        "save_metadata": false,
        "pingpong": false,
        "save_output": false,
        "images": ["33", 0]
      },
      "class_type": "VHS_VideoCombine"
    },
    "8": {
      "inputs": {
        "text": "\"0\" :\"Anime girl closed eyes (happy:1.2) listening to music,seaside\",\n\"6\" :\"Anime girl open eyes (happy:1.2) listening to music,seaside\",\n\"9\" :\"Anime girl open eyes (happy, smiling:1.2) listening to music,seaside\"\n\n",
        "max_frames": 16,
        "print_output": false,
        "pre_text": "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n",
        "start_frame": 0,
        "end_frame": 0,
        "clip": ["15", 5]
      },
      "class_type": "BatchPromptSchedule"
    },
    "15": {
      "inputs": {
        "ckpt_name": "dreamshaper_8.safetensors",
        "vae_name": "Baked VAE",
        "clip_skip": -1,
        "lora_name": "SD1.5/animatediff/v3_sd15_adapter.ckpt",
        "lora_model_strength": 0.8,
        "lora_clip_strength": 0.8,
        "positive": "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n",
        "negative": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
        "token_normalization": "none",
        "weight_interpretation": "comfy",
        "empty_latent_width": 512,
        "empty_latent_height": 512,
        "batch_size": 16
      },
      "class_type": "Efficient Loader"
    },
    "25": {
      "inputs": {
        "strength": 0.8,
        "start_percent": 0.062,
        "end_percent": 0.8,
        "positive": ["8", 0],
        "negative": ["15", 2],
        "control_net": ["38", 0],
        "image": ["2", 5]
      },
      "class_type": "ACN_AdvancedControlNetApply"
    },
    "28": {
      "inputs": {
        "seed": 1037631207225729,
        "steps": 25,
        "cfg": 8.5,
        "sampler_name": "ddpm",
        "scheduler": "normal",
        "denoise": 0.7000000000000001,
        "model": ["4", 0],
        "positive": ["25", 0],
        "negative": ["25", 1],
        "latent_image": ["36", 0]
      },
      "class_type": "KSampler"
    },
    "31": {
      "inputs": { "samples": ["28", 0], "vae": ["2", 4] },
      "class_type": "VAEDecode"
    },
    "32": {
      "inputs": {
        "sharpen_radius": 1,
        "sigma": 0.4,
        "alpha": 0.6,
        "image": ["31", 0]
      },
      "class_type": "ImageSharpen"
    },
    "33": {
      "inputs": {
        "ckpt_name": "rife47.pth",
        "clear_cache_after_n_frames": 10,
        "multiplier": 3,
        "fast_mode": true,
        "ensemble": true,
        "scale_factor": 1,
        "frames": ["32", 0]
      },
      "class_type": "RIFE VFI"
    },
    "36": {
      "inputs": {
        "upscale_method": "nearest-exact",
        "scale_by": 1.5,
        "samples": ["2", 3]
      },
      "class_type": "LatentUpscaleBy"
    },
    "38": {
      "inputs": { "control_net_name": "controlnet_checkpoint.ckpt" },
      "class_type": "ControlNetLoader"
    }
  },
  "extra_data": {
    "extra_pnginfo": {
      "workflow": {
        "last_node_id": 38,
        "last_link_id": 48,
        "nodes": [
          {
            "id": 6,
            "type": "ADE_LoopedUniformContextOptions",
            "pos": [227, -232],
            "size": { "0": 317.4000244140625, "1": 246 },
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [
              {
                "name": "prev_context",
                "type": "CONTEXT_OPTIONS",
                "link": null
              },
              { "name": "view_opts", "type": "VIEW_OPTS", "link": null }
            ],
            "outputs": [
              {
                "name": "CONTEXT_OPTS",
                "type": "CONTEXT_OPTIONS",
                "links": [8],
                "shape": 3
              }
            ],
            "properties": {
              "Node name for S&R": "ADE_LoopedUniformContextOptions"
            },
            "widgets_values": [16, 1, 2, false, "pyramid", false, 0, 1]
          },
          {
            "id": 9,
            "type": "PrimitiveNode",
            "pos": [233, 791],
            "size": { "0": 210, "1": 82 },
            "flags": {},
            "order": 1,
            "mode": 0,
            "outputs": [
              {
                "name": "INT",
                "type": "INT",
                "links": [11, 21],
                "slot_index": 0,
                "widget": { "name": "max_frames" }
              }
            ],
            "properties": { "Run widget replace on values": false },
            "widgets_values": [16, "fixed"]
          },
          {
            "id": 16,
            "type": "PrimitiveNode",
            "pos": [1027, 892],
            "size": { "0": 210, "1": 76.00000762939453 },
            "flags": {},
            "order": 2,
            "mode": 0,
            "outputs": [
              {
                "name": "STRING",
                "type": "STRING",
                "links": [24],
                "widget": { "name": "pre_text" }
              }
            ],
            "properties": { "Run widget replace on values": false },
            "widgets_values": [
              "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n"
            ]
          },
          {
            "id": 15,
            "type": "Efficient Loader",
            "pos": [181, 102],
            "size": { "0": 400, "1": 606 },
            "flags": {},
            "order": 4,
            "mode": 0,
            "inputs": [
              { "name": "lora_stack", "type": "LORA_STACK", "link": null },
              {
                "name": "cnet_stack",
                "type": "CONTROL_NET_STACK",
                "link": null
              },
              {
                "name": "batch_size",
                "type": "INT",
                "link": 21,
                "widget": { "name": "batch_size" }
              }
            ],
            "outputs": [
              {
                "name": "MODEL",
                "type": "MODEL",
                "links": [22],
                "slot_index": 0,
                "shape": 3
              },
              {
                "name": "CONDITIONING+",
                "type": "CONDITIONING",
                "links": null,
                "shape": 3
              },
              {
                "name": "CONDITIONING-",
                "type": "CONDITIONING",
                "links": [29],
                "slot_index": 2,
                "shape": 3
              },
              {
                "name": "LATENT",
                "type": "LATENT",
                "links": [19],
                "slot_index": 3,
                "shape": 3
              },
              {
                "name": "VAE",
                "type": "VAE",
                "links": [20],
                "slot_index": 4,
                "shape": 3
              },
              {
                "name": "CLIP",
                "type": "CLIP",
                "links": [23],
                "slot_index": 5,
                "shape": 3
              },
              {
                "name": "DEPENDENCIES",
                "type": "DEPENDENCIES",
                "links": null,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "Efficient Loader" },
            "widgets_values": [
              "dreamshaper_8.safetensors",
              "Baked VAE",
              -1,
              "SD1.5/animatediff/v3_sd15_adapter.ckpt",
              0.8,
              0.8,
              "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n",
              "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
              "none",
              "comfy",
              512,
              512,
              16
            ],
            "color": "#222233",
            "bgcolor": "#333355",
            "shape": 1
          },
          {
            "id": 29,
            "type": "Reroute",
            "pos": [804, 497],
            "size": [75, 26],
            "flags": {},
            "order": 6,
            "mode": 0,
            "inputs": [{ "name": "", "type": "*", "link": 29 }],
            "outputs": [
              {
                "name": "",
                "type": "CONDITIONING",
                "links": [27, 28],
                "slot_index": 0
              }
            ],
            "properties": { "showOutputText": false, "horizontal": false }
          },
          {
            "id": 8,
            "type": "BatchPromptSchedule",
            "pos": [596, 679],
            "size": { "0": 400, "1": 318 },
            "flags": {},
            "order": 7,
            "mode": 0,
            "inputs": [
              { "name": "clip", "type": "CLIP", "link": 23 },
              {
                "name": "pre_text",
                "type": "STRING",
                "link": 24,
                "widget": { "name": "pre_text" }
              },
              {
                "name": "app_text",
                "type": "STRING",
                "link": null,
                "widget": { "name": "app_text" }
              },
              {
                "name": "pw_a",
                "type": "FLOAT",
                "link": null,
                "widget": { "name": "pw_a" }
              },
              {
                "name": "pw_b",
                "type": "FLOAT",
                "link": null,
                "widget": { "name": "pw_b" }
              },
              {
                "name": "pw_c",
                "type": "FLOAT",
                "link": null,
                "widget": { "name": "pw_c" }
              },
              {
                "name": "pw_d",
                "type": "FLOAT",
                "link": null,
                "widget": { "name": "pw_d" }
              },
              {
                "name": "max_frames",
                "type": "INT",
                "link": 11,
                "widget": { "name": "max_frames" }
              }
            ],
            "outputs": [
              {
                "name": "POS",
                "type": "CONDITIONING",
                "links": [30],
                "slot_index": 0,
                "shape": 3
              },
              {
                "name": "NEG",
                "type": "CONDITIONING",
                "links": null,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "BatchPromptSchedule" },
            "widgets_values": [
              "\"0\" :\"Anime girl closed eyes (happy:1.2) listening to music,seaside\",\n\"6\" :\"Anime girl open eyes (happy:1.2) listening to music,seaside\",\n\"9\" :\"Anime girl open eyes (happy, smiling:1.2) listening to music,seaside\"\n\n",
              16,
              false,
              "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n",
              "high quality, detailed, high resolution, 4k",
              0,
              0,
              0,
              0,
              0,
              0
            ]
          },
          {
            "id": 30,
            "type": "Reroute",
            "pos": [803, 562],
            "size": [75, 26],
            "flags": {},
            "order": 8,
            "mode": 0,
            "inputs": [{ "name": "", "type": "*", "link": 30 }],
            "outputs": [
              {
                "name": "",
                "type": "CONDITIONING",
                "links": [31, 32],
                "slot_index": 0
              }
            ],
            "properties": { "showOutputText": false, "horizontal": false }
          },
          {
            "id": 4,
            "type": "ADE_AnimateDiffLoaderWithContext",
            "pos": [627, -229],
            "size": { "0": 315, "1": 230 },
            "flags": {},
            "order": 5,
            "mode": 0,
            "inputs": [
              { "name": "model", "type": "MODEL", "link": 22 },
              {
                "name": "context_options",
                "type": "CONTEXT_OPTIONS",
                "link": 8
              },
              { "name": "motion_lora", "type": "MOTION_LORA", "link": null },
              { "name": "ad_settings", "type": "AD_SETTINGS", "link": null },
              {
                "name": "sample_settings",
                "type": "SAMPLE_SETTINGS",
                "link": null
              },
              { "name": "ad_keyframes", "type": "AD_KEYFRAMES", "link": null }
            ],
            "outputs": [
              {
                "name": "MODEL",
                "type": "MODEL",
                "links": [7, 35],
                "slot_index": 0,
                "shape": 3
              }
            ],
            "properties": {
              "Node name for S&R": "ADE_AnimateDiffLoaderWithContext"
            },
            "widgets_values": [
              "v3_sd15_mm.ckpt",
              "sqrt_linear (AnimateDiff)",
              1.08,
              true
            ]
          },
          {
            "id": 31,
            "type": "VAEDecode",
            "pos": [1971, 448],
            "size": { "0": 210, "1": 46 },
            "flags": {},
            "order": 13,
            "mode": 0,
            "inputs": [
              { "name": "samples", "type": "LATENT", "link": 38 },
              { "name": "vae", "type": "VAE", "link": 40 }
            ],
            "outputs": [
              {
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [39],
                "slot_index": 0,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "VAEDecode" }
          },
          {
            "id": 32,
            "type": "ImageSharpen",
            "pos": [2224, 405],
            "size": { "0": 315, "1": 106 },
            "flags": {},
            "order": 14,
            "mode": 0,
            "inputs": [{ "name": "image", "type": "IMAGE", "link": 39 }],
            "outputs": [
              {
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [41],
                "slot_index": 0,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "ImageSharpen" },
            "widgets_values": [1, 0.4, 0.6]
          },
          {
            "id": 28,
            "type": "KSampler",
            "pos": [1745, 107],
            "size": { "0": 315, "1": 262 },
            "flags": {},
            "order": 12,
            "mode": 0,
            "inputs": [
              { "name": "model", "type": "MODEL", "link": 35 },
              { "name": "positive", "type": "CONDITIONING", "link": 33 },
              { "name": "negative", "type": "CONDITIONING", "link": 34 },
              { "name": "latent_image", "type": "LATENT", "link": 47 }
            ],
            "outputs": [
              {
                "name": "LATENT",
                "type": "LATENT",
                "links": [38],
                "slot_index": 0,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "KSampler" },
            "widgets_values": [
              1037631207225729,
              "randomize",
              25,
              8.5,
              "ddpm",
              "normal",
              0.7000000000000001
            ]
          },
          {
            "id": 36,
            "type": "LatentUpscaleBy",
            "pos": [1596, 428],
            "size": { "0": 315, "1": 82 },
            "flags": {},
            "order": 10,
            "mode": 0,
            "inputs": [{ "name": "samples", "type": "LATENT", "link": 46 }],
            "outputs": [
              {
                "name": "LATENT",
                "type": "LATENT",
                "links": [47],
                "slot_index": 0,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "LatentUpscaleBy" },
            "widgets_values": ["nearest-exact", 1.5]
          },
          {
            "id": 33,
            "type": "RIFE VFI",
            "pos": [1849, 709],
            "size": { "0": 443.4000244140625, "1": 198 },
            "flags": {},
            "order": 15,
            "mode": 0,
            "inputs": [
              { "name": "frames", "type": "IMAGE", "link": 41 },
              {
                "name": "optional_interpolation_states",
                "type": "INTERPOLATION_STATES",
                "link": null
              }
            ],
            "outputs": [
              {
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [42],
                "slot_index": 0,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "RIFE VFI" },
            "widgets_values": ["rife47.pth", 10, 3, true, true, 1]
          },
          {
            "id": 25,
            "type": "ACN_AdvancedControlNetApply",
            "pos": [1307, 115],
            "size": { "0": 325.6000061035156, "1": 286 },
            "flags": {},
            "order": 11,
            "mode": 0,
            "inputs": [
              { "name": "positive", "type": "CONDITIONING", "link": 31 },
              { "name": "negative", "type": "CONDITIONING", "link": 28 },
              { "name": "control_net", "type": "CONTROL_NET", "link": 48 },
              { "name": "image", "type": "IMAGE", "link": 37 },
              { "name": "mask_optional", "type": "MASK", "link": null },
              {
                "name": "timestep_kf",
                "type": "TIMESTEP_KEYFRAME",
                "link": null
              },
              {
                "name": "latent_kf_override",
                "type": "LATENT_KEYFRAME",
                "link": null
              },
              {
                "name": "weights_override",
                "type": "CONTROL_NET_WEIGHTS",
                "link": null
              },
              { "name": "model_optional", "type": "MODEL", "link": null },
              { "name": "vae_optional", "type": "VAE", "link": null }
            ],
            "outputs": [
              {
                "name": "positive",
                "type": "CONDITIONING",
                "links": [33],
                "slot_index": 0,
                "shape": 3
              },
              {
                "name": "negative",
                "type": "CONDITIONING",
                "links": [34],
                "slot_index": 1,
                "shape": 3
              },
              {
                "name": "model_opt",
                "type": "MODEL",
                "links": null,
                "shape": 3
              }
            ],
            "properties": {
              "Node name for S&R": "ACN_AdvancedControlNetApply"
            },
            "widgets_values": [0.8, 0.062, 0.8, ""]
          },
          {
            "id": 2,
            "type": "KSampler (Efficient)",
            "pos": [1378, 667],
            "size": { "0": 325, "1": 562 },
            "flags": {},
            "order": 9,
            "mode": 0,
            "inputs": [
              { "name": "model", "type": "MODEL", "link": 7 },
              { "name": "positive", "type": "CONDITIONING", "link": 32 },
              { "name": "negative", "type": "CONDITIONING", "link": 27 },
              { "name": "latent_image", "type": "LATENT", "link": 19 },
              { "name": "optional_vae", "type": "VAE", "link": 20 },
              { "name": "script", "type": "SCRIPT", "link": null }
            ],
            "outputs": [
              { "name": "MODEL", "type": "MODEL", "links": null, "shape": 3 },
              {
                "name": "CONDITIONING+",
                "type": "CONDITIONING",
                "links": null,
                "shape": 3
              },
              {
                "name": "CONDITIONING-",
                "type": "CONDITIONING",
                "links": null,
                "shape": 3
              },
              {
                "name": "LATENT",
                "type": "LATENT",
                "links": [46],
                "slot_index": 3,
                "shape": 3
              },
              {
                "name": "VAE",
                "type": "VAE",
                "links": [40],
                "slot_index": 4,
                "shape": 3
              },
              {
                "name": "IMAGE",
                "type": "IMAGE",
                "links": [37],
                "slot_index": 5,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "KSampler (Efficient)" },
            "widgets_values": [
              -1,
              null,
              20,
              7,
              "ddpm",
              "normal",
              1,
              "auto",
              "true"
            ],
            "color": "#332233",
            "bgcolor": "#553355",
            "shape": 1
          },
          {
            "id": 38,
            "type": "ControlNetLoader",
            "pos": [934, 62],
            "size": { "0": 315, "1": 58 },
            "flags": {},
            "order": 3,
            "mode": 0,
            "outputs": [
              {
                "name": "CONTROL_NET",
                "type": "CONTROL_NET",
                "links": [48],
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "ControlNetLoader" },
            "widgets_values": ["controlnet_checkpoint.ckpt"]
          },
          {
            "id": 7,
            "type": "VHS_VideoCombine",
            "pos": [2395, 726],
            "size": [437.7029724121094, 310],
            "flags": {},
            "order": 16,
            "mode": 0,
            "inputs": [
              { "name": "images", "type": "IMAGE", "link": 42 },
              { "name": "audio", "type": "AUDIO", "link": null },
              {
                "name": "meta_batch",
                "type": "VHS_BatchManager",
                "link": null
              },
              { "name": "vae", "type": "VAE", "link": null }
            ],
            "outputs": [
              {
                "name": "Filenames",
                "type": "VHS_FILENAMES",
                "links": null,
                "shape": 3
              }
            ],
            "properties": { "Node name for S&R": "VHS_VideoCombine" },
            "widgets_values": {
              "frame_rate": 8,
              "loop_count": 0,
              "filename_prefix": "AnimateDiff",
              "format": "video/h264-mp4",
              "pix_fmt": "yuv420p",
              "crf": 22,
              "save_metadata": false,
              "pingpong": false,
              "save_output": false,
              "videopreview": {
                "hidden": false,
                "paused": false,
                "params": {
                  "filename": "AnimateDiff_00012.mp4",
                  "subfolder": "",
                  "type": "temp",
                  "format": "video/h264-mp4",
                  "frame_rate": 8
                },
                "muted": false
              }
            }
          }
        ],
        "links": [
          [7, 4, 0, 2, 0, "MODEL"],
          [8, 6, 0, 4, 1, "CONTEXT_OPTIONS"],
          [11, 9, 0, 8, 7, "INT"],
          [19, 15, 3, 2, 3, "LATENT"],
          [20, 15, 4, 2, 4, "VAE"],
          [21, 9, 0, 15, 2, "INT"],
          [22, 15, 0, 4, 0, "MODEL"],
          [23, 15, 5, 8, 0, "CLIP"],
          [24, 16, 0, 8, 1, "STRING"],
          [27, 29, 0, 2, 2, "CONDITIONING"],
          [28, 29, 0, 25, 1, "CONDITIONING"],
          [29, 15, 2, 29, 0, "*"],
          [30, 8, 0, 30, 0, "*"],
          [31, 30, 0, 25, 0, "CONDITIONING"],
          [32, 30, 0, 2, 1, "CONDITIONING"],
          [33, 25, 0, 28, 1, "CONDITIONING"],
          [34, 25, 1, 28, 2, "CONDITIONING"],
          [35, 4, 0, 28, 0, "MODEL"],
          [37, 2, 5, 25, 3, "IMAGE"],
          [38, 28, 0, 31, 0, "LATENT"],
          [39, 31, 0, 32, 0, "IMAGE"],
          [40, 2, 4, 31, 1, "VAE"],
          [41, 32, 0, 33, 0, "IMAGE"],
          [42, 33, 0, 7, 0, "IMAGE"],
          [46, 2, 3, 36, 0, "LATENT"],
          [47, 36, 0, 28, 3, "LATENT"],
          [48, 38, 0, 25, 2, "CONTROL_NET"]
        ],
        "groups": [],
        "config": {},
        "extra": {
          "ds": {
            "scale": 0.12284597357367237,
            "offset": [4127.293775475935, 821.5566641284396]
          }
        },
        "version": 0.4,
        "seed_widgets": { "2": 0, "28": 0 }
      }
    }
  }
}
"""
