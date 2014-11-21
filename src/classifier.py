from svmutil import *

def svmClassifier(trainingLabel,testingLabel,featureVectorsTrain,featureVectorsTest):

    """Feed the feature vector to svm to create model"""
    print "Creating SVM Model"
    model = svm_train(trainingLabel, featureVectorsTrain, '-c 0.005 -h 0 -t 0')
    print "Model created. Saving..."

    """Save model"""
    svm_save_model('./sentimentAnalysisSVM.model', model)
    print "Model Saved. Proceed to test..."

    # model = svm_load_model('./sentimentAnalysisSVM.model')
    # print "Model loaded. Proceed to test..."

    predictedLabel, predictedAcc, predictedValue = svm_predict(testingLabel, featureVectorsTest, model)
    print "Finished. The accuracy is:"
    print predictedAcc[0]
    return predictedLabel
