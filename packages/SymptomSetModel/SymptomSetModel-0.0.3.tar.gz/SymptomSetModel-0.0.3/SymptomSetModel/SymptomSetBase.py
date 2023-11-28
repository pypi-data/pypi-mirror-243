import pandas as pd 
import numpy as np
from scipy import sparse
from scipy.special import gammaln,betaln,expit,digamma
import pickle
from sklearn.metrics import precision_recall_curve, average_precision_score

SMALL_FLOAT=np.finfo(np.float64).eps
MINLOG = np.log(SMALL_FLOAT)

class InferenceDataStruct:

	def __init__(self,sparse_data_array,subject_index,target_hpo_to_index_map):
		"""This class constructs a series of data structures that simplify the inference/application of the SymptomSetModel. 
		
		Args:
		    sparse_data_array (sparse.csr_array): sparse.csr_array of binary indicators, which represent the set of symptoms (columns) diagnosed in each subject (rows).
		    subject_index (pandas.Series): Subject ID-to-array rows, provided using a pd.Series data structure 
		    target_hpo_to_index_map (pandas.Series): HPO ID-to-array columns, provided using a pd.Series data structure 
		"""
		self.all_subjects=subject_index.index
		self.target_hpo_to_oringal_index_map=target_hpo_to_index_map
		self.oringal_index_map_to_hpo=pd.Series(target_hpo_to_index_map.index,target_hpo_to_index_map.values)
		self.new_index_to_original_index_map=pd.Series(target_hpo_to_index_map.values,index=np.arange(len(target_hpo_to_index_map)))
		self.orignal_index_to_new_index_map=pd.Series(np.arange(len(target_hpo_to_index_map)),index=target_hpo_to_index_map.values)

		symptom_counts=sparse_data_array[:,self.target_hpo_to_oringal_index_map.values].sum(axis=1)

		no_symptoms=np.where(symptom_counts==0)[0]
		at_least_one_symptom=np.where(symptom_counts>0)[0]

		self.all_asymptomatic_cases=pd.Series(no_symptoms,index=subject_index.index[no_symptoms])
		self.all_symptomatic_cases=pd.Series(at_least_one_symptom,index=subject_index.index[at_least_one_symptom])


		#Find all of the unique symptom sets and where they occur. 
		symptomatic_lil_array=sparse.lil_array(sparse_data_array[self.all_symptomatic_cases.values][:,self.target_hpo_to_oringal_index_map.values])
		unique_symptom_sets,array_of_unique_indices=np.unique(symptomatic_lil_array.rows,return_inverse=True)

		self.unique_symptom_sets=pd.Series([self.new_index_to_original_index_map.loc[x].values for x in unique_symptom_sets],index=map(str,np.arange(len(unique_symptom_sets))))
		self.symptomatic_patients_to_unique_sets=pd.Series(map(str,array_of_unique_indices),index=self.all_symptomatic_cases.index)

		self.symptoms_to_unique_sets={}
		for u_id,symptom_array in self.unique_symptom_sets.items():
			for symp in symptom_array:
				try:
					self.symptoms_to_unique_sets[self.oringal_index_map_to_hpo[symp]]+=[u_id]
				except KeyError:
					self.symptoms_to_unique_sets[self.oringal_index_map_to_hpo[symp]]=[u_id]
		self.symptoms_to_unique_sets=pd.DataFrame({'HPO':list(self.symptoms_to_unique_sets.keys()),'SET_ID':list(self.symptoms_to_unique_sets.values())})
		self.symptoms_to_unique_sets.set_index('HPO',inplace=True)


		self.unique_sets_to_patient_map={}
		for p_id,u_id in self.symptomatic_patients_to_unique_sets.items():
			try:
				self.unique_sets_to_patient_map[u_id]+=[p_id]
			except KeyError:
				self.unique_sets_to_patient_map[u_id]=[p_id]
		self.unique_sets_to_patient_map=pd.DataFrame({'SET_ID':list(self.unique_sets_to_patient_map.keys()),'SUBJECT_ID':list(self.unique_sets_to_patient_map.values())})
		self.unique_sets_to_patient_map.set_index('SET_ID',inplace=True)

		self.num_unique_sets_total=self.unique_symptom_sets.shape[0]


	def _compute_independent_counts(self,independence_indicator_weights):
		independent_counts=np.zeros((len(self.target_hpo_to_oringal_index_map),2))
		for u_idx,p_id in self.unique_sets_to_patient_map.iterrows():
			independent_counts[[self.orignal_index_to_new_index_map[orig_index] for orig_index in self.unique_symptom_sets[u_idx]],0]+=np.sum(independence_indicator_weights.loc[p_id.SUBJECT_ID])
		independent_counts[:,1]=independence_indicator_weights.sum()-independent_counts[:,0]
		return pd.DataFrame(independent_counts,index=self.target_hpo_to_oringal_index_map.index,columns=['Present','Absent'])


	def _compute_set_based_counts(self, set_indicator_weights):
		target_count_vec=pd.Series(np.zeros(self.num_unique_sets_total+1),index=np.concatenate([self.unique_symptom_sets.index,np.array(['NULL'])]))
		for u_idx,p_id in self.unique_sets_to_patient_map.iterrows():
			target_count_vec.loc[u_idx]+=np.sum(set_indicator_weights.loc[p_id.SUBJECT_ID])
		target_count_vec.loc['NULL']+=np.sum(set_indicator_weights.loc[self.all_asymptomatic_cases.index])
		return target_count_vec


