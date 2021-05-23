# Phishpedia

- This is the official implementation of "Phishpedia: A Hybrid Deep Learning Based Approach to Visually Identify Phishing Webpages" USENIX'21 [[paper](https://www.usenix.org/conference/usenixsecurity21/presentation/lin)]
    
### Framework
    
<img src="big_pic/pic.png" style="width:2000px;height:350px"/>

```Input```: A URL and its screenshot ```Output```: Phish/Benign, Phishing target
- Step 1: Enter <b>Deep Object Detection Model</b>, get predicted elements

- Step 2: Enter <b>Deep Siamese Model</b>
    - If Siamese report no target, ```Return  Benign, None```
    - Else Siamese report a target, ```Return Phish, Phishing target``` 


### Instructions
1. Download all the model files:
- First 
```
cd src/phishpedia
```
``` 
wget https://drive.google.com/file/d/1H0Q_DbdKPLFcZee8I14K62qV7TTy7xvS/view?usp=sharing
```
``` 
wget https://drive.google.com/file/d/1_C8NSQYWkpW_-tW8WzFaBr8vDeBAWQ87/view?usp=sharing
```
``` 
wget https://drive.google.com/file/d/1qSdkSSoCYUkZMKs44Rup_1DPBxHnEKl1/view?usp=sharing
```

- Then 
```
cd src/detectron2_pedia/output/rcnn_2
```
```
wget https://drive.google.com/file/d/1tE2Mu5WC8uqCxei3XqAd7AWaP5JTmVWH/view?usp=sharing
```

- Afterwards 
```
cd src/siamese_retrain
```
```
wget https://drive.google.com/file/d/1cuGAGe-HubaQWU8Gwn0evKSOake6hCTZ/view?usp=sharing
```
```
wget https://drive.google.com/file/d/1GirhWiOVQpJWafhHA93elMfsUrxJzr9f/view?usp=sharing
```
```
wget https://drive.google.com/file/d/12GjdcYeSBbPji8pCq5KrFhWmqUC451Pc/view?usp=sharing
```
2. Download all data files
- Download phish30k, benign30k dataset:
```
cd datasets
wget https://drive.google.com/file/d/12ypEMPRQ43zGRqHGut0Esq2z5en0DH4g/view?usp=sharing
wget https://drive.google.com/file/d/1yORUeSrF5vGcgxYrsCoqXcpOUHt-iHq_/view?usp=sharing
```
- Download labelled benign30k dataset (optional, if you want to train Faster-RCNN yourself):
```
cd datasets
wget 
```
3. Run experiment 
- For phish discovery experiment:
```
python phishpedia_main.py --folder [data folder you want to test] --results [xxx.txt]
```
- For general experiment: 
please run evaluation scripts
```
python -m src.pipeline_eval --data-dir datasets/phish_sample_30k --mode phish --write-txt output_phish.txt --ts [threshold for siamese]
```
```
python -m src.pipeline_eval --data-dir datasets/benign_sample_30k --mode benign --write-txt output_benign.txt --ts [threshold for siamese]
```
- For adversarial attack on Siamese, download all files [[here]()] and put them under **datasets/**:


### Training the model (Optional)
1. If you want to train object detection faster-rcnn model yourself, 
- First dowonload training data
```
cd datasets
wget https://drive.google.com/file/d/1L3KSWEXcnWzYdJ4hPrNEUvC8jaaNOiBa/view?usp=sharing
unzip data.zip -d . 
```
- Then start training 
To train on a single gpu:
```
python -m src.detectron2_pedia.train_net \
       --config-file src/detectron2_pedia/configs/faster_rcnn.yaml
```

To train on multiple gpus:
```
python -m src.detectron2_pedia.train_net \
       --num-gpus 4 \
       --config-file src/detectron2_pedia/configs/faster_rcnn.yaml
```

To resume training from a checkpoint (finds last checkpoint from cfg.OUTPUT_DIR)
```
python -m src.detectron2_pedia.train_net \
       --num-gpus 4 \
       --config-file src/detectron2_pedia/configs/faster_rcnn.yaml \
       --resume
```
- Launch DAG adversarial attack on faster-rcnn:
```
python -m src.detectron2_pedia.run_DAG \
    --cfg-path src/detectron2_pedia/configs/faster_rcnn.yaml \
    --weights-path src/detectron2_pedia/output/rcnn_2/rcnn_bet365.pth \
    --results-save-path coco_instances_results.json \
    --vis-save-dir saved
```

2. If you want to train siamese
- I first pretrained on the Logos2k [[download here](https://drive.google.com/open?id=1PTA24UTZcsnzXPN1gmV0_lRg3lMHqwp6)] dataset, using a pretrained BiT-M ResNet50x1 model, which we have to download first:
```
wget https://storage.googleapis.com/bit_models/BiT-M-R50x1.npz
```
This command runs the pre-training on the downloaded model:
```
python -m src.siamese_retrain.bit_pytorch.train \
    --name {exp_name} \  # Name of this run. Used for monitoring and checkpointing.
    --model BiT-M-R50x1 \  # Which pretrained model to use.
    --logdir {log_dir} \  # Where to log training info.
    --dataset logo_2k \  # Name of custom dataset as specified and self-implemented above.
```
Saving and utilizing the weights in the previous step, I finetune the model on our logo targetlist dataset:
```
python -m src.siamese_retrain.bit_pytorch.train \
    --name {exp_name} \  # Name of this run. Used for monitoring and checkpointing.
    --model BiT-M-R50x1 \  # Which pretrained model to use.
    --logdir {log_dir} \  # Where to log training info.
    --dataset targetlist \  # Name of custom dataset as specified and self-implemented above.
    --weights_path {weights_path} \  # Path to weights saved in the previous step, i.e. bit.pth.tar.
```
- Launch adversarial attack on siamese:
Run src/adv_attack/gradient masking siamese.ipynb 

### Project structure
- src
    - siamese_retrain: training script for siamese
    - detectron2_peida: training script for object detector
    - phishpedia: inference script for siamese
    - util: other scripts (chromedriver utilities)
    - siamese.py: main script for siamese
    - pipeline_eval.py: evaluation script for general experiment
    - phishpedia_main.py: script for phish-discovery experiment 

        