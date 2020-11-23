import pandas as pd
from joblib import dump, load
import numpy as np
import io
from sklearn.model_selection import train_test_split
from skimage.segmentation import watershed
from skimage import exposure
from scipy import ndimage
from sklearn.ensemble import ExtraTreesClassifier
from skimage.color import rgb2hsv,rgb2gray
from collections import OrderedDict

uv_data = pd.read_csv('Main/DataSienceUV/uv_data.csv')


class UV_Model(object):
  
    def __init__(self,model=None):
        if model == None:
            self.features = pd.read_csv('Main/DataSienceUV/features.csv')
            self.y = uv_data['segment_value']
            self.etc = ExtraTreesClassifier(criterion='gini',min_samples_split=3) #warm_start=True
            self.etc.fit(self.features,self.y)
        else:
            self.etc = load(model)
    
    def __histogram_equalize(self,img):
        img_cdf, bin_centers = exposure.cumulative_distribution(img)
        return np.interp(img, bin_centers, img_cdf)
  
    def __get_features(self,photo,mask,segment_num):
        # Get segment from photo
        p1 = np.ma.masked_where(mask == segment_num, photo[:,:,0])
        p2 = np.ma.masked_where(mask == segment_num, photo[:,:,1])
        p3 = np.ma.masked_where(mask == segment_num, photo[:,:,2])
        # Get histograms 3 chanels of photo
        hist1 = np.histogram(p1.mask * p1.data, bins = 32, range = (0,1))
        hist2 = np.histogram(p2.mask * p2.data, bins = 32, range = (0,1))
        hist3 = np.histogram(p3.mask * p3.data, bins = 32, range = (0,1))

        features = np.concatenate((np.array(hist1[0][1:] / np.sum(p1.mask),dtype=object),
                                  np.array(hist2[0][1:] / np.sum(p2.mask),dtype=object),
                                  np.array(hist3[0][1:] / np.sum(p3.mask),dtype=object)))
        return features

    def __segment_preprocessing(self,photo,mask,segment_num):
        hsv_features = self.__get_features(rgb2hsv(photo),mask,segment_num)
        rgb_features = self.__get_features(self.__histogram_equalize(photo),mask,segment_num)
        vector = np.concatenate((hsv_features,rgb_features))
        return vector

    def __get_important_features(self,features):
        discarded_features = np.load('Main/DataSienceUV/not_importance_features.npy')
        for i in range(len(discarded_features)):
            features.drop(discarded_features[i],axis='columns', inplace=True)
        return features

    def __photo_preprocessing(self,photo,mask,json_data=None):
        features_arr = []
        if json_data == None:
            unique_segments = list(OrderedDict.fromkeys(mask.ravel()))
        else:
            unique_segments = list(map(int,json_data.keys()))
            y = []
        for i in unique_segments:
            vector = self.__segment_preprocessing(photo,mask,i)        
            features_arr.append(list(vector))
            if json_data != None:
                y.append(json_data[str(i)])
    
        features = pd.DataFrame(features_arr)
        features = self.__get_important_features(features)
        if json_data != None:
            y = pd.Series(y)
            features['y'] = y
    
        return features
  
    def __to_semantic_segmentation(self,mask,predicts):
        labels_uniq = list(OrderedDict.fromkeys(mask.ravel()))
    
        for i in range(predicts.shape[0]):
            if predicts[i] == 'Отсутствует':
                mask = np.where(mask == labels_uniq[i],100,mask)
            if predicts[i] == 'Насыщенное':
                mask = np.where(mask == labels_uniq[i],200,mask)
            if predicts[i] == 'Карбонатное':
                mask = np.where(mask == labels_uniq[i],300,mask)
        return mask
  
    def predict(self,photo):
        mask = watershed(rgb2gray(photo),markers=12)
        photo_features = self.__photo_preprocessing(photo,mask)
        predicts = self.etc.predict(photo_features)
        semantic_seg = self.__to_semantic_segmentation(mask,predicts)
        return semantic_seg
    
    def retrain(self,photos,masks,jsons):
        for i in range(len(photos)):
            photo = photos[i]
            mask = masks[i]
            json_data = jsons[i]
            features = self.__photo_preprocessing(photo,mask,json_data)
            y = features['y']
            features.drop(['y'],axis='columns', inplace=True)
            #self.etc.fit(features,y)
            for i in range(features.shape[0]):
                self.features.loc[self.features.shape[0]] = features.loc[i].tolist()
                self.y.loc[self.y.shape[0]] = y.loc[i]
        self.etc.fit(self.features,self.y)
  
    def save_model(self, name):
        dump(self.etc, name)
