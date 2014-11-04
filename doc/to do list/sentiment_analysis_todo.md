Core Sentiment Analysis Package
- [ ] Documentation, specifically docstrings. Set-up sphinx to organize documentation.
- [ ] Data loader need to refactored to respond gracefully to faults in the provided datasets.
- [ ] Helper function for concatenating train, dev and test data and providing the CV params (important/useful for `learning_curve` or other methods that only accept a single set of data with cross-validation parameters.)
- [ ] Turn the miscellaneous scripts into either package scripts or helper methods
- [ ] Clean up the IPython Notebooks and they can all be executed with "run all" and remove old/irrelevant ones
- [ ] Provide Cookbook with useful snippets
- [ ] Fix the package installer (`setup.py`) to support one-click install, so when the package is distributed, it will install everything required, including e.g. NLTK Copora, etc.
- [ ] Refactor code so all components are consistent. So far, `data.py` and `feature_extraction.py` are fully up-to-date and compliant with the design philosophy, but not so much modules like `analyzer.py`.
- [ ] Twitter conformance tests for tokenization and preprocessing
- [ ] Tests for feature calculation methods
- [ ] Consistent logging

Sentiment Analysis Web Service
- [ ] Deployment documentation
- [ ] More extensive exception handling
- [ ] Additional views useful for analysing text (feature weights, etc)

Research

- SemEval evaluation script
  
  - [ ] If we wish to partake in SemEval-2014 task 9, we need to implement a helper method or snippet to the result of classification on the test data in a way that conforms to the specifications of their scorer.

- Cascade Classifier
  
  - [ ] As a first step, we need to simply take the instances with gold-standard annotation of `positive`/`negative` and train a polarity classifier. We also normalize these instances (`positive`/`negative`) into equivalence class `subjective` and train a subjectivity classifier with the `objective/neutral` instances. See if we obtain promising results from this. 
  - [ ] If so, there is a bit of implementation required to support this kind of cascaded classier (http://stackoverflow.com/questions/21151346/cascade-classifiers-for-multiclass-problems-in-scikit-learn/21159014#21159014)

- Sentiment Lexicon
  
  - [ ] Incorporate the sentiment lexicons used by (Mohammad et al. 2013) into the `TweetFeaturesaExtractor` so features can be computed based on these lexicons. All of these lexicons have been obtained and reside in the `resources` directory.

- Negation

  - [ ] Potts 2011 (http://sentiment.christopherpotts.net/lingstruc.html) describe an interesting way to handle words under the semantic scope of negation. This method has been implemented as an option in the preprocessing step of the pipeline but not yet evaluated. N.B. Mohammad et al. 2013 also adopt this approach.
  
- Part-of-Speech tagging
  
  - [ ] Many works on sentiment analysis use part-of-speech tagging one way or another. Either by appending the tags to the tokens, or having some integer-valued feature which counts the occurrence of a particular part-of-speech. Both of these have been implemented as options in various components of the pipeline but again is yet to evaluated.

- Feature Selection
  
  The Recursive Feature Elimination (RFE) method introduced by (I Guyon et al. 2002) has shown promising improvements. We're able to distill the minimal set of features required to obtain comparable or even better accuracy. However, as with all feature selection methods, we are wary of overfitting: the increase in performance could be attributed to the fact that we've removed sufficient noise from our feature space and distilled the truly general sentiment-bearing features with excellent discriminative capabilities, but it could also be attributed to extreme overfitting to our training set. This is the toughest counter-argument to the soundness of this method and to address this, we need to:

  - [ ] Reimplement the RFE method so the scoring is done against the held-out test set, rather than a cross-validation on all available data. The `RFECV` method provided by `scikit-learn` is broken beyond repair (https://github.com/scikit-learn/scikit-learn/issues/2403#issuecomment-33963597).
  - [ ] Bias-Variance Analysis: learning curves of error committed on training and test sets. Use http://see.stanford.edu/materials/aimlcs229/ML-advice.pdf to guide this analysis.
  - [ ] If we take the subset of features which yielded the best performance on the held-out test set (assuming the performance does peak as before with the CV results), we need to know how it will perform on out-of-domain data. Immediately, we can apply this to the SemEval SMS dataset but perhaps data from another social media platform is more desirable. As a baseline, we take the trained model using all the features and test this against out-of-domain data. Then we can test this with the minimal subset of features.
  - [ ] Another question is how this method compares to simply taking the top `n` features and dropping the rest. This is equivalent a single iteration of RFE. To do this, we should first run RFE to find the optimal number of features say `m`. Then, we train another model just once and only keep the top `m` features and analyse the difference not just in their performace: do the same features appear in both? What characterizes the symmetric difference between these set of `m` features? This will test whether it is neccessary to use the computationally intensive iterative feature elimination approach which trains a new model on each iteration or whether we can just train the model once and simply keep the top `n`.
  - [ ] We need to address why we chose this particular method over the myriad of other popular methods. The results from the above should already be compelling but we should try other methods simply for completeness:
    - Principal Component Analysis.
    - Univariate feature selection with information gain or chi-squared.
    - `tf-idf, min/max df`. If we specify something like `min df` or even perform `tf-idf` weighting, in some sense, we are removing or down-weighting some features we suspect won't be very discriminative already even before we fit a model to it. We should compare these to the methods which perform feature elimination *after* the data has been fitted to a model.

- Kernels
  - [ ] String Kernel
  - [ ] Tree Kernel

- Report
  - [ ] A thorough and comprehensive write-up describing every detail of work conducted on the sentiment analysis problem.