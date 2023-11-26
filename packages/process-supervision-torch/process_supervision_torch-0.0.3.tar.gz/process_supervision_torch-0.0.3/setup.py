# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['process_supervision']

package_data = \
{'': ['*']}

install_requires = \
['autopep8',
 'black',
 'rich',
 'ruff',
 'swarms',
 'transformers',
 'trl',
 'zetascale']

setup_kwargs = {
    'name': 'process-supervision-torch',
    'version': '0.0.3',
    'description': 'Process SuperVision - Pytorch',
    'long_description': '# "Let’s Verify Step by Step"\nImplementation of "Improving Mathematical Reasoning with Process Supervision" by OPENAI \n\n## Install\n`pip3 install --upgrade process-supervision-torch`\n\n\n## Usage:\n\n### GPT4 without tokenizer\n```python\nimport torch \nfrom process_supervision.main import GPT4\n\n# Usage with random inputs\ntext = torch.randint(0, 20000, (1, 1024))\n\n# Initiliaze the model\nmodel = GPT4()\noutput = model(text)\nprint(output)\n```\n\n\n### `PRM`\n```python\nimport torch\nfrom process_supervision.prm import PRM\nfrom swarms.models import OpenAIChat\nfrom process_supervision.generator import MathDataGenerator\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\napi_key = os.getenv("OPENAI_API_KEY")\n\n# LLM initialization\nllm = OpenAIChat(openai_api_key=api_key)\n\n# Math data generator initialization\nmath_datagenerator = MathDataGenerator(llm, num_iters=10)\n\n# Device initialization\ndevice = 0 if torch.cuda.is_available() else "cpu"\n\n# Model initialization\nprm_model = PRM(\n    model_name="lvwerra/gpt2-imdb-pos-v2",\n    ref_model_name="lvwerra/gpt2-imdb",\n    reward_model_name="lvwerra/distilbert-imdb",\n    device=device,\n)\n\n# Generation arguments\ngen_kwargs = {\n    "min_length": -1,\n    "top_k": 0.0,\n    "top_p": 1.0,\n    "do_sample": True,\n    "pad_token_id": prm_model.tokenizer.eos_token_id,\n}\nsent_kwargs = {"top_k": None, "function_to_apply": "none", "batch_size": 16}\n\n# Sample queries\nqueries = ["Sample query 1", "Sample query 2"]\nqueries = [math_datagenerator.generate_samples(query) for query in queries]\n\n# Generate responses\nresponses = prm_model.generate_responses(\n    queries, gen_len=10, gen_kwargs=gen_kwargs\n)\n\n# Score responses\nscores = prm_model.score_responses(responses, sent_kwargs)\n\n# Display results\nfor query, response, score in zip(queries, responses, scores):\n    print(f"Query: {query}\\nResponse: {response}\\nScore: {score}\\n")\n\n```\n\n\n### GPT4 + PRM\n\n\n# Method\n\n\n# Citation\n```bibtex\n@misc{lightman2023lets,\n   title={Let\'s Verify Step by Step}, \n   author={Hunter Lightman and Vineet Kosaraju and Yura Burda and Harri Edwards and Bowen Baker and Teddy Lee and Jan Leike and John Schulman and Ilya Sutskever and Karl Cobbe},\n   year={2023},\n   eprint={2305.20050},\n   archivePrefix={arXiv},\n   primaryClass={cs.LG}\n}\n\n```\n\n# Todo\n- [ ] Creae the PRM reward model\n\n\n\n\n# License\nMIT\n\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Lets-Verify-Step-by-Step',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
