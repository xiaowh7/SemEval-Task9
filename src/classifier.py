from svmutil import *

def svmClassifier(trainingLabel, testingLabel,
                  featureVectorsTrain, featureVectorsTest, modelFilename = ""):
    """Feed the feature vector to svm to create model"""
    # print "Creating SVM Model"
    # model = svm_train(trainingLabel, featureVectorsTrain, '-c 0.005 -h 0 -t 0')
    # print "Model created. Saving..."
    #
    # """Save model"""
    # svm_save_model('./Semeval2014+SentiStrength3class.model', model)
    # print "Model Saved. Proceed to test..."

    model = svm_load_model('./Semeval2014+SentiStrength3class.model')
    # model = svm_load_model('./Semeval2014SVMc0.005.model')
    print "Model loaded. Proceed to test..."

    predictedLabel, predictedAcc, predictedValue = \
        svm_predict(testingLabel, featureVectorsTest, model)
    print "Finished. The accuracy is:"
    print predictedAcc[0]
    return predictedLabel
