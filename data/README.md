# Description of the crowdsourcing results json file

This README describes the contents of the file _DocSimHITsResultsALL.json_. The file contains the results from all the crowdsourcing task batches. At the end, we also include some aggregation scripts to create interesting views in case this file is loaded into a MongoDB database.

The _DocSimHITsResultsALL.json_ file contains 813 documents. Each document consists of a HIT, and contains all its properties (e.g. ID, batch ID, timestamp, type of HIT, the HTML script, etc) and all answers the crowd provided to said HIT. Here's the structure of each document:

- _id: This document's unique identifier. This identifier is the same provided by Mechanical Turk when the HIT is created, so you can use this field to look for the HIT at MTurk via boto3 or any other API.
- batch_id: The unique identifier for the batch of HITs which were released together to the marketplace. This is a uuid4 number generated at the time of release of the HITs. All HITs from the same batch share a configuration file, so they'll share most of the properties noted here.
- type: Type of task design used. Either 'pairs' (Variations 1 and 2) or 'ranking' (Variation 3).
- scale: In the case when _type_ equals 'pairs', scale can be either 'likert' or 'magnitude' to specify if the task is from Variation 1 or 2, respectivelly.
- documents_id: The unique identifier (uuid4) used for the set of documents being compared in this HIT. This corresponds to a object in either _DocumentPairSetsForHITS.json_ or _DocumentRankingSetsForHITS.json_.
- documents: A set of documents to be compared, in the shape of a list of pairs (in the case of Variations 1 and 2) or a list of ranking (Variation 3). In the first case, each element of the list has the format:
    - document_1: The first document of the pair.
        - id: The id of the document, as given by the TBFY Tenders API.
        - body: The text of the document.
    - document_2: The second document of the pair.
        - id: Same as above.
        - body: Same as above.
    - g_id: If the pair is a golden pair, this value is 1 if it's the least similar pair, 2 if it's the most similar pair. If not a golden pair, it's 0.


    In the second case, each element of the list has the format:
    - main_document: The document against which other documents are to be ranked against for similarity.
        - id: Same as above.
        - body: Same as above.
    - documents: The list of three documents which are to be ranked according to similarity to the _main_document_. Each of the three has the same format of:
        - id: Same as above.
        - body: Same as above.
- timestamp: The timestamp of when the HIT was sent to MTurk.
- hit: The HIT itself, as taken from the MTurk API. Contains:
    - HITId: Same as __id_. This is in case you only want to use the _hit_ objects.
    - HITTypeId: The identifier for the type of HIT. If you want to create other HITs with details similar to this one, you can give this to the MTurk API when creating hits instead of the normal list of parameters.
    - HITGroupId: The identifier for the HIT group. A HIT group is a group of HITs which can be accepted and worked on in batches by a worker.
    - CreationTime: Not the same as _timestamp_. This is the time when the HIT was created at MTurk, while _timestamp_ is when the HTTP response of the creation from MTurk was captured and registered.
    - Title: Title of the HIT, as shown to the workers.
    - Description: Description of the HIT, as shown to the workers.
    - Question: An XML object with the exact HTML page shown to the worker. If you want to see what the workers responding to this HIT saw, copy the content inside the <HTMLContent> tag to a html file and open it with your browser.
    - Keywords: The keywords for the HIT, as shown to the workers.
    - HITStatus: The status of the HIT. Learn [here](https://blog.mturk.com/understanding-hit-states-d0bc9806c0ee) about the possible status.
    - MaxAssignments: Maximum number of Workers (distinct WorkerIDs) that can work on this HIT. If you need more people, you can launch a new HIT with the same set of documents (_documents_id_) and same HTML code (_hit.Question_).
    - Reward: Monetary compensation, in USD, for each completed and approved assignment.
    - AutoApprovalDelayInSeconds: If approval is automatic, time between assignment completion and approval.
    - Expiration: When the HIT will expire if all assignments are not completed. Otherwise, it expired when all assignments are completed.
    - AssignmentDurationInSeconds: How much time a worker has to finish the assignment once it accepts it.
    - QualificationRequirements: List of requirements a worker must have before working on this HIT. For more information on this, check [here](https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html).
    - HITReviewStatus: If the HIT has been reviewed. This is a manual flag set by who's controlling the HITs. We didn't use it.
    - NumberOfAssignmentsPending: Number of assignments being held by workers, who're currently working on them.
    - NumberOfAssignmentsAvailable: Number of assignments that no worker currently holds.
    - NumberOfAssignmentsCompleted: Number of assignments already completed, but not necessarily accepted.
- answers: This is the list of answers given by workers. Everytime an assignment is completed and accepted, the user's answers are collected and inserted into this list. Each object has the fields:
    - worker_id: The anonymous unique identifier of the worker who submitted these answers. You can use this ID with the MTurk API to block and unblock workers.
    - assignment_id: The unique identifier for the specific assignment these answers refer to.
    - HITId: Same as __id_.
    - values: When you create a HIT, you can have it return a list of named values. These are the values returned by this HIT. For the HITs in this crowdsourcing project, for all three variations, we kept the list of values constant. They are:
        - outputs: List of responses given to each pair/ranking in the pair of documents. In the case of Variations 1 and 2, each document has the form:
            - similarity: The similarity score for that pair.
            - confidence: The confidence level of the worker for that pair.
            - reason: The reason why the worker gave those scores.


            For Variation 3, each document has the form:
            - similarity: An array of 3 values, each for one of the documents to be ranked, representing their place in the ranking.
            - confidence: The confidence level of the worker for that ranking.
            - reason; The reason why the worker ranked them that way.
        - times: A list of times, in seconds, the worker spent in each document pair/ranking of the set.
        - events: A list of events, denoting what happened during the assignment. Each has:
            - timestamp: When the event happened.
            - type: What was the event.
            - attr: Additional attributes of the event.
        - feedback: Any feedback the worker had on the task.