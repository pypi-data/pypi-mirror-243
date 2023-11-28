import gradio as gr
from novita_client import *
import logging
import random
import traceback


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(filename)s(%(lineno)d) %(message)s')


first_stage_activication_words = "a ohwx"
second_stage_activication_words = "a closeup photo of ohwx"

first_stage_lora_scale_default = 0.3
second_stage_lora_scale_default = 1.0

suggestion_checkpoints = [
    "dreamshaper_8_93211.safetensors",
    "epicrealism_pureEvolutionV5_97793.safetensors",
    "v1-5-pruned-emaonly.safetensors"
]
base_checkpoints = ["epicrealism_naturalSin_121250", "v1-5-pruned-emaonly"]


get_local_storage = """
    function() {
      globalThis.setStorage = (key, value)=>{
        localStorage.setItem(key, JSON.stringify(value))
      }
       globalThis.getStorage = (key, value)=>{
        return JSON.parse(localStorage.getItem(key))
      }

       const novita_key =  getStorage('novita_key')
       return [novita_key];
      }
    """


def get_noviata_client(novita_key):
    client = NovitaClient(novita_key, os.getenv('NOVITA_API_URI', None))
    client.set_extra_headers({"User-Agent": "stylization-playground"})
    return client


def create_ui():
    with gr.Blocks() as demo:
        gr.HTML(''' 
        <a href="https://novita.ai/?utm_source=huggingface&utm_medium=face-stylization&utm_campaign=face-stylization">
            <img src="https://raw.githubusercontent.com/wiki/novitalabs/sd-webui-cleaner/images/logo2.png" width="120px;" alt="Unsplash" />
        </a>
        <h1>Face Stylization Playground</h1>
        <h3>Start integrate with <a href="https://novita.ai/get-started/Model_training.html?utm_source=huggingface&utm_medium=face-stylization&utm_campaign=face-stylization">Model_training API</a> 
        <h3> Get Novita.AI API Key from <a href="https://novita.ai/get-started/Account_account_and_key.html?utm_source=huggingface&utm_medium=face-stylization&utm_campaign=face-stylization">Novita.AI</a></h2>
        '''
                )

        free_trial_notice = gr.HTML('', visible=False)
        with gr.Row():
            with gr.Column(scale=1):
                novita_key = gr.Textbox(value="", label="Novita.AI API KEY (store in broweser)", placeholder="novita.ai api key", type="password")
            with gr.Column(scale=1):
                user_balance = gr.Textbox(label="User Balance", value="0.0")

        with gr.Tab(label="Subject Training"):
            with gr.Row():
                with gr.Column(scale=1):
                    training_subject_base_model = gr.Dropdown(choices=base_checkpoints, label="Base Model", value=base_checkpoints[0])
                    training_subject_geneder = gr.Radio(choices=["man", "woman", "person"], value="man", label="Geneder")
                    training_subject_name = gr.Text(label="Training Name", placeholder="training name", elem_id="training_name", value="my-face-001")
                    training_subject_max_train_steps = gr.Slider(minimum=200, maximum=4000, step=1, label="Max Train Steps", value=2000)
                    training_subject_images = gr.File(file_types=["image"], file_count="multiple", label="6-10 face images.")
                    training_subject_button = gr.Button(value="Train")
                    training_subject_payload = gr.JSON(label="Training Payload, POST /v3/training/subject")
                with gr.Column(scale=1):
                    training_subject_refresh_button = gr.Button(value="Refresh Training Status")
                    training_subject_refresh_json = gr.JSON()

                def on_upload_training_subject_images(files):
                    if files is None:
                        return 2000
                    return min(2000, len(files) * 200)

                training_subject_images.change(
                    inputs=[training_subject_images],
                    outputs=training_subject_max_train_steps,
                    fn=on_upload_training_subject_images,
                )

                def train_subject(novita_key, base_model, training_name, training_subject_geneder, max_train_steps, training_images):
                    training_images = [_.name for _ in training_images]
                    try:
                        get_noviata_client(novita_key).create_training_subject(
                            base_model=base_model,
                            name=training_name,
                            instance_prompt=f"a closeup photo of ohwx person",
                            class_prompt="person",
                            max_train_steps=max_train_steps,
                            images=training_images,
                            components=FACE_TRAINING_DEFAULT_COMPONENTS,
                            learning_rate=3e-4,
                            seed=None,
                            lr_scheduler='cosine_with_restarts',
                            with_prior_preservation=True,
                            prior_loss_weight=1.0,
                            lora_r=32,
                            lora_alpha=32,
                            lora_text_encoder_r=32,
                            lora_text_encoder_alpha=32,
                        )

                        payload = dict(
                            name=training_name,
                            base_model=base_model,
                            image_dataset_items=["....assets_ids, please manually upload to novita.ai"],
                            expert_setting=TrainingExpertSetting(
                                instance_prompt=f"a closeup photo of ohwx person",
                                class_prompt="person",
                                max_train_steps=max_train_steps,
                                learning_rate="3e-4",
                                seed=None,
                                lr_scheduler='cosine_with_restarts',
                                with_prior_preservation=True,
                                prior_loss_weight=1.0,
                                lora_r=32,
                                lora_alpha=32,
                                lora_text_encoder_r=32,
                                lora_text_encoder_alpha=32,
                            ),
                            components=[_.to_dict() for _ in FACE_TRAINING_DEFAULT_COMPONENTS],
                        )
                    except Exception as e:
                        logging.error(e)
                        raise gr.Error(traceback.format_exc())

                    return gr.update(value=get_noviata_client(novita_key).list_training("subject").sort_by_created_at()), payload

                training_subject_refresh_button.click(
                    inputs=[novita_key],
                    outputs=training_subject_refresh_json,
                    fn=lambda novita_key: gr.update(value=get_noviata_client(novita_key).list_training("subject").sort_by_created_at())
                )
                training_subject_button.click(
                    inputs=[novita_key, training_subject_base_model, training_subject_name, training_subject_geneder, training_subject_max_train_steps, training_subject_images],
                    outputs=[training_subject_refresh_json, training_subject_payload],
                    fn=train_subject
                )

        with gr.Tab(label="Style Training"):
            with gr.Row():
                with gr.Column(scale=1):
                    training_style_base_model = gr.Dropdown(choices=base_checkpoints, label="Base Model", value="v1-5-pruned-emaonly")
                    training_style_name = gr.Text(label="Training Name", placeholder="training name", elem_id="training_name", value="my-style-001")
                    training_style_max_train_steps = gr.Slider(minimum=200, maximum=10000, step=1, label="Max Train Steps", value=2000)
                    training_style_images_and_captions = gr.File(file_types=["image", ".txt", ".caption"], file_count="multiple", label="10-50 style images.")
                    training_style_button = gr.Button(value="Train")
                    training_style_payload = gr.JSON(label="Training Payload, POST /v3/training/style")
                with gr.Column(scale=1):
                    training_style_refresh_button = gr.Button(value="Refresh Training Status")
                    training_style_refresh_json = gr.JSON()

                def on_upload_training_style_images(files):
                    if files is None:
                        return 2000

                    caption_files = [f for f in files if f.name.endswith(".caption") or f.name.endswith(".txt")]
                    image_files = [f for f in files if not f.name.endswith(".caption") and not f.name.endswith(".txt")]

                    if len(caption_files) != len(image_files):
                        raise gr.Error("caption files and image files must be same length")

                    return min(2000, len(image_files) * 200)

                training_style_images_and_captions.change(
                    inputs=[training_style_images_and_captions],
                    outputs=training_style_max_train_steps,
                    fn=on_upload_training_style_images,
                )

                def train_style(novita_key, base_model, training_name, max_train_steps, training_style_images_and_captions):
                    files = [_.name for _ in training_style_images_and_captions]
                    images_captions = {}
                    for f in files:
                        basename = os.path.basename(f).rsplit(".", 1)[0]
                        if basename not in images_captions:
                            images_captions[basename] = {}
                        if f.endswith(".caption") or f.endswith(".txt"):
                            images_captions[basename]["caption"] = f
                        else:
                            images_captions[basename]["image"] = f

                    for k, v in images_captions.items():
                        if len(v) != 2:
                            raise gr.Error(f"image and caption must be provided for {k}")

                    images = []
                    captions = []

                    for _, v in images_captions.items():
                        if "image" in v:
                            images.append(v["image"])
                        if "caption" in v:
                            with open(v["caption"], "r") as f:
                                captions.append(f.read().strip())

                    get_noviata_client(novita_key).create_training_style(
                        name=training_name,
                        base_model=base_model,
                        max_train_steps=max_train_steps,
                        images=images,
                        captions=captions,
                        learning_rate=1e-4,
                    )
                    payload = dict(
                        name=training_name,
                        base_model=base_model,
                        image_dataset_items=["....assets_ids, please manually upload to novita.ai"],
                        expert_setting=TrainingExpertSetting(
                            learning_rate=1e-4,
                        ),
                    )
                    return gr.update(value=get_noviata_client(novita_key).list_training("style").sort_by_created_at()), payload

                training_style_button.click(
                    inputs=[novita_key, training_style_base_model, training_style_name, training_style_max_train_steps, training_style_images_and_captions],
                    outputs=[training_style_refresh_json, training_style_payload],
                    fn=train_style
                )
                training_style_refresh_button.click(
                    inputs=[novita_key],
                    outputs=training_style_refresh_json,
                    fn=lambda novita_key: gr.update(value=get_noviata_client(novita_key).list_training("style").sort_by_created_at())
                )

        with gr.Tab(label="Subject Inferencing"):
            with gr.Row():
                with gr.Column(scale=1):
                    style_prompt = gr.TextArea(lines=3, label="Style Prompt")
                    style_negative_prompt = gr.TextArea(lines=3, label="Style Negative Prompt")
                    style_gender = gr.Radio(choices=["man", "woman", "person"], value="man", label="Gender")
                    style_model = gr.Dropdown(choices=suggestion_checkpoints, label="Style Model")
                    style_lora = gr.Dropdown(choices=[], label="Style LoRA", type="index")
                    _hide_lora_training_response = gr.JSON(visible=False)
                    style_height = gr.Slider(minimum=1, maximum=1024, step=1, label="Style Height", value=512)
                    style_width = gr.Slider(minimum=1, maximum=1024, step=1, label="Style Width", value=512)
                    style_method = gr.Radio(choices=["txt2img", "controlnet-depth", "controlnet-pose", "controlnet-canny",
                                            "controlnet-lineart", "controlnet-scribble", "controlnet-tile"], label="Style Method")

                    style_advanced = gr.Checkbox(label="Advanced")
                    with gr.Column(scale=1, visible=False) as style_advanced_tab:
                        first_stage_seed = gr.Slider(minimum=-1, maximum=1000000, step=1, label="First Stage Seed", value=-1)
                        second_stage_seed = gr.Slider(minimum=-1, maximum=1000000, step=1, label="Second Stage Seed", value=-1)
                        first_stage_lora_scale = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label="First Stage LoRA Scale", value=0.3)
                        second_stage_lora_scale = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label="Second Stage LoRA Scale", value=1.0)
                        second_stage_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label="Second Stage Strength", value=0.3)
                        second_stage_steps = gr.Slider(minimum=1, maximum=100, step=1, label="Second Stage Steps", value=20)
                        controlnet_weight = gr.Slider(minimum=0.0, maximum=2.0, step=0.01, label="Controlnet Weight", value=1.0)

                    style_advanced.change(inputs=[style_advanced], outputs=[style_advanced_tab], fn=lambda v: gr.update(visible=v))

                    style_reference_image = gr.Image(label="Style Reference Image", height=512)

                with gr.Column(scale=1):
                    inference_refresh_button = gr.Button(value="Refresh Style LoRA")
                    generate_button = gr.Button(value="Generate")
                    num_images = gr.Slider(minimum=1, maximum=10, step=1, label="Num Images", value=1)
                    gallery = gr.Gallery(label="Gallery", height="auto", object_fit="scale-down", show_share_button=False)

                    def inference_refresh_button_fn(novita_key):
                        # trained_loras_models = [_.name for _ in get_noviata_client(novita_key).models_v3(refresh=True).filter_by_type("lora").filter_by_visibility("private")]
                        serving_models = [_.models[0].model_name for _ in get_noviata_client(novita_key).list_training("subject").filter_by_model_status("SERVING")]
                        serving_models_labels = [_.task_name for _ in get_noviata_client(novita_key).list_training("subject").filter_by_model_status("SERVING")]
                        default_serving_model = serving_models_labels[0] if len(serving_models_labels) > 0 else None
                        return gr.update(choices=serving_models_labels, value=default_serving_model), gr.update(value=serving_models)

                    inference_refresh_button.click(
                        inputs=[novita_key],
                        outputs=[style_lora, _hide_lora_training_response],
                        fn=inference_refresh_button_fn
                    )

                    first_stage_request_body = gr.JSON(label="First Stage Request Body, POST /api/v2/txt2img")

            templates = [
                {
                    "style_prompt": "(masterpiece), (extremely intricate:1.3), (realistic), portrait of a person, the most handsome in the world, (medieval armor), metal reflections, upper body, outdoors, intense sunlight, far away castle, professional photograph of a stunning person detailed, sharp focus, dramatic, award winning, cinematic lighting, octane render unreal engine, volumetrics dtx, (film grain, blurry background, blurry foreground, bokeh, depth of field, sunset, motion blur:1.3), chainmail",
                    "style_negative_prompt": "BadDream_53202, UnrealisticDream_53204",
                    "style_gender": "man",
                    "style_model": "dreamshaper_8_93211.safetensors",
                    "style_method": "txt2img",
                    "style_height": 768,
                    "style_width": 512,
                    "style_reference_image": "./00001.jpg",
                },
                {
                    "style_prompt": "photo of beautiful age 18 girl, pastel hair, freckles sexy, beautiful, close up, young, dslr, 8k, 4k, ultrarealistic, realistic, natural skin, textured skin",
                    "style_negative_prompt": "BadDream_53202, UnrealisticDream_53204",
                    "style_gender": "woman",
                    "style_model": "dreamshaper_8_93211.safetensors",
                    "style_method": "controlnet-depth",
                    "style_height": 768,
                    "style_width": 512,
                    "style_reference_image": "./00002.jpg",
                },
                {
                    "style_prompt": "majesty, holy, saintly, godly, 1girl, an angel descending from heaven, upper body, beautiful asian goddess, looking at viewer, detail face and eyes, symmetrical eyes, glowing white eye, warm attitude, long hair, blonde hair, floating hair, royal clothes, gold armor, feathered wings, glowing wings, nice hands",
                    "style_negative_prompt": "BadDream_53202, UnrealisticDream_53204",
                    "style_gender": "woman",
                    "style_model": "dreamshaper_8_93211.safetensors",
                    "style_method": "controlnet-canny",
                    "style_height": 768,
                    "style_width": 512,
                    "style_reference_image": "./00003.jpg",
                },
                {
                    "style_prompt": "Iron Man, close up, digital art, character concept, magical realism, warm golden light, sunset, Marvel Cinematic Universe, Hogwarts, high-resolution, vibrant colors, realistic rendering, key art, fantasy fashion, Iron Man suit integration, elegant and powerful pose",
                    "style_negative_prompt": "BadDream_53202, UnrealisticDream_53204",
                    "style_gender": "man",
                    "style_model": "dreamshaper_8_93211.safetensors",
                    "style_method": "controlnet-depth",
                    "style_height": 768,
                    "style_width": 512,
                    "style_reference_image": "./00004.jpg",
                }
            ]

            def mirror(*args):
                return args

            with gr.Row():
                examples = gr.Examples(
                    [
                        [
                            _.get("style_prompt", ""),
                            _.get("style_negative_prompt", ""),
                            _.get("style_gender", "man"),
                            _.get("style_model", ""),
                            _.get("style_height", 512),
                            _.get("style_width", 512),
                            _.get("style_method", "txt2img"),
                            _.get("style_reference_image", ""),
                        ] for _ in templates
                    ],
                    [
                        style_prompt,
                        style_negative_prompt,
                        style_gender,
                        style_model,
                        style_height,
                        style_width,
                        style_method,
                        style_reference_image,
                    ],
                    [
                        style_prompt,
                        style_negative_prompt,
                        style_gender,
                        style_model,
                        style_height,
                        style_width,
                        style_method,
                        style_reference_image,
                    ],
                    mirror,
                    cache_examples=False,
                )

            def generate(novita_key,
                         style_gender,
                         style_prompt,
                         style_negative_prompt,
                         style_model,
                         style_lora,
                         _hide_lora_training_response,
                         style_hegiht,
                         style_width,
                         style_method,
                         style_reference_image,
                         first_stage_seed,
                         second_stage_seed,
                         first_stage_lora_scale,
                         second_stage_lora_scale,
                         second_stage_strength,
                         second_stage_steps,
                         controlnet_weight,
                         num_images):

                style_reference_image = Image.fromarray(style_reference_image)

                def style(style_method,
                          style_gender,
                          style_prompt,
                          style_negative_prompt,
                          style_model,
                          style_lora,
                          _hide_lora_training_response,
                          style_hegiht,
                          style_width,
                          style_reference_image,
                          first_stage_seed,
                          second_stage_seed,
                          first_stage_lora_scale,
                          second_stage_lora_scale,
                          second_stage_strength,
                          second_stage_steps,
                          controlnet_weight,
                          num_images
                          ):
                    if isinstance(style_lora, int):
                        style_lora = _hide_lora_training_response[style_lora].replace(".safetensors", "")
                    else:
                        style_lora = style_lora.replace(".safetensors", "")

                    height = int(style_hegiht)
                    width = int(style_width)

                    if first_stage_seed == -1:
                        first_stage_seed = random.randint(1, 2 ** 32 - 1)
                    if second_stage_seed == -1:
                        second_stage_seed = random.randint(1, 2 ** 32 - 1)

                    activication_words = f"{first_stage_activication_words} {style_gender}"

                    style_prompt = f"{activication_words}, <lora:{style_lora}:{first_stage_lora_scale}>, {style_prompt}"

                    if style_method == "txt2img":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                        )
                    elif style_method == "controlnet-depth":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                            controlnet_units=[
                                ControlnetUnit(
                                    input_image=image_to_base64(style_reference_image),
                                    control_mode=ControlNetMode.BALANCED,
                                    model="control_v11f1p_sd15_depth",
                                    module=ControlNetPreprocessor.DEPTH,
                                    resize_mode=ControlNetResizeMode.RESIZE_OR_CORP,
                                    weight=controlnet_weight,
                                )
                            ]
                        )
                    elif style_method == "controlnet-pose":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                            controlnet_units=[
                                ControlnetUnit(
                                    input_image=image_to_base64(style_reference_image),
                                    control_mode=ControlNetMode.BALANCED,
                                    model="control_v11p_sd15_openpose",
                                    module=ControlNetPreprocessor.OPENPOSE,
                                    resize_mode=ControlNetResizeMode.RESIZE_OR_CORP,
                                    weight=controlnet_weight,
                                )
                            ]
                        )
                    elif style_method == "controlnet-canny":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                            controlnet_units=[
                                ControlnetUnit(
                                    input_image=image_to_base64(style_reference_image),
                                    control_mode=ControlNetMode.BALANCED,
                                    model="control_v11p_sd15_canny",
                                    module=ControlNetPreprocessor.CANNY,
                                    resize_mode=ControlNetResizeMode.RESIZE_OR_CORP,
                                    weight=controlnet_weight,
                                )
                            ]
                        )
                    elif style_method == "controlnet-lineart":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                            controlnet_units=[
                                ControlnetUnit(
                                    input_image=image_to_base64(style_reference_image),
                                    control_mode=ControlNetMode.BALANCED,
                                    model="control_v11p_sd15_lineart",
                                    module=ControlNetPreprocessor.LINEART,
                                    resize_mode=ControlNetResizeMode.RESIZE_OR_CORP,
                                    weight=controlnet_weight,
                                )
                            ]
                        )
                    elif style_method == "controlnet-scribble":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                            controlnet_units=[
                                ControlnetUnit(
                                    input_image=image_to_base64(style_reference_image),
                                    control_mode=ControlNetMode.BALANCED,
                                    model="control_v11p_sd15_scribble",
                                    module=ControlNetPreprocessor.SCRIBBLE_HED,
                                    resize_mode=ControlNetResizeMode.RESIZE_OR_CORP,
                                    weight=controlnet_weight,
                                )
                            ]
                        )
                    elif style_method == "controlnet-tile":
                        req = Txt2ImgRequest(
                            prompt=style_prompt,
                            negative_prompt=style_negative_prompt,
                            width=width,
                            height=height,
                            model_name=style_model,
                            steps=30,
                            sampler_name=Samplers.DPMPP_M_KARRAS,
                            seed=first_stage_seed,
                            controlnet_units=[
                                ControlnetUnit(
                                    input_image=image_to_base64(style_reference_image),
                                    control_mode=ControlNetMode.BALANCED,
                                    model="control_v11f1e_sd15_tile",
                                    module=ControlNetPreprocessor.NULL,
                                    resize_mode=ControlNetResizeMode.RESIZE_OR_CORP,
                                    weight=controlnet_weight,
                                )
                            ],
                        )

                    ad_req = ADEtailer(
                        prompt=f"{second_stage_activication_words} {style_gender}, masterpiece, <lora:{style_lora}:{second_stage_lora_scale}>",
                        negative_prompt=style_negative_prompt,
                        strength=second_stage_strength,
                        seed=second_stage_seed,
                        steps=second_stage_steps,
                    )
                    req.batch_size = num_images
                    req.adetailer = ad_req

                    res = get_noviata_client(novita_key).sync_txt2img(req)
                    style_images = [Image.open(BytesIO(b)) for b in res.data.imgs_bytes]

                    return style_images, req.to_dict()
                images = []
                try:
                    final_images, first_stage_request_body = style(
                        style_method,
                        style_gender,
                        style_prompt,
                        style_negative_prompt,
                        style_model,
                        style_lora,
                        _hide_lora_training_response,
                        style_hegiht,
                        style_width,
                        style_reference_image,
                        first_stage_seed,
                        second_stage_seed,
                        first_stage_lora_scale,
                        second_stage_lora_scale,
                        second_stage_strength,
                        second_stage_steps,
                        controlnet_weight,
                        num_images
                    )
                    images.extend(final_images)
                except:
                    raise gr.Error(traceback.format_exc())

                return gr.update(value=images), first_stage_request_body

            generate_button.click(
                inputs=[novita_key,
                        style_gender,
                        style_prompt,
                        style_negative_prompt,
                        style_model,
                        style_lora,
                        _hide_lora_training_response,
                        style_height,
                        style_width,
                        style_method,
                        style_reference_image,
                        first_stage_seed,
                        second_stage_seed,
                        first_stage_lora_scale,
                        second_stage_lora_scale,
                        second_stage_strength,
                        second_stage_steps,
                        controlnet_weight,
                        num_images],
                outputs=[gallery, first_stage_request_body],
                fn=generate
            )

        with gr.Tab(label="Style Inferencing"):
            with gr.Row():
                with gr.Column(scale=1):
                    inference_style_prompt = gr.TextArea(lines=3, label="Style Prompt")
                    inference_style_negative_prompt = gr.TextArea(lines=3, label="Style Negative Prompt")
                    inference_style_model = gr.Dropdown(choices=suggestion_checkpoints, label="Style Model")
                    _inference_style_hide_lora_training_response = gr.JSON(visible=False)
                    inference_style_lora = gr.Dropdown(choices=[], label="Style LoRA", type="index")
                    inference_style_height = gr.Slider(minimum=1, maximum=1024, step=1, label="Style Height", value=512)
                    inference_style_width = gr.Slider(minimum=1, maximum=1024, step=1, label="Style Width", value=512)

                    inference_style_first_stage_seed = gr.Slider(minimum=-1, maximum=1000000, step=1, label="First Stage Seed", value=-1)
                    inference_style_first_stage_lora_scale = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label="First Stage LoRA Scale", value=1.0)

                with gr.Column(scale=1):
                    inference_style_refresh_button = gr.Button(value="Refresh Style LoRA")
                    inference_style_generate_button = gr.Button(value="Generate")
                    inference_style_num_images = gr.Slider(minimum=1, maximum=10, step=1, label="Num Images", value=1)
                    inference_style_gallery = gr.Gallery(label="Gallery", height="auto", object_fit="scale-down", show_share_button=False)

                    def inference_style_refresh_button_fn(novita_key):
                        # trained_loras_models = [_.name for _ in get_noviata_client(novita_key).models_v3(refresh=True).filter_by_type("lora").filter_by_visibility("private")]
                        serving_models = [_.models[0].model_name for _ in get_noviata_client(novita_key).list_training("subject").filter_by_model_status("SERVING")]
                        serving_models_labels = [_.task_name for _ in get_noviata_client(novita_key).list_training("subject").filter_by_model_status("SERVING")]
                        default_serving_model = serving_models_labels[0] if len(serving_models_labels) > 0 else None
                        return gr.update(choices=serving_models_labels, value=default_serving_model), gr.update(value=serving_models)

                    inference_style_refresh_button.click(
                        inputs=[novita_key],
                        outputs=[inference_style_lora, _inference_style_hide_lora_training_response],
                        fn=inference_style_refresh_button_fn
                    )

                    inference_style_first_stage_request_body = gr.JSON(label="First Stage Request Body, POST /api/v2/txt2img")

            def inference_style_generate(novita_key,
                                         style_prompt,
                                         style_negative_prompt,
                                         style_model,
                                         style_lora,
                                         _hide_lora_training_response,
                                         style_hegiht,
                                         style_width,
                                         first_stage_seed,
                                         first_stage_lora_scale,
                                         num_images):

                def style(
                    style_prompt,
                    style_negative_prompt,
                    style_model,
                    style_lora,
                    _hide_lora_training_response,
                    style_hegiht,
                    style_width,
                    first_stage_seed,
                    first_stage_lora_scale,
                    num_images
                ):
                    if isinstance(style_lora, int):
                        style_lora = _hide_lora_training_response[style_lora].replace(".safetensors", "")
                    else:
                        style_lora = style_lora.replace(".safetensors", "")

                    height = int(style_hegiht)
                    width = int(style_width)

                    if first_stage_seed == -1:
                        first_stage_seed = random.randint(1, 2 ** 32 - 1)

                    style_prompt = f"{style_prompt}, <lora:{style_lora}:{first_stage_lora_scale}>"
                    req = Txt2ImgRequest(
                        prompt=style_prompt,
                        negative_prompt=style_negative_prompt,
                        width=width,
                        height=height,
                        model_name=style_model,
                        steps=30,
                        sampler_name=Samplers.DPMPP_M_KARRAS,
                        seed=first_stage_seed,
                        batch_size=num_images
                    )

                    res = get_noviata_client(novita_key).sync_txt2img(req)
                    style_images = [Image.open(BytesIO(b)) for b in res.data.imgs_bytes]
                    return style_images, req.to_dict()

                images = []
                try:
                    final_images, first_stage_request_body = style(
                        style_prompt,
                        style_negative_prompt,
                        style_model,
                        style_lora,
                        _hide_lora_training_response,
                        style_hegiht,
                        style_width,
                        first_stage_seed,
                        first_stage_lora_scale,
                        num_images
                    )
                    images.extend(final_images)
                except:
                    raise gr.Error(traceback.format_exc())

                return gr.update(value=images), first_stage_request_body

            inference_style_generate_button.click(
                inputs=[novita_key,
                        inference_style_prompt,
                        inference_style_negative_prompt,
                        inference_style_model,
                        inference_style_lora,
                        _inference_style_hide_lora_training_response,
                        inference_style_height,
                        inference_style_width,
                        inference_style_first_stage_seed,
                        inference_style_first_stage_lora_scale,
                        inference_style_num_images],
                outputs=[inference_style_gallery, inference_style_first_stage_request_body],
                fn=inference_style_generate
            )

        def onload(novita_key):
            if novita_key is None or novita_key == "":
                return novita_key, gr.update(choices=[], value=None), gr.update(value=None), f"$ UNKNOWN", gr.update(visible=False)
            try:
                user_info_json = get_noviata_client(novita_key).user_info()
                serving_models = [_.models[0].model_name for _ in get_noviata_client(novita_key).list_training().filter_by_model_status("SERVING")]
                serving_models_labels = [_.task_name for _ in get_noviata_client(novita_key).list_training().filter_by_model_status("SERVING")]
            except Exception as e:
                logging.error(e)
                return novita_key, gr.update(choices=[], value=None), gr.update(value=None), f"$ UNKNOWN", gr.update(visible=False)
            default_serving_model = serving_models_labels[0] if len(serving_models_labels) > 0 else None
            free_trial = user_info_json.free_trial.get('training', 0)
            trial_html = f'''<h2 style="color: red"> 🌟 Free trial quota: {free_trial} </h2>'''

            return novita_key, gr.update(choices=serving_models_labels, value=default_serving_model), gr.update(value=serving_models), f"$ {user_info_json.credit_balance / 100 / 100:.2f}", gr.update(value=trial_html, visible=free_trial > 0)

        novita_key.change(onload, inputs=novita_key, outputs=[novita_key, style_lora, _hide_lora_training_response,
                          user_balance, free_trial_notice], _js="(v)=>{ setStorage('novita_key',v); return [v]; }")

        demo.load(
            inputs=[novita_key],
            outputs=[novita_key, style_lora, _hide_lora_training_response, user_balance, free_trial_notice],
            fn=onload,
            _js=get_local_storage,
        )

    return demo


if __name__ == '__main__':
    demo = create_ui()
    demo.queue(api_open=False, concurrency_count=20)
    demo.launch()