class SymptomSetBase:
	def _beta_exp_log_x(self,alpha,beta):
		return digamma(alpha)-digamma(alpha+beta)

	def _beta_exp_log_1mx(self,alpha,beta):
		return digamma(beta)-digamma(alpha+beta)

	def _beta_entropy(self,alpha,beta):
		return betaln(alpha,beta)-(alpha-1.0)*digamma(alpha)-(beta-1.0)*digamma(beta)+(alpha+beta-2.0)*digamma(alpha+beta)

	def _dirichlet_entropy(self,pvec):
		return self._multivariate_log_beta(pvec)+(np.sum(pvec)-pvec.shape[0])*digamma(np.sum(pvec))-np.sum((pvec-1.0)*digamma(pvec))
	
	def _dirichlet_log_like(self,log_prob_vec,param_vec):
		return np.sum((param_vec-1.0)*log_prob_vec)-self._multivariate_log_beta(param_vec)

	def _multivariate_log_beta(self,alpha_vec):
		return np.sum(gammaln(alpha_vec))-gammaln(np.sum(alpha_vec))

	def _dirichlet_exp_logx(self,param_vec):
		return digamma(param_vec)-digamma(np.sum(param_vec))

	def _dirichlet_marg_like(self,obs_vec,pvec):
		prior_norm_const=self._multivariate_log_beta(pvec)
		posterior_norm_const=np.sum(gammaln(pvec+obs_vec))-gammaln(np.sum(pvec+obs_vec))
		return posterior_norm_const-prior_norm_const
				


	def _removeZeros(self):
		counts=np.array(self.SparseSymptomMatrix.sum(axis=0)).ravel()
		missing_counts=np.where(counts==0)[0]
		obs_counts=np.where(counts>0)[0]
		if missing_counts.shape[0]>0:
			print('Warning: {0:d} symptoms have no observed diagnoses. Dropping from dataset. If you believe this is an error, please double check your matrix of diagnoses.'.format(missing_counts.shape[0]))
			self.SparseSymptomMatrix=self.SparseSymptomMatrix[:,obs_counts]
			self.HPOColumns=self.HPOColumns[obs_counts]
			self.HPOIndexMap=pd.Series(np.arange(self.SparseSymptomMatrix.shape[1]),index=self.HPOColumns)

	def __init__(self,SubjectIndex,HPOColumns,SparseSymptomMatrix):
		"""
		
		This class stores and performs basic operations over a sparse, binary matrix of symptoms. Each subject is has a unique identifer, which corresponds to the rows of the matrix. Symptom column names are similarly stored.
		
		Args:
			SubjectIndex (array-like): Array of subject indices
			HPOColumns (array-like): Labels for the HPO-derived symptoms
			SparseSymptomMatrix (sparse.csr_array): Sparse matrix of symptoms
		
		"""


		self.SubjectIndex=np.array(SubjectIndex)
		assert len(set(self.SubjectIndex))==self.SubjectIndex.shape[0],"Patient indices contain duplicate columns."
		self.HPOColumns=np.array(HPOColumns)
		assert len(set(self.HPOColumns))==self.HPOColumns.shape[0],"Symptom array columns contain duplicate HPO terms."
		self.SparseSymptomMatrix=SparseSymptomMatrix

		assert isinstance(self.SparseSymptomMatrix,sparse.csr_array),"HPO data matrix must be a scipy.sparse_csr array."

		self.SubjectIndexMap=pd.Series(np.arange(SparseSymptomMatrix.shape[0]),index=self.SubjectIndex)
		self.HPOIndexMap=pd.Series(np.arange(SparseSymptomMatrix.shape[1]),index=self.HPOColumns)
		self._removeZeros()


	def DropLowFrequencySymptoms(self,min_freq):
		"""Drops all symptoms with prevelance less than min_freq from the dataset. The dataset is then re-indexed.
		
		Args:
		    min_freq (float): Minimum allowed prevalence for symptoms. 
		"""
		freqs=np.array(self.SparseSymptomMatrix.mean(axis=0)).ravel()
		dropped=np.where(freqs<min_freq)[0]
		allowed=np.where(freqs>=min_freq)[0]
		print('{0:d} symptoms with prevalence < {1:f}. Dropping from dataset.'.format(dropped.shape[0],min_freq))
		self.SparseSymptomMatrix=self.SparseSymptomMatrix[:,allowed]
		self.HPOColumns=self.HPOColumns[allowed]
		self.HPOIndexMap=pd.Series(np.arange(self.SparseSymptomMatrix.shape[1]),index=self.HPOColumns)


	def PheRS(self,hpo_terms,training_fraction):
		"""Contructs a PheRS (see PMID: 29590070) for a set of HPO terms using the instantiated symptom matrix.
		
		Args:
		    hpo_terms (list-like): HPO terms for PheRS 
		    training_fraction (float): Float in (0.0, 1.0] that indicates what fraction of the dataset should be used for training (the remainder is used for testing/validation of score)
		
		Returns:
		    Dictionary: Dictionary of results is returned, which containes the following information: {'PheRS_Weights':pd.Series containing the weights for each HPO term,'Training': pd.Series containing PheRS for training dataset,'Testing':pd.Series containing PheRS for testing dataset}
		"""
		missing_terms=set(hpo_terms).difference(self.HPOColumns)

		new_index_array=np.copy(self.SubjectIndex)
		np.random.shuffle(new_index_array)
		cutoff=int(np.floor(training_fraction*new_index_array.shape[0]))
		training_index=new_index_array[:cutoff]
		testing_index=new_index_array[cutoff:]

		if len(missing_terms)>0:
			print('Warning: {0:s} are not in the datset. Note: they may have been dropped because their frequency was too low.'.format(','.join(missing_terms)))
			hpo_terms=list(hpo_terms.intersection(self.HPOColumns))

		hpo_indices=pd.Series([self.HPOIndexMap[x] for x in hpo_terms],index=hpo_terms)

		assert np.sum(self.SparseSymptomMatrix[:,hpo_indices][self.SubjectIndexMap[training_index],:].sum(axis=0)==0)==0,"There are symptoms with no observations in the training data. Please either increase training dataset size or drop low frequency symptoms."

		surprisals=-1.0*np.log(self.SparseSymptomMatrix[self.SubjectIndexMap[training_index]].mean(axis=0))[hpo_indices]

		training_phers=self.SparseSymptomMatrix[self.SubjectIndexMap[training_index]][:,hpo_indices].multiply(surprisals.reshape(1,-1)).sum(axis=1)

		if testing_index.shape[0]>0:
			testing_phers=self.SparseSymptomMatrix[self.SubjectIndexMap[testing_index]][:,hpo_indices].multiply(surprisals.reshape(1,-1)).sum(axis=1)
		else:
			testing_phers=np.array([])
		return {'PheRS_Weights':pd.Series(surprisals,index=hpo_terms),'Training':pd.Series(training_phers,index=training_index),'Testing':pd.Series(testing_phers,index=testing_index)}

	def BasicPerformanceStats(self,labels,scores):
		"""Given a set of true labels and a set of scores (both of which should be pd.Series with the same index), returns 
		
		Args:
		    labels (pd.Series): pd.Series containing the true labels for a set of subjects
		    scores (pd.Series): pd.Series containing the scores for a set of subjects
		
		Returns:
		    Dictionary: {'Precision': Precision statistics at all score cutpoints,'Recall': Recall statistics at all sacore cutpoints,'AvgPrecision':Average precision score from sklearn}
		"""
		assert isinstance(labels,pd.Series), "Expects labels to be a pd.Series with the index corresponding to the the patient indices."
		assert isinstance(scores,pd.Series), "Expects scores to be a pd.Series with the index corresponding to the the patient indices."
		avg_precision_score=average_precision_score(labels,scores)
		prec,recall,thresh=precision_recall_curve(labels,scores)

		results={'Precision':prec,'Recall':recall,'AvgPrecision':avg_precision_score}

		return results



