import os
# os.system("conda activate wavlip")
os.system(f'conda activate wavlip && python inference.py --checkpoint_path .\models\wav2lip_gan.pth --face shravya.png --audio ./audio/response.wav --outfile ./video/result_voice.mp4 && conda deactivate')
# os.system("")