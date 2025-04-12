# **Phish Eye: Enhanced Phishing Detection with Hybrid Deep Learning and Transformers**

Phish Eye builds upon the original Phishpedia framework by integrating a secondary URL classifier based on Transformer architectures. While the legacy system relied on visual logo detection and brand-domain consistency (using object detection and a Siamese network), Phish Eye overcomes the limitation of missing brand logos by employing a BERT-based URL analysis. This hybrid two-stage approach not only reinforces accuracy by analyzing both visual and textual patterns but also significantly reduces false negatives.

## Overview

**Two-Stage Architecture:**

1. **Stage 1: Legacy Phishpedia Pipeline (Logo-Based Detection)**
   - **Logo Detection:** Uses Faster R-CNN (via Detectron2) to extract candidate logos from webpage screenshots.
   - **Brand Matching:** Leverages a Siamese neural network with triplet loss to compare detected logos against a curated reference set. A mismatch between the detected brand and the URL’s domain flags the site as phishing.

2. **Stage 2: Transformer-Based URL Classification**
   - If no matching logo is found (or if the brand is not in the reference list), the raw URL is analyzed using a fine-tuned BERT model (imanoop7/bert-phishing-detector) to detect suspicious textual patterns.
   - This ensures that text-based phishing attempts—such as typosquatting or deceptive domain strings—are effectively flagged.

**Key Advantages:**
- **Expanded Brand Recognition:** Enhanced logo detection combined with textual URL analysis detects phishing even for brands not preloaded in the reference set.
- **Hybrid Defense:** The combination of visual and text-based analysis improves overall detection performance and drastically reduces false negatives.
- **Real-World Robustness:** Preliminary evaluations indicate a near-perfect detection rate on challenging datasets.

## Instructions

**Prerequisite:**  
Anaconda installed (see [Anaconda Installation](https://docs.anaconda.com/free/anaconda/install/index.html)).

### Running Inference from the Command Line

1. **Create a Local Clone and Set Up Environment:**
   ```bash
   git clone https://github.com/Atika6677/Phish_Eye.git
   cd Phish_Eye
   chmod +x ./setup.sh
   ./setup.sh
2. **Activate Environment**
    ```bash
    conda activate phisheye
3. **Run Inference**
   ```bash
   python Phish_Eye.py --folder <folder you want to test e.g. ./datasets/test_sites>
   
The testing folder should be structured as follows:
```bash
test_site_1
├── info.txt   (Contains the URL)
└── shot.png   (Screenshot of the webpage)

test_site_2
├── info.txt
└── shot.png
...
