# LLM Reasoning Checking in Semantic Relation Extraction
![](https://img.shields.io/badge/Python-3.9-brightgreen.svg)

This project aimed at assessing advances in generative large language models in the domain of Information Retrieval and Relation **Extraction in particular**.

Please refer to the related findings and presentation (RU language) for greater details:

[![YouTube](http://i.ytimg.com/vi/zeKg1MAQrYA/hqdefault.jpg)](https://www.youtube.com/watch?v=zeKg1MAQrYA)

**Presentation**: https://nicolay-r.github.io/website/data/report_llm2023-nerel.pdf

## Usage

This project shares three main scripts:
1. `eval.py` -- dedicated for evaluating accuracies of the binary classification of the manually annotated relations. The output accuaracy shows the alignment with the annotation provided by experts ✍️
2. `graph.py` -- script that adopts D3JS library for visualizing radial graphs that highlights: alignment 🟢 and misalignment 🔴.
3. `launch.py` -- launches the application of the LLM model towards the composed input prompts to perform **binary semantic relations classification** of knonw semantic relations (present / absent, i.e. agree or disagree with experts annotaiton)

> **Update 08/08/2024:** ⚠️ This project adopts `RevGPT` API, which is obsolete at present. Please use the other project such as [QuickCoT](https://github.com/nicolay-r/quick_cot) for inferring other LLM models useing the official API.

## Experiment 

We refer to the [NEREL collection](https://github.com/nerel-ds/NEREL) which is used as a sorce for the semantic relations.

We experiment with `OpenAI/ChatGPT-3.5-0613` model.

### Results

Results are shortly higlighted in [the related presentation](https://nicolay-r.github.io/website/data/report_llm2023-nerel.pdf)

Top 3 relation types are bolded:

|Relation Type |Accuracy | Number of Relations |
|-|-|-|
|**CAUSE_OF_DEATH** |0.93|41|
|**DATE_OF_BIRTH** |0.92|114|
|**DATE_OF_DEATH** |0.86|87|
|PLACE_OF_DEATH |0.86|63|
|END_TIME |0.86|22|
|START_TIME |0.82|38|
|PLACE_OF_BIRTH |0.76|97|
|DATE_OF_CREATION |0.75|117|
|SCHOOLS_ATTENDED |0.74|84|
|PART_OF |0.73|45|
|MEMBER_OF |0.72|218|
|WORKS_AS |0.71|3053|
|LOCATED_IN |0.71|611|
|TAKES_PLACE_IN |0.7|1222|
|SUBEVENT_OF |0.68|212|
|DATE_FOUNDED_IN |0.68|44|
|DATE_DEFUNCT_IN |0.67|6|
|AWARDED_WITH |0.64|401|
|ORIGINS_FROM |0.61|956|
|RELIGION_OF |0.61|31|
|RELATIVE |0.57|30|
|MEDICAL_CONDITION |0.57|196|
|OWNER_OF |0.54|94|
|PENALIZED_AS |0.54|123|
|WORKPLACE |0.53|804|
|PARENT_OF |0.5|200|
|SIBLING |0.48|86|
|SPOUSE |0.47|119|
|PARTICIPANT_IN |0.42|2764|
|HAS_CAUSE |0.42|481|
|KNOWS |0.41|264|
|EXPENDITURE |0.41|29|
|ALTERNATIVE_NAME |0.4|942|
|FOUNDED_BY |0.37|86|
|ORGANIZES |0.3|123|
|CONVICTED_OF |0.22|286|
|SUBORDINATE_OF |0.15|105|


## References

The visualization has been taken from the side [ARElight](https://github.com/nicolay-r/ARElight) project
