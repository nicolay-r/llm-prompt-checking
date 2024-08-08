# LLM Promp Checking Demo
![](https://img.shields.io/badge/Python-3.9-brightgreen.svg)

This project aimed at assessing advances in generative large language models in the domain of Information Retrieval and Relation **Extraction in particular**.

Please refer to the related findings and presentation (RU language) for greater details:

[![YouTube](http://i.ytimg.com/vi/zeKg1MAQrYA/hqdefault.jpg)](https://www.youtube.com/watch?v=zeKg1MAQrYA)

## Usage

This project shares three main scripts:
1. `eval.py` -- dedicated for evaluating accuracies of the binary classification of the manually annotated relations. The output accuaracy shows the alignment with the annotation provided by experts ✍️
2. `graph.py` -- script that adopts D3JS library for visualizing radial graphs that highlights: alignment 🟢 and misalignment 🔴.
3. `launch.py` -- launches the application of the LLM model towards the composed input prompts to perform **binary semantic relations classification** of knonw semantic relations (present / absent, i.e. agree or disagree with experts annotaiton)

> **Update 08/08/2024: ⚠️ **Obsolete** This project adopts `RevGPT` API, which is obsolete at present. Please use the other project such as [QuickCoT](https://github.com/nicolay-r/quick_cot) for inferring other LLM models useing the official API.

## Experiment 

We refer to the [NEREL collection](https://github.com/nerel-ds/NEREL) which is used as a sorce for the semantic relations.

We experiment with `OpenAI/ChatGPT-3.5-0613` model.

## References

The visualization has been taken from the side [ARElight](https://github.com/nicolay-r/ARElight) project
