import os, argparse
import sys
import gradio as gr
from scripts.gradio.i2v_test_application import Image2Video
sys.path.insert(1, os.path.join(sys.path[0], 'lvdm'))


i2v_examples_interp_512 = [
    ['prompts/512_interp/smile_01.png', 'a smiling girl', 50, 7.5, 1.0, 5, 12306, 'prompts/512_interp/smile_02.png'],
    ['prompts/512_interp/stone01_01.png', 'rotating view', 50, 7.5, 1.0, 5, 123, 'prompts/512_interp/stone01_02.png'],
    ['prompts/512_interp/walk_01.png', 'man walking', 50, 7.5, 1.0, 5, 345, 'prompts/512_interp/walk_02.png'],
]
i2v_examples_loop_512 = [
    ['prompts/512_loop/24.png', 'a beach with waves and clouds at sunset', 50, 7.5, 1.0, 5, 234],
    ['prompts/512_loop/36.png', 'clothes swaying in the wind', 50, 7.5, 1.0, 5, 123],
    ['prompts/512_loop/40.png', 'flowers swaying in the wind', 50, 7.5, 1.0, 5, 234],
]



def dynamicrafter_demo(result_dir='./tmp/', res=512):
    if res == 1024:
        resolution = '576_1024'
        css = """#input_img {max-width: 1024px !important} #output_vid {max-width: 1024px; max-height:576px}"""
    elif res == 512:
        resolution = '320_512'
        css = """#input_img {max-width: 512px !important} #output_vid {max-width: 512px; max-height: 320px} #input_img2 {max-width: 512px !important} #output_vid {max-width: 512px; max-height: 320px}"""
    elif res == 256:
        resolution = '256_256'
        css = """#input_img {max-width: 256px !important} #output_vid {max-width: 256px; max-height: 256px}"""
    else:
        raise NotImplementedError(f"Unsupported resolution: {res}")
    image2video = Image2Video(result_dir, resolution=resolution)
    with gr.Blocks(analytics_enabled=False, css=css) as dynamicrafter_iface:
        gr.Markdown("<div align='center'> <h1> DynamiCrafter: Animating Open-domain Images with Video Diffusion Priors </span> </h1> \
                      <h2 style='font-weight: 450; font-size: 1rem; margin: 0rem'>\
                        <a href='https://doubiiu.github.io/'>Jinbo Xing</a>, \
                        <a href='https://menghanxia.github.io/'>Menghan Xia</a>, <a href='https://yzhang2016.github.io/'>Yong Zhang</a>, \
                        <a href=''>Haoxin Chen</a>, <a href=''> Wangbo Yu</a>,\
                        <a href='https://github.com/hyliu'>Hanyuan Liu</a>, <a href='https://xinntao.github.io/'>Xintao Wang</a>,\
                        <a href='https://www.cse.cuhk.edu.hk/~ttwong/myself.html'>Tien-Tsin Wong</a>,\
                        <a href='https://scholar.google.com/citations?user=4oXBp9UAAAAJ&hl=zh-CN'>Ying Shan</a>\
                    </h2> \
                     <a style='font-size:18px;color: #000000' href='https://arxiv.org/abs/2310.12190'> [ArXiv] </a>\
                     <a style='font-size:18px;color: #000000' href='https://doubiiu.github.io/projects/DynamiCrafter/'> [Project Page] </a> \
                     <a style='font-size:18px;color: #000000' href='https://github.com/Doubiiu/DynamiCrafter'> [Github] </a> </div>")
        
        #######generative frame interpolation and looping video generation######
        with gr.Tab(label='Generative Frame Interpolation_320x512'):
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            i2v_input_image = gr.Image(label="Input Image1",elem_id="input_img")
                        with gr.Row():
                            i2v_input_text = gr.Text(label='Prompts')
                        with gr.Row():
                            i2v_seed = gr.Slider(label='Random Seed', minimum=0, maximum=50000, step=1, value=123)
                            i2v_eta = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, label='ETA', value=1.0, elem_id="i2v_eta")
                            i2v_cfg_scale = gr.Slider(minimum=1.0, maximum=15.0, step=0.5, label='CFG Scale', value=7.5, elem_id="i2v_cfg_scale")
                        with gr.Row():
                            i2v_steps = gr.Slider(minimum=1, maximum=60, step=1, elem_id="i2v_steps", label="Sampling steps", value=50)
                            i2v_motion = gr.Slider(minimum=5, maximum=30, step=1, elem_id="i2v_motion", label="FPS", value=10)
                        i2v_end_btn = gr.Button("Generate")
                    with gr.Column():
                        with gr.Row():
                            i2v_input_image2 = gr.Image(label="Input Image2",elem_id="input_img2")
                        with gr.Row():
                            i2v_output_video = gr.Video(label="Generated Video",elem_id="output_vid",autoplay=True,show_share_button=True)

                gr.Examples(examples=i2v_examples_interp_512,
                            inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed, i2v_input_image2],
                            outputs=[i2v_output_video],
                            fn = image2video.get_image,
                            cache_examples=False,
                )
            i2v_end_btn.click(inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed, i2v_input_image2],
                            outputs=[i2v_output_video],
                            fn = image2video.get_image
            )
        #######generative frame interpolation and looping video generation######
        with gr.Tab(label='Looping Video Generation_320x512'):
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            i2v_input_image = gr.Image(label="Input Image",elem_id="input_img")
                        with gr.Row():
                            i2v_input_text = gr.Text(label='Prompts')
                        with gr.Row():
                            i2v_seed = gr.Slider(label='Random Seed', minimum=0, maximum=50000, step=1, value=123)
                            i2v_eta = gr.Slider(minimum=0.0, maximum=1.0, step=0.1, label='ETA', value=1.0, elem_id="i2v_eta")
                            i2v_cfg_scale = gr.Slider(minimum=1.0, maximum=15.0, step=0.5, label='CFG Scale', value=7.5, elem_id="i2v_cfg_scale")
                        with gr.Row():
                            i2v_steps = gr.Slider(minimum=1, maximum=60, step=1, elem_id="i2v_steps", label="Sampling steps", value=50)
                            i2v_motion = gr.Slider(minimum=5, maximum=30, step=1, elem_id="i2v_motion", label="FPS", value=5)
                        i2v_end_btn = gr.Button("Generate")
                    # with gr.Tab(label='Result'):
                    with gr.Row():
                        i2v_output_video = gr.Video(label="Generated Video",elem_id="output_vid",autoplay=True,show_share_button=True)

                gr.Examples(examples=i2v_examples_loop_512,
                            inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed],
                            outputs=[i2v_output_video],
                            fn = image2video.get_image,
                            cache_examples=False,
                )
            i2v_end_btn.click(inputs=[i2v_input_image, i2v_input_text, i2v_steps, i2v_cfg_scale, i2v_eta, i2v_motion, i2v_seed],
                            outputs=[i2v_output_video],
                            fn = image2video.get_image
            )

    return dynamicrafter_iface

def get_parser():
    parser = argparse.ArgumentParser()
    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    result_dir = os.path.join('./', 'results')
    dynamicrafter_iface = dynamicrafter_demo(result_dir)
    dynamicrafter_iface.queue(max_size=12)
    dynamicrafter_iface.launch(max_threads=1, share=True)
    # dynamicrafter_iface.launch(server_name='0.0.0.0', server_port=80, max_threads=1)