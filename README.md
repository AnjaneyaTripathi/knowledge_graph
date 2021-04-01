# Knowledge Graphs on Legal Data (SEC)

A knowledge graph has been constructed as a proof of concept on legal documents using the litigation releases from the [SECs Website](https://www.sec.gov/litigation/litreleases.htm).

The documents have been categorised into 4 main categories - Fraud, Insider Trading, Misappropriation of Funds and Unregistered Brokers. (There are more categories, but this is just a PoC so we have considered only these 4).

After the classification, we have proceeded to extract relevant information from these litigations such as the violations, violators, action taken against the individuals as well as the fine imposed. These have been stored in a tabular format. The above data has also been prepared to be converted into a knowledge graph which is nested in nature.

### **Classification of Crimes**

For the classification of crimes, multiple algorithms were implemented to identify them accurately. 4 main classes were picked into which all the documents were classified, they were - Insider Trading, Misappropriation of Funds, Unregistered Brokers and Fraud. Many of the crimes would be a part of multiple classes, so they were classified accordingly. Three approaches were tried, they were:

1. **LDA Unsupervised Topic Modelling:** The first approach was to use an unsupervised model to classify the litigation releases into different classes. Unfortunately, the classification was highly erratic and inaccurate. In addition to this, the releases could not be classified into multiple classes with accuracy. This approach was then scrapped and we decided to use a supervised model.
2. **BERT Text Classification:** The next approach was to use a supervised text classification model for classifying the litigation releases into different categories. It was observed that the BERT model was not able to properly classify the documents into the correct classes. The BERT text classification module performed poorly and had an accuracy of 24.67%. It was then decided to increase the size of the training data, but the accuracy was once again the same. The reason for this could be either that the training and test set were not large enough or that the topics in which we were trying to classify into were closely related and distinguishing between them was hard with insufficient data. We finally decided to read through a handful of documents and identified certain patterns in the litigation releases. This led us to use Regular Expressions.
3. **Regular Expressions:** This was the most robust approach and was extremely accurate. The releases were classified into multiple classes successfully with an accuracy of 95% on the same dataset used for the BERT Topic Classification Model.

As a result, we settled to use a regex parser for the classification of the litigation releases into different crimes.

### **Entity Extraction**

For the construction of the knowledge graph, we tried multiple approaches to identify the relevant entities in the corpus. The approaches were:

1. **Identifying Subject, Object:** Our initial approach was to identify the subject and object of the document and find the relationship between them (either a predicate or the verb word). It was observed that this extraction was not very accurate and the results obtained were not satisfactory. This led us to improve the extraction algorithm and we decided to work on SVO extraction.
2. **SVO Extraction:** This approach involved the identification of triplet phrases. We would identify the subject and object phrases and the relation between the two was the verb phrase. This extraction algorithm performed significantly better than our initial approach. However, in some cases the relationship across the document entities were lost. This shortcoming motivated us to use the concept of ontologies for knowledge graph representation.
3. **Ontologies for Information Extraction:** We decided that since these documents had a lot of similarities between them and we could construct ontology rules from the available litigation releases. The ontology has 5 main classes - Violator, Violation, Crime, Action Taken, Fine and Date. Relationships were drawn between the various classes and this prompted us to use a nested knowledge graph structure instead of the standard triplet relationships. We then classified

### **Classes of the Ontology**

1. **Violators:**
For picking out the violators from the text, multiple litigation releases were studied and it was observed that in most cases the violator&#39;s name was present as part of the heading usually in the form of &#39;Authority name vs Violator name No.&#39; followed by the litigation number. Regular expressions were used to pick out the pattern &#39;vs name No.&#39;, and the violator name was picked out from all occurrences of such patterns.

2. **Laws:**
Three algorithms were constructed to get the sections violated from the text
    1. The first algorithm returned the section violated along with the name of the law, the year it was made and some information about the violation. First, all instances of the pattern &quot;(violat.\*section.\*?)\.&quot; were picked out. Then these instances were split by the word &#39;section&#39;. In order to reinstate the occurrences of &#39;section&#39; which would be removed while splitting, the string &#39;section&#39; was appended to each item except the first. Next, the strings were further split by sentences. After splitting into sentences, each phrase was tested for the presence of numbers, signifying that it contained a section violation. If the phrase did not contain a number, it was considered an explanation to the next section violation and was appended to the start of the next phrase. Furthermore, if the phrase contained the phrase &#39;and&#39; but did not contain any mention of &#39;section&#39; or penalty (denoted by &#39;$), then the text after the &#39;and&#39; was considered unnecessary and dropped from each violation phrase. At the end, the violations are trimmed to remove dangling &#39;and&#39;.  **It was found that the violations returned using the above algorithm contained a lot of filler information which was not necessary to understand which sections were violated.**
    2. After observing the results returned by Algorithm 1, it was decided that the description before the first occurrence of the phrase &#39;violat&#39; could be     removed. Hence, each violation was further trimmed to return only the substring starting with &#39;violat&#39; followed by a brief description of the violation.
    3. The third algorithm was constructed to remove any descriptions that were returned by the first two algorithms. To do this, all patterns of the kind &quot;Section.\*?of [0-9]{4}&quot; (section number followed by Act name and year) or &quot;Section.\*?Act&quot; (section number followed by Act name without year) were found in each sentence and returned as the violations.

3. **Fines:**
The fines levied were found to be of four kinds: disgorgement, penalty, prejudgment interest and total fine. Each of these labels can be identified by the occurrence of the keywords [&#39;disgorge&#39;, &#39;penalt&#39;, &#39;prejudgment interest&#39;,] in the fine string. For each label, the pattern could be, fine amount followed by some description and then label keyword or label keyword followed by description and finally the fine amount. Hence, the text was searched for patterns of the kind &quot;\$.\*?in {keyword}&quot; and &quot;{keyword}.\*?of \$.\*?[\.]&quot;. However, a particular fine amount may be attributed to multiple labels. If a phrase contains multiple labels, it is attributed to the last label it contains.

4. **Action Taken:**
After studying multiple litigation releases, it was found that any paragraph that related to the action taken by legislators contains one or more of the words: [&#39;settlement&#39;, &#39;penalty&#39;, &#39;court granted&#39;, &#39;admitting or denying the allegations&#39;, &#39;seeks&#39;]. For each paragraph, if it contains a sentence that contains any of the keywords, then the entire paragraph starting with that sentence is included under action taken.

5. **Dates:**
A regular expression was used to find out the date when the case was filed.

### **Knowledge Graph Construction**

After the classes have been defined, we proceed to link them to each other using various relationships. These relationships are:

1. Violator → committed → Crime
2. Violator → violated → Law
3. Violator → face → Action
4. Crime → ofValue → Fine

### **Results**

Using the above ontology and the relationships between the various classes, we were able to create a nested knowledge graph. It&#39;s visualisation has been attached below.

![Fig. 1](/results/images/releases.png)

Visualization of the knowledge graph can be seen in Fig 2.

![Fig. 2](/results/images/revamped_kg10.png)

In Fig. 3, we have shown how some insights can be derived from the data that has been extracted.

![Fig. 2](/results/images/years.png)

### **Further Work**

For deriving more insights from the knowledge base that has been created and the accompanying knowledge graph, we can store the data in graph databases such as Neo4j or GraphQL. This allows us to dynamically update the graph and derive inferences from the data. We can also get metadata from the litigation releases. An example can be seen in Fig. 3.
