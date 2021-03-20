# Financial Knowledge Graphs

A nested knowledge graph has been constructed as a proof of concept on financial documents. Using the litigation releases from the [SECs Website](https://www.sec.gov/litigation/litreleases.htm).

The documents have been categorised into 4 main categories - Fraud, Insider Trading, Misappropriation of Funds and Unregistered Brokers. (There are more categories, but this is just a PoC so we have considered only these 4 categroies).

After the classification, we have proceeded to extract relevant information from these litigations such as the violations, violators, action taken against the individuals as well as the fine imposed. These have been stored in a tabular format. The above data has also been prepared to be converted into a knowledge graph. The knowledge graph is nested in nature.
An example of one graph has been included below. 

![Sample Knowledge Graph](/results/images/revamped_kg10.png)

The data has also been compiled to ensure that it is easy to view instead of going through all the litigation releases on the SECs website.

![Releases](/results/images/releases.png)

We have also compiled the data according to years and categorized it with the number of occurences of said crimes.

![Years](/results/images/years.png)

### Learnings

We had used a BERT text classification model (accuracy was 24.67%) as well as an Unsupervised LDA topic modelling algorithm to classify the text into different categories, however teh results were extremely poor. A regex parser turned out to perform much better than the previous two models. 
