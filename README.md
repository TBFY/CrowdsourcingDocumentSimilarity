# Document Similarity Crowdsourced Task

## Intro

This repository contains the data, scripts and documents used for running the crowdsourcing tasks which try to validate the Document Similarity algorithm used in WP3 of the TBFY project.

We created and ran through workers in the Mechanical Turk platform a series of Human Intelligence Tasks (HITs), using three variations of a Document Similarity task:

- Variation 1: We showed workers 5 pairs of documents and, for each, asked them to rate their similarity in a 4-level Likert scale (None, Low, Medium, High), tell us a confidence level of how sure they were (from 0 to 4) and a written reason as to why they chose that similarity level. For quality reasons, two of the 5 pairs were golden-standards, which means we knew their ratings already and checked the workers responses. They had to give the golden pair with the higher similarity a higher score than the other golden pair, otherwise their answer would be rejected.
- Variation 2: We repeated variation 1 but with a slight alteration: instead of a Likert scale for the similarity score, we asked for a Magnitude Estimation, which is any number above 0. It could be 1, 0.0001, 1000, 42, as long as it was coherent, as in a more similar pair had a higher score than a less similar pair and vice-versa;
- Variation 3: We showed workers 5 rankings. Each ranking had a main document and 3 auxiliary documents to be compared against the main one. They also had to report a confidence score and give a short written reason, just like variation 1. The first ranking is a golden-standard, and we knew the values for the 3 pairs in it (the pairs were the main document paired with each of the 3 auxiliary documents), and they had to give the golden pair with the highest similarity a higher rank than the one with the lower similarity.

We also checked the time they spent in each pair and if they moved all controls. Failing these checks meant we didn't accept their responses.

## Repository Structure

The repository is structured as follows: A config folder with configuration files, a data folder with all the data used, and .html, .py and .ipynb with the scripts used to create and run HITs, and to collect results.

### Config

- _banlist.json_ contains the Worker IDs for all workers we identified as spammers;
- _task_content_pairs_likert.json_ contains the configurations used to run the Variation 1 HITs;
- _task_content_pairs_magnitude.json_ contains the configurations used to run the Variation 2 HITs;
- _task_content_ranking.json_ contains the configurations used to run the Variation 3 HITs;

### Data

- _DocSimHITsResultsALL.json_ is the file with all the results from the crowdsourcing, from every worker, for every variation. For the description of the contents, check the README file in the data folder;
- _DocumentPairSetsForHITS.json_ is the file which contains all sets of pairs to be sent on the HITs for variations 1 and 2. Each set has the content of one HIT;
- _DocumentRankingSetsForHITS.json_ is the file which contains all sets of rankings to be sent on the HITs for variation 3. Each set has the content of one HIT;
- _documents_en_nometadate.json_ is the _documents.csv_ file processed to include only english documents with no extra information to them;
- _documents.csv_ is the file of all documents as provided by Carlos/Oscar;
- _final_scores_likert.csv_ is the resulting scores for each pair using the variation 1 tasks;
- _final_scores_magnitude.csv_ is the resulting scores for each pair using the variation 2 tasks;
- _final_scores_ranking.csv_ is the resulting scores for each pair using the variation 3 tasks;
- _golden-case-x.md_, with x from 1 to 5 are the golden-data sets provided by Carlos/Oscar;
- _golden-data.json_ is the 5 files above turned into json;
- _golden-data-pairs.json_ is the file above turned into pairs of documents;
- _golden-data-pairs-new.json_ is the final version of the above file we used. We discovered that people were failing a lot of quality checks because they did not naturally agree with the similarity concept used in the original golden-data sets, and they were sending lots of complaints about it. So we made it easier for them to spot which pair is the most similar by inserting another level of similarity, which is basically the main document paraphrased. People stopped complaining and the tasks completed;
- _pairs.csv_ is the pairs file given by Carlos/Oscar;
- _pairs_en.csv_ is the file above but only where both documents are in english;
- _pairs_en.json_ is the file above but json.

### Scripts

- _DocSimPairsLikertMockup.html_ is an example of the Variation 1 task which you can open on your browser;
- _DocSimPairsMagnitudeMockup.html_ is an example of the Variation 2 task which you can open on your browser;
- _DocSimPairsRankingMockup.html_ is an example of the Variation 3 task which you can open on your browser;


- _DocSimPairsTemplate.html_ is the file which serves as template for the Variation 1 and 2 tasks. It is populated by the contents of the corresponding config file and with one of the input elements below;
- _contextSliderTemplate.html_ is the input element for the Variation 1 task, used to complete the _DocSimPairsTemplate.html_ file;
- _contextMagnitudeTemplate.html_ is the input element for the Variation 2 task, used to complete the _DocSimPairsTemplate.html_ file;
- _DocSimRankingTemplate_ is the file which serves as template for the Variation 3 task. It is populated by the contents of the corresponding config file;


- _GenerateDocumentSets.ipynb_ is the notebook which takes the raw _documents_en_nometadata.json_, _pairs_en.csv_ and _golden-data-pairs-new.json_ files and turns them into the document sets to be sent in the HITs. Each document set is the document pairs/ranking which will be shown in a HIT;
- _ExperimentRunner.ipynb_ is the notebook which runs the HITs;
- _HITAnswerExplorer.ipynb_ is the notebook which analyses the results from the HITs;


- _krippendorff_alpha.py_ is the python script which has the code for the krippendorff alpha. Created by Thomas Grill;
- _mturk.py_ is the python script which serves as an interface to the MTurk API in the boto3 package. You should create a _config/amazon_credentials.json_ file with a valid access key and secret key to use MTurk with boto3;
- _update_db.py_ is the script which updates a mongodb database with the HITs created.