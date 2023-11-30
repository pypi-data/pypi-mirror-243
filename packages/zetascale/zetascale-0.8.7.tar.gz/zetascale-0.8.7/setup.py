# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeta',
 'zeta.models',
 'zeta.nn',
 'zeta.nn.attention',
 'zeta.nn.biases',
 'zeta.nn.embeddings',
 'zeta.nn.modules',
 'zeta.nn.modules.xmoe',
 'zeta.ops',
 'zeta.optim',
 'zeta.quant',
 'zeta.rl',
 'zeta.structs',
 'zeta.tokenizers',
 'zeta.training',
 'zeta.utils']

package_data = \
{'': ['*']}

install_requires = \
['accelerate',
 'beartype',
 'bitsandbytes',
 'colt5-attention==0.10.18',
 'datasets',
 'einops',
 'einops-exts',
 'fairscale',
 'lion-pytorch',
 'pytest',
 'rich',
 'scipy',
 'sentencepiece',
 'tiktoken',
 'timm',
 'tokenmonster',
 'torch',
 'torchdiffeq',
 'torchvision',
 'tqdm',
 'transformers',
 'typing',
 'vector-quantize-pytorch==1.11.7']

setup_kwargs = {
    'name': 'zetascale',
    'version': '0.8.7',
    'description': 'Transformers at zeta scales',
    'long_description': '[![Multi-Modality](images/agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n![Zeta banner](images/zeta.png)\nBuild High-performance, agile, and scalable AI models with modular and re-useable building blocks!\n\n\n[![Docs](https://readthedocs.org/projects/zeta/badge/)](https://zeta.readthedocs.io)\n\n<p>\n  <a href="https://github.com/kyegomez/zeta/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>\n  <a href="https://pypi.org/project/zetascale"><img alt="MIT License" src="https://badge.fury.io/py/zetascale.svg" /></a>\n</p>\n\n# Design Principles\n- Fluid Experimentation: Zeta aims to be effortless for researchers and industrial AI engineers to rapidly experiment with the latest modules and components like `MultiGroupedQueryAttention` or `Unet` and many others!\n- Production-Grade Reliability: Facilitate reproducibility with bleeding-edge performance.\n- Modularity: Modularized Lego Building Blocks for building and deploying the best ML Models!\n\n\n# 🤝 Schedule a 1-on-1 Session\nBook a [1-on-1 Session with Kye](https://calendly.com/apacai/agora), the Creator, to discuss any issues, provide feedback, or explore how we can improve Zeta for you.\n\n\n## Installation\n\n`pip install zetascale`\n\n## Initiating Your Journey\n\nCreating a model empowered with the aforementioned breakthrough research features is a breeze. Here\'s how to quickly materialize the renowned Flash Attention\n\n```python\nimport torch\nfrom zeta.nn.attention import FlashAttention\n\nq = torch.randn(2, 4, 6, 8)\nk = torch.randn(2, 4, 10, 8)\nv = torch.randn(2, 4, 10, 8)\n\nattention = FlashAttention(causal=False, dropout=0.1, flash=True)\noutput = attention(q, k, v)\n\nprint(output.shape) \n\n```\n\n### ```RelativePositionBias```\n- ```RelativePositionBias``` quantizes the distance between two positions into a certain number of buckets and then uses an embedding to get the relative position bias. This mechanism aids in the attention mechanism by providing biases based on relative positions between the query and key, rather than relying solely on their absolute positions.\n```python\nfrom zeta.nn import RelativePositionBias\nimport torch\n\n# Initialize the RelativePositionBias module\nrel_pos_bias = RelativePositionBias()\n\n# Example 1: Compute bias for a single batch\nbias_matrix = rel_pos_bias(1, 10, 10)\n\n# Example 2: Utilize in conjunction with an attention mechanism\n# NOTE: This is a mock example, and may not represent an actual attention mechanism\'s complete implementation.\nclass MockAttention(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.rel_pos_bias = RelativePositionBias()\n\n    def forward(self, queries, keys):\n        bias = self.rel_pos_bias(queries.size(0), queries.size(1), keys.size(1))\n        # Further computations with bias in the attention mechanism...\n        return None  # Placeholder\n\n# Example 3: Modify default configurations\ncustom_rel_pos_bias = RelativePositionBias(bidirectional=False, num_buckets=64, max_distance=256, n_heads=8)\n\n```\n\n### `FeedForward`\nThe FeedForward module performs a feedforward operation on the input tensor x. It consists of a multi-layer perceptron (MLP) with an optional activation function and LayerNorm. \n\n```python\nfrom zeta.nn import FeedForward\n\nmodel = FeedForward(\n  256, \n  512, \n  glu=True, \n  post_act_ln=True, \n  dropout=0.2\n)\n\nx = torch.randn(1, 256)\n\noutput = model(x)\nprint(output.shape)\n```\n\n### `BitLinear`\n- The BitLinear module performs linear transformation on the input data, followed by quantization and dequantization. The quantization process is performed using the absmax_quantize function, which quantizes the input tensor based on the absolute maximum value, [from the paper](https://arxiv.org/abs/2310.11453)\n```python\nimport torch\nfrom torch import nn\nimport zeta.quant as qt\n\nclass MyModel(nn.Module):\n    def __init__(self):\n        super(MyModel, self).__init__()\n        self.linear = qt.BitLinear(10, 20)\n\n    def forward(self, x):\n        return self.linear(x)\n\n# Initialize the model\nmodel = MyModel()\n\n# Create a random tensor of size (128, 10)\ninput = torch.randn(128, 10)\n\n# Perform the forward pass\noutput = model(input)\n\n# Print the size of the output\nprint(output.size())  # torch.Size([128, 20])\n\n```\n\n### `PalmE`\n- This is an implementation of the multi-modal Palm-E model using a decoder llm as the backbone with an VIT image encoder to process vision, it\'s very similiar to GPT4, Kosmos, RTX2, and many other multi-modality model architectures\n\n```python\nimport torch\nfrom zeta.structs import (\n  AutoregressiveWrapper,\n  Decoder,\n  Encoder,\n  Transformer,\n  ViTransformerWrapper,\n)\n\n\nclass PalmE(torch.nn.Module):\n    """\n    PalmE is a transformer architecture that uses a ViT encoder and a transformer decoder.\n\n    Args:\n\n        image_size (int): Size of the image.\n        patch_size (int): Size of the patch.\n        encoder_dim (int): Dimension of the encoder.\n        encoder_depth (int): Depth of the encoder.\n        encoder_heads (int): Number of heads in the encoder.\n        num_tokens (int): Number of tokens.\n        max_seq_len (int): Maximum sequence length.\n        decoder_dim (int): Dimension of the decoder.\n        decoder_depth (int): Depth of the decoder.\n        decoder_heads (int): Number of heads in the decoder.\n        alibi_num_heads (int): Number of heads in the alibi attention.\n        attn_kv_heads (int): Number of heads in the attention key-value projection.\n        use_abs_pos_emb (bool): Whether to use absolute positional embeddings.\n        cross_attend (bool): Whether to cross attend in the decoder.\n        alibi_pos_bias (bool): Whether to use positional bias in the alibi attention.\n        rotary_xpos (bool): Whether to use rotary positional embeddings.\n        attn_flash (bool): Whether to use attention flash.\n        qk_norm (bool): Whether to normalize the query and key in the attention layer.\n\n    Returns:\n\n            torch.Tensor: The output of the model.\n\n    Usage:\n\n            >>> img = torch.randn(1, 3, 256, 256)\n            >>> text = torch.randint(0, 20000, (1, 1024))\n            >>> model = PalmE()\n            >>> output = model(img, text)\n            >>> print(output)\n\n    """\n\n    def __init__(\n        self,\n        image_size=256,\n        patch_size=32,\n        encoder_dim=512,\n        encoder_depth=6,\n        encoder_heads=8,\n        num_tokens=20000,\n        max_seq_len=1024,\n        decoder_dim=512,\n        decoder_depth=6,\n        decoder_heads=8,\n        alibi_num_heads=4,\n        attn_kv_heads=2,\n        use_abs_pos_emb=False,\n        cross_attend=True,\n        alibi_pos_bias=True,\n        rotary_xpos=True,\n        attn_flash=True,\n        qk_norm=True,\n    ):\n        super(PalmE, self).__init__()\n\n        # vit architecture\n        self.encoder = ViTransformerWrapper(\n            image_size=image_size,\n            patch_size=patch_size,\n            attn_layers=Encoder(\n                dim=encoder_dim, depth=encoder_depth, heads=encoder_heads\n            ),\n        )\n\n        # palm model architecture\n        self.decoder = Transformer(\n            num_tokens=num_tokens,\n            max_seq_len=max_seq_len,\n            use_abs_pos_emb=use_abs_pos_emb,\n            attn_layers=Decoder(\n                dim=decoder_dim,\n                depth=decoder_depth,\n                heads=decoder_heads,\n                cross_attend=cross_attend,\n                alibi_pos_bias=alibi_pos_bias,\n                alibi_num_heads=alibi_num_heads,\n                rotary_xpos=rotary_xpos,\n                attn_kv_heads=attn_kv_heads,\n                attn_flash=attn_flash,\n                qk_norm=qk_norm,\n            ),\n        )\n\n        # autoregressive wrapper to enable generation of tokens\n        self.decoder = AutoregressiveWrapper(self.decoder)\n\n    def forward(self, img: torch.Tensor, text: torch.Tensor):\n        """Forward pass of the model."""\n        try:\n            encoded = self.encoder(img, return_embeddings=True)\n            return self.decoder(text, context=encoded)\n        except Exception as error:\n            print(f"Failed in forward method: {error}")\n            raise\n\n# Usage with random inputs\nimg = torch.randn(1, 3, 256, 256)\ntext = torch.randint(0, 20000, (1, 1024))\n\n# Initiliaze the model\nmodel = PalmE()\noutput = model(img, text)\nprint(output)\n\n\n```\n\n\n### `Unet`\nUnet is a famous convolutional neural network architecture originally used for biomedical image segmentation but soon became the backbone of the generative AI Mega-revolution. The architecture comprises two primary pathways: downsampling and upsampling, followed by an output convolution. Due to its U-shape, the architecture is named U-Net. Its symmetric architecture ensures that the context (from downsampling) and the localization (from upsampling) are captured effectively.\n\n```python\nimport torch\nfrom zeta.nn import Unet  \n\n# Initialize the U-Net model\nmodel = Unet(n_channels=1, n_classes=2)\n\n# Random input tensor with dimensions [batch_size, channels, height, width]\nx = torch.randn(1, 1, 572, 572)\n\n# Forward pass through the model\ny = model(x)\n\n# Output\nprint(f"Input shape: {x.shape}")\nprint(f"Output shape: {y.shape}")\n\n\n```\n\n\n### `VisionEmbeddings`\nThe VisionEmbedding class is designed for converting images into patch embeddings, making them suitable for processing by transformer-based models. This class plays a crucial role in various computer vision tasks and enables the integration of vision data into transformer architectures!\n\n```python\nfrom zeta.nn import VisionEmbedding\nimport torch\n\n# Create an instance of VisionEmbedding\nvision_embedding = VisionEmbedding(\n  img_size=224,\n  patch_size=16,\n  in_chans=3,\n  embed_dim=768,\n  contain_mask_token=True,\n  prepend_cls_token=True,\n)\n\n# Load an example image (3 channels, 224x224)\ninput_image = torch.rand(1, 3, 224, 224)\n\n# Perform image-to-patch embedding\noutput = vision_embedding(input_image)\n\n# The output now contains patch embeddings, ready for input to a transformer model\n```\n\n# Documentation\n[Click here for the documentation, it\'s at zeta.apac.ai](https://zeta.apac.ai)\n\n\n## Contributing\n- We need you to help us build the most re-useable, reliable, and high performance ML framework ever.\n\n- [Check out the project board here!](https://github.com/users/kyegomez/projects/7/views/2)\n\n- We need help writing tests and documentation!\n\n\n# License \n- MIT',
    'author': 'Zeta Team',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/zeta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
