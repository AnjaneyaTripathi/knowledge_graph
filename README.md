# Financial Nested Knowledge Graphs

A nested knowledge graph has been constructed as a proof of concept on financial documents. Using the litigation releases from the [SECs Website](https://www.sec.gov/litigation/litreleases.htm).

The documents have been categorised into 4 main categories - Fraud, Insider Trading, Misappropriation of Funds and Unregistered Brokers. (There are more categories, but this is just a PoC so we have considered only these 4 categroies).

After the classification, we have proceeded to extract relevant information from these litigations such as the violations, violators, action taken against the individuals as well as the fine imposed. These have been stored in a tabular format. The above data has also been prepared to be converted into a knowledge graph. The knowledge graph is nested in nature.
An example of one graph has been included below. 

![Sample Knowledge Graph](/images/revamped_kg10.png)
