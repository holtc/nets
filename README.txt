README

Our repository has 3 subdirectories: data, docs, and src.

/data:
We have all of our sample input and output data for our aggregation and quality control modules.

sample_qc_input.txt: This file shows a sample quality control input file for 6 different tweets, each identified by their articleId. For each worker, we will compare their labels with the goldenlabels, and assign a quality multiplier to them based on how many correct and incorrect labels they provide. A label is correct if it matches the golden label. 

sample_qc_output.txt: We see the quality multipliers that each worker received; in this example, worker1 received a multiplier of 1, and worker2 received a multiplier of 0.6.
  
sample_agg_input.txt: This file shows the input data that we will receive for 6 different tweets. Each tweet is identified by its articleId, and each worker that worked on the tweet has a workerId. labelpos and labelneg refer to the labels that the worker assigned the tweet. These are the three input parameters that we need for aggregation.

sample_agg_output.txt: Here, we have assigned final labels to each tweet by aggregating the labels provided by each worker. For each tweet, we find all of the workers who worked on the tweet, we find each of their worker quality multipliers, and we find the label that each worker assigned. We generate a final label by using a weighted average (quality multiplier*label) across all workers on each tweet. 

/data/raw:
We provide one sample raw tweet - we will collect thousands of these tweets and upload them to Crowdflower to collect judgements.


/docs:
We provide a Flow Chart that outlines the overall flow of our project.
We provide 2 screen shots of a sample HIT, as it appears on CrowdFlower.

/src:
We provide the implementation of our aggregation module and our qc module. The behavior of these scripts matches the behavior described above.