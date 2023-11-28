import pandas as pd 
import numpy as np
from scipy.special import logsumexp,betaln
from scipy.stats import beta as beta_dist
from scipy.optimize import fsolve
import time
from scipy.optimize import fmin
from scipy.integrate import quad
import tqdm
import warnings
from .SymptomSetBase import InferenceDataStruct,SymptomSetBase
from .DirichletSymptomPrior import DirichletSymptomPrior

SMALL_FLOAT=np.finfo(np.float64).eps
MINLOG = np.log(SMALL_FLOAT)

__version__ = "0.0.3"

class SymptomSetModel(SymptomSetBase):

	"""

	Probailistic genotype-to-phenotype model for rare diseases, where phenotype represents an arbitrary set of binary symptoms. The full model is specified as:

	P(Symptom Set|Subject-specific Parameters, Variant)=P(Penetrance|Variant,Subject-specific Parameters)*P(Symptom Set|Penetrance,Variant,Subject-specific parameters). 
	
	The model is initialized by providing a sparse matrix of binary symptoms, with labels for the rows and columns denoting subjects and HPO-derived symptoms respectively. 

	Args:
		SubjectIndex (array-like): Array of subject indices, with order matching the provided symptom array
		HPOColumns (array-like): Labels for the HPO-derived symptoms, with order matching the provided symptom array.
		SparseSymptomMatrix (scipy.csr_array): Sparse array of diagnosed symptoms
	"""
	
	def _convert_bounds_to_beta_prior(self,lower_bound,upper_bound,CI=0.99,tol=1e-8):
		mean=lower_bound+(upper_bound-lower_bound)/2.0
		init_denom=(1.0/mean)*100
		log_a=np.log(init_denom*mean)
		log_b=np.log(init_denom-np.exp(log_a))

		f=lambda x: np.sqrt((upper_bound-beta_dist(np.exp(x[0]),np.exp(x[1])).ppf(1.0-(1.0-CI)/2.0))**2+(lower_bound-beta_dist(np.exp(x[0]),np.exp(x[1])).ppf((1.0-CI)/2.0))**2)
		output=fmin(f,np.array([log_a,log_b]),ftol=tol,disp=False)
		return np.exp(output)


	def _null_arbitrary_model(self, ControlSubjects,InferenceStruct,SetPrior):
		control_indicators=pd.Series(np.zeros(InferenceStruct.all_subjects.shape[0]),index=InferenceStruct.all_subjects)
		control_indicators.loc[ControlSubjects]=1.0
		freq_counts=InferenceStruct._compute_set_based_counts(control_indicators)
		posterior_params=freq_counts+SetPrior/InferenceStruct.num_unique_sets_total
		set_log_likelihoods=np.log(posterior_params/np.sum(posterior_params))
		return set_log_likelihoods

	def _null_independent_model(self,ControlSubjects,InferenceStruct,IndependentFreqPrior):
		control_indicators=pd.Series(np.zeros(InferenceStruct.all_subjects.shape[0]),index=InferenceStruct.all_subjects)
		control_indicators.loc[ControlSubjects]=1.0

		freq_counts=InferenceStruct._compute_independent_counts(control_indicators)
		posterior_params=freq_counts+IndependentFreqPrior

		log_prob_pos=pd.Series(np.array([np.log(x[0]/np.sum(x)) for x in posterior_params.values]),index=freq_counts.index)
		log_prob_neg=pd.Series(np.array([np.log(x[1]/np.sum(x)) for x in posterior_params.values]),index=freq_counts.index)

		set_log_likelihoods = pd.Series(np.zeros(InferenceStruct.unique_symptom_sets.shape[0]),index=InferenceStruct.unique_symptom_sets.index)
		for unique_set_idx,symp_set in InferenceStruct.unique_symptom_sets.items():
			set_log_likelihoods.loc[unique_set_idx]=log_prob_pos.loc[InferenceStruct.oringal_index_map_to_hpo[symp_set]].sum()+log_prob_neg.loc[log_prob_neg.index.difference(InferenceStruct.oringal_index_map_to_hpo[symp_set])].sum()
		set_log_likelihoods.loc['NULL']=log_prob_neg.sum()
		return set_log_likelihoods

	def _UpdateIndependentBackground(self,CarrierIndicators,InferenceStruct,IndependentFreqPrior):
		control_indicators=1.0-CarrierIndicators
		freq_counts=InferenceStruct._compute_independent_counts(control_indicators)
		posterior_params=freq_counts+IndependentFreqPrior

		log_prob_pos=pd.Series(np.array([self._dirichlet_exp_logx(x)[0] for x in posterior_params.values]),index=freq_counts.index)
		log_prob_neg=pd.Series(np.array([self._dirichlet_exp_logx(x)[1] for x in posterior_params.values]),index=freq_counts.index)
		set_log_likelihoods = pd.Series(np.zeros(InferenceStruct.unique_symptom_sets.shape[0]),index=InferenceStruct.unique_symptom_sets.index)
		for unique_set_idx,symp_set in InferenceStruct.unique_symptom_sets.items():
			set_log_likelihoods.loc[unique_set_idx]=log_prob_pos.loc[InferenceStruct.oringal_index_map_to_hpo[symp_set]].sum()+log_prob_neg.loc[log_prob_neg.index.difference(InferenceStruct.oringal_index_map_to_hpo[symp_set])].sum()
		set_log_likelihoods.loc['NULL']=log_prob_neg.sum()
		return posterior_params,set_log_likelihoods


	def _UpdateArbitraryBackground(self,CarrierIndicators,InferenceStruct,SetPrior):
		control_indicators=1.0-CarrierIndicators
		freq_counts=InferenceStruct._compute_set_based_counts(control_indicators)
		posterior_params=freq_counts+SetPrior/InferenceStruct.num_unique_sets_total
		set_log_likelihoods=self._dirichlet_exp_logx(posterior_params)
		return posterior_params,set_log_likelihoods

	def _UpdatePenetranceIndicators(self,target_subjects,inference_struct,penetrance_posterior,symptom_set_posterior,background_model_log_probs):
		output_vector=pd.Series(np.zeros(len(target_subjects)),index=target_subjects)

		output_vector.loc[inference_struct.all_asymptomatic_cases.index.intersection(target_subjects)]=SMALL_FLOAT
		symptomatic_targets=inference_struct.all_symptomatic_cases.index.intersection(target_subjects)

		exp_log_set_prob=self._dirichlet_exp_logx(symptom_set_posterior)
		exp_log_pen_prob=self._dirichlet_exp_logx(penetrance_posterior)

		symptomatic_log_prob_penetrant=pd.Series(exp_log_set_prob.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_pen_prob[0]
		symptomatic_log_prob_nonpenetrant=pd.Series(background_model_log_probs.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_pen_prob[1]
		norm_consts=logsumexp(np.hstack((symptomatic_log_prob_penetrant.values.reshape(-1,1),symptomatic_log_prob_nonpenetrant.values.reshape(-1,1))),axis=-1)

		output_vector.loc[symptomatic_targets]=pd.Series(np.exp(symptomatic_log_prob_penetrant.values-norm_consts),index=symptomatic_targets)
		output_vector[output_vector<SMALL_FLOAT]=SMALL_FLOAT
		output_vector[output_vector>(1.0-SMALL_FLOAT)]=(1.0-SMALL_FLOAT)
		return output_vector

	def _UpdateCarrierIndicators(self,target_subjects,inference_struct,carrier_posterior,symptom_set_posterior,background_model_log_probs):
		output_vector=pd.Series(np.zeros(len(target_subjects)),index=target_subjects)

		output_vector.loc[inference_struct.all_asymptomatic_cases.index.intersection(target_subjects)]=SMALL_FLOAT
		symptomatic_targets=inference_struct.all_symptomatic_cases.index.intersection(target_subjects)

		disease_model_exp_log_set_prob=self._dirichlet_exp_logx(symptom_set_posterior)
		exp_log_carrier_freq=self._dirichlet_exp_logx(carrier_posterior)

		symptomatic_log_prob_carrier=pd.Series(disease_model_exp_log_set_prob.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_carrier_freq[0]
		symptomatic_log_prob_noncarrier=pd.Series(background_model_log_probs.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_carrier_freq[1]
		norm_consts=logsumexp(np.hstack((symptomatic_log_prob_carrier.values.reshape(-1,1),symptomatic_log_prob_noncarrier.values.reshape(-1,1))),axis=-1)

		output_vector.loc[symptomatic_targets]=pd.Series(np.exp(symptomatic_log_prob_carrier.values-norm_consts),index=symptomatic_targets)
		output_vector[output_vector<SMALL_FLOAT]=SMALL_FLOAT
		output_vector[output_vector>(1.0-SMALL_FLOAT)]=(1.0-SMALL_FLOAT)
		return output_vector


	def _UpdateSetBasedPosterior(self,penetrance_indicators,inference_struct,symptom_set_prior):
		all_indicators=pd.Series(np.zeros(len(inference_struct.all_subjects)),index=inference_struct.all_subjects)
		all_indicators.loc[penetrance_indicators.index]=penetrance_indicators

		set_freq_counts=inference_struct._compute_set_based_counts(all_indicators)
		posteriors=set_freq_counts.drop('NULL')+symptom_set_prior
		return posteriors

	def _UpdateCarrierFreqPosterior(self,carrier_indicators,carrier_freq_prior):
		carrier_freq_posterior=carrier_freq_prior.copy()
		carrier_freq_posterior[0]+=carrier_indicators.sum()
		carrier_freq_posterior[1]+=carrier_indicators.shape[0]-carrier_indicators.sum()
		return carrier_freq_posterior

	def _UpdatePenetrancePosterior(self,penetrance_indicators,penetrance_prior):
		penetrance_posterior=penetrance_prior.copy()
		penetrance_posterior[0]+=penetrance_indicators.sum()
		penetrance_posterior[1]+=penetrance_indicators.shape[0]-penetrance_indicators.sum()
		return penetrance_posterior

	def _PenetranceModelMargLike(self,penetrance_indicators,inference_struct,penetrance_posterior,symptom_set_posterior,penetrance_prior,symptom_set_prior,background_model):
		#Note: the latent variables include: 1) penentrance indicators 2) penetrance prior.
		exp_log_set_prob=self._dirichlet_exp_logx(symptom_set_posterior)
		exp_log_pen_prob=self._dirichlet_exp_logx(penetrance_posterior)

		#First, compute Exp[joint likelihood], first in symptomatic subjects
		symptomatic_targets=inference_struct.all_symptomatic_cases.index.intersection(penetrance_indicators.index)


		symptomatic_log_prob_penetrant=pd.Series(exp_log_set_prob.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_pen_prob[0]
		symptomatic_log_prob_nonpenetrant=pd.Series(background_model.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_pen_prob[1]


		ELBO=np.sum(penetrance_indicators.loc[symptomatic_targets]*symptomatic_log_prob_penetrant+(1.0-penetrance_indicators.loc[symptomatic_targets])*symptomatic_log_prob_nonpenetrant)

		#now asympomatics

		asymptomatic_targets=inference_struct.all_asymptomatic_cases.index.intersection(penetrance_indicators.index)
		ELBO+=asymptomatic_targets.shape[0]*(background_model.loc['NULL']+exp_log_pen_prob[1])

		#now add prior to ExpLogLike, in this case, it's the penetrance prob and symptom sets
		ELBO+=self._dirichlet_log_like(exp_log_pen_prob,penetrance_prior)

		ELBO+=self._dirichlet_log_like(exp_log_set_prob,symptom_set_prior)

		#now add entropy terms
		ELBO+=np.sum(-1.0*np.log(penetrance_indicators)*penetrance_indicators-np.log(1.0-penetrance_indicators)*(1.0-penetrance_indicators))
		ELBO+=self._dirichlet_entropy(penetrance_posterior)
		ELBO+=self._dirichlet_entropy(symptom_set_posterior)
		return ELBO




	def _CarrierModelMargLike(self,carrier_indicators,inference_struct,carrier_freq_posterior,symptom_set_posterior,background_posterior,background_symptom_set_log_prob,carrier_freq_prior,symptom_set_prior,background_model_prior,background_model_type):

		exp_log_set_prob=self._dirichlet_exp_logx(symptom_set_posterior)
		exp_log_carrier_prob=self._dirichlet_exp_logx(carrier_freq_posterior)
		exp_log_background_prob=background_symptom_set_log_prob

		#First, compute Exp[joint likelihood], first in symptomatic subjects
		symptomatic_targets=inference_struct.all_symptomatic_cases.index.intersection(carrier_indicators.index)


		symptomatic_log_prob_carrier=pd.Series(exp_log_set_prob.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_carrier_prob[0]
		symptomatic_log_prob_noncarrier=pd.Series(exp_log_background_prob.loc[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets].values].values,index=symptomatic_targets)+exp_log_carrier_prob[1]


		ELBO=np.sum(carrier_indicators.loc[symptomatic_targets]*symptomatic_log_prob_carrier+(1.0-carrier_indicators.loc[symptomatic_targets])*symptomatic_log_prob_noncarrier)

		#now asympomatics

		asymptomatic_targets=inference_struct.all_asymptomatic_cases.index.intersection(carrier_indicators.index)
		ELBO+=asymptomatic_targets.shape[0]*(background_symptom_set_log_prob.loc['NULL']+exp_log_carrier_prob[1])

		#now add prior to ExpLogLike, in this case, it's the carrier prob, disease symptom sets, and background symptom sets
		ELBO+=self._dirichlet_log_like(exp_log_carrier_prob,carrier_freq_prior)
		ELBO+=self._dirichlet_log_like(exp_log_set_prob,symptom_set_prior)
		if background_model_type=='Independent':
			ELBO+=np.sum([self._dirichlet_log_like(self._dirichlet_exp_logx(x),background_model_prior) for x in background_posterior.values])
		else:
			ELBO+=self._dirichlet_log_like(exp_log_background_prob,background_model_prior/inference_struct.num_unique_sets_total)

		#now add entropy terms
		ELBO+=np.sum(-1.0*np.log(carrier_indicators)*carrier_indicators-np.log(1.0-carrier_indicators)*(1.0-carrier_indicators))
		ELBO+=self._dirichlet_entropy(carrier_freq_posterior)
		ELBO+=self._dirichlet_entropy(symptom_set_posterior)
		if background_model_type=='Independent':
			ELBO+=np.sum([self._dirichlet_entropy(x) for x in background_posterior.values])
		else:
			ELBO+=self._dirichlet_entropy(background_posterior)
		return ELBO


	def _FitSpecificDisease(self,dis_id,target_subjects,inference_struct,penetrance_posterior,symptom_set_posterior,penetrance_prior,symptom_set_prior,background_model,max_iter,error_tol,verbose):

		#initialize penetrance indicators

		penetrance_indicators=self._UpdatePenetranceIndicators(target_subjects,inference_struct,penetrance_posterior,symptom_set_posterior,background_model)

		#adjust posteriors
		symptom_set_posterior=self._UpdateSetBasedPosterior(penetrance_indicators,inference_struct,symptom_set_prior)
		penetrance_posterior=self._UpdatePenetrancePosterior(penetrance_indicators,penetrance_prior)


		#initialize ELBO
		ELBO=self._PenetranceModelMargLike(penetrance_indicators,inference_struct,penetrance_posterior,symptom_set_posterior,penetrance_prior,symptom_set_prior,background_model)

		if verbose:
			print('Initialized Penetrance Model for {0:s}. Inital Log-Marginal Likelihood (Lower-bound): {1:f}.'.format(dis_id,ELBO))

		prior_ELBO=ELBO

		for fit_iter in range(max_iter):
			penetrance_indicators=self._UpdatePenetranceIndicators(target_subjects,inference_struct,penetrance_posterior,symptom_set_posterior,background_model)
			symptom_set_posterior=self._UpdateSetBasedPosterior(penetrance_indicators,inference_struct,symptom_set_prior)
			penetrance_posterior=self._UpdatePenetrancePosterior(penetrance_indicators,penetrance_prior)
			ELBO=self._PenetranceModelMargLike(penetrance_indicators,inference_struct,penetrance_posterior,symptom_set_posterior,penetrance_prior,symptom_set_prior,background_model)

			error=(ELBO-prior_ELBO)/np.abs(ELBO)
			if error<=error_tol:
				if verbose:
					print('Inference complete. Final Log-Marginal Likelihood (Error): {0:f} ({1:e}).'.format(ELBO,error))
				break
			else:
				prior_ELBO=ELBO
				if verbose:
					print('Completed {0:d} iterations. Current Log-Marginal Likelihood (Error): {1:f} ({2:e})'.format(fit_iter+1,ELBO,error))

		return penetrance_indicators,penetrance_posterior,symptom_set_posterior,ELBO


	def FitFullPenetranceModel(self,DiseaseSpecificSubjects,DiseaseSpecificControls,DiseaseSpecificPriorInformation,UpdatePrior=True,verbose=False,CoupleStrengths=False,max_iter=50,error_tol=1e-8,**model_kwargs):

		"""This function fits the probabilistic SymptomSetModel in a semi-supervised fashion, with the ultimate goal of estimating the subject-specific penetrances while learning a hierarchical prior distribution over symptom set frequencies. Inference is conducted using a Variational Bayes framework. The function returns penetrance predictions for all the rare disease cases along with estimates for the symptom set posteriors and priors. 
		
		Args:
		    DiseaseSpecificSubjects (dictionary of lists): Each entry in the diciontary contains the list of variant carriers for a specific disease, with the key providing a unique Disease ID

		    DiseaseSpecificControls (dictionary of lists): Each entry in the diciontary contains the list of controls used for the disease-specific penetrance estimation, with the key providing a unique Disease ID

		    DiseaseSpecificPriorInformation (dictionary of pd.DataFrame's): Each entry in the diciontary contains a pandas.DataFrame with two columns and S rows, where S denotes the number of symptoms annotated to each disease. The two columns contain: 1) the annotation probability and 2) the symptom-set frequency information. The latter must either be a vector of length 5, which indicates the probability mass assigned to an ordinal set of frequecies ('VR', 'OC','F','VF', 'O'; see HPO for details), or a tuple containing the following information: (number of cases with symptom, total number of cases)

		    UpdatePrior (bool, optional): Indicates whether the hierarchical prior will be updated during model inference. Default is True.

		    verbose (bool, optional): Indicates whether to print convergence informtion during model inference. Used for debugging. Default is False.

		    CoupleStrengths (bool, optional): Indicates whether to couple prior strength parameters across diseases. Default is False.

		    max_iter (int, optional): Maximum number of iterations used to fit model. Default is 50 (models typically converge in <10 iterations)

		    error_tol (float, optional): Error tolerance to assess convergence. Default is 1e-8.

		    **model_kwargs: Additional optional model parameters. These include:
				'BackgroundModel': Must be either ['Independent','Arbitrary']. Default is 'Arbitrary', which is equivalent to a generic symptom set model. 
				'PenetrancePrior': Parameters specifying the prior distributions over disease penetrance. Must be list-like with length 2. Default is [0.5,0.5].
				'IndependentFreqPrior': Iterable of length 2, which specifies the prior distribution for an Independent Frequency background prior. Default is [0.5,0.5].
				'ArbitraryFreqPriorParam': ArbitraryFreqPriorParam defines the concentration of a symmetric Dirichlet distribution (alpha), where alpha=ArbitraryFreqPriorParam/N_dim. Default is 1.0, which is equivalent to Jeffrey's prior for the symmetric Dirichlet distribution.
				'InitialPriorInformationParameters': InitPriorInformationParameters must be a dictionary of floats that defines the initial parameters that specify the heirarchical prior model for the symptom set frequencies. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam. Note, the strength parameters will vary across diseases, but only a single initial value is required. Default is {'Strength':1.0,'Smoothing':0.99,'LogAnnotRateParam':0.5,'LogSymptomFreqParam':0.5}.
		
		Returns:
			Results Dictionary: Dictionary of results with the following key-value pairs:
				'PenetrancePosteriors': Dictionary of pd.Series, one for each disease. Each entry contains an array of length 2, which contains the parameters that define the variational posterior over penetrance for that disease.
				'SubjectLevelPenetranceProbabilities': Dictionary of pd.Series, one for each disease. Each entry contains the subject-level penetrance estimates for the carriers specific to that disease.
				'SymptomSetPosteriors': Dictionary of pd.Series, one for each disease. Each entry contains the posterior distribution over symptom sets for that disease. 
				'HierarchicalPriorParameters': Dictionary containing the parameters that define the hierarchical prior. 

		"""
		assert len(set(DiseaseSpecificSubjects.keys()).symmetric_difference(DiseaseSpecificControls.keys()))==0,"The dictionary of rare disease cases and controls have differing diseases."
		assert len(set(DiseaseSpecificSubjects.keys()).symmetric_difference(DiseaseSpecificPriorInformation.keys()))==0,"The dictionary of rare disease cases and prior information tables have differing diseases."
		for dis_id in list(DiseaseSpecificSubjects.keys()):
			assert len(set(DiseaseSpecificSubjects[dis_id]).intersection(DiseaseSpecificControls[dis_id]))==0,"Set of RareDiseaseSubjects for disease {0:s} is not disjoint from the ControlSubjects".format(dis_id)
			assert isinstance(DiseaseSpecificPriorInformation[dis_id], pd.DataFrame),"Prior information for each disease must be a pandas.DataFrame."
			assert len(DiseaseSpecificPriorInformation[dis_id].columns)==2,"Each entry in DiseaseSpecificPriorInformation must contain at least two columns. The first must contain the probability that the symptom is correctly annotated, and the second should specify a prior distribution over symptom frequency."
			if len(DiseaseSpecificPriorInformation[dis_id].index.difference(self.HPOIndexMap.index)):
				if verbose:
					print("Symptoms {0:s} for disease/gene {1:s} were not observed in the dataset. Dropping them from the analysis.".format(','.join(DiseaseSpecificPriorInformation[dis_id].index.difference(self.HPOIndexMap.index)),dis_id))

				observed_symptoms=self.HPOIndexMap.index.intersection(DiseaseSpecificPriorInformation[dis_id].index)
				if len(observed_symptoms):
					DiseaseSpecificPriorInformation[dis_id]=DiseaseSpecificPriorInformation[dis_id].loc[observed_symptoms]
				else:
					print('Warning: Diagnostic dataset shares no overlap with the symptoms annotated for disease {0:s}. Dropping from analysis.'.format(dis_id))
					DiseaseSpecificPriorInformation.pop(dis_id)
					DiseaseSpecificSubjects.pop(dis_id)
					DiseaseSpecificControls.pop(dis_id)

		hyperparameters={}

		if 'BackgroundModel' in model_kwargs.keys():
			assert model_kwargs['BackgroundModel'] in ['Independent','Arbitrary'],'Only two background models available: Independent (assumes symptoms occur independently) and Arbitrary (estimates a probability rate for all observed symptom sets).'
			hyperparameters['BackgroundModel']=model_kwargs['BackgroundModel']
		else:
			hyperparameters['BackgroundModel']='Arbitrary'

		if 'PenetrancePrior' in model_kwargs.keys():
			assert len(model_kwargs['PenetrancePrior'])==2, "Penetrance prior distribution is expected to be an iterable of length 2. It specifies the beta prior distribution over rare variant penentrance. Default is [0.5,0.5]."
			assert (model_kwargs['PenetrancePrior'][0]>0.0) and (model_kwargs['PenetrancePrior'][1]>0.0), "Both penetrance prior parameters must be > 0.0"
			hyperparameters['PenetrancePrior']=np.array(model_kwargs['PenetrancePrior'])
		else:
			hyperparameters['PenetrancePrior']=np.array([0.5,0.5])

		if 'IndependentFreqPrior' in model_kwargs.keys():
			assert len(model_kwargs['IndependentFreqPrior'])==2, "Independent frequenqy prior distribution is expected to be an iterable of length 2. It specifies the beta prior distribution over symptom prevalence in general population. Default is [0.5,0.5]."
			assert (model_kwargs['IndependentFreqPrior'][0]>0.0) and (model_kwargs['IndependentFreqPrior'][1]>0.0), "Both independent frequency prior parameters must be > 0.0"
			hyperparameters['IndependentFreqPrior']=np.array(model_kwargs['IndependentFreqPrior'])	
		else:
			hyperparameters['IndependentFreqPrior']=np.array([0.5,0.5])

		if 'ArbitraryFreqPriorParam' in model_kwargs.keys():
			assert isinstance(model_kwargs['ArbitraryFreqPriorParam'],float),"ArbitraryFreqPriorParam defines the concentration of a symmetric Dirichlet distribution (alpha), where alpha=ArbitraryFreqPriorParam/N_dim. Default is 1.0, which is equivalent to Jeffrey's prior for the symmetric Dirichlet distribution. "
			assert (model_kwargs['ArbitraryFreqPriorParam']>0.0),"ArbitraryFreqPriorParam must be greater than zero."
			hyperparameters['ArbitraryFreqPriorParam']=model_kwargs['ArbitraryFreqPriorParam']
		else:
			hyperparameters['ArbitraryFreqPriorParam']=1.0


		if 'InitialPriorInformationParameters' in model_kwargs.keys():
			assert isinstance(model_kwargs['InitialPriorInformationParameters'],dict),"InitPriorInformationParameters must be a dictionary that defines the initial parameters that specify the heirarchical prior model for symptom set frequency. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam. Note, the strength parameters will vary across diseases, but only a single initial value is required."
			assert set(model_kwargs['InitialPriorInformationParameters'].keys()).symmetric_difference(['Strength', 'Smoothing', 'LogAnnotRateParam', 'LogSymptomFreqParam'])==set(),"InitPriorInformationParameters must be a dictionary that defines the initial parameters that specify the heirarchical prior model for symptom set frequency. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam. Note, the strength parameters will vary across diseases, but only a single initial value is required."
			assert isinstance(model_kwargs['InitialPriorInformationParameters']['Strength'],float) and (model_kwargs['InitialPriorInformationParameters']['Strength']>0.0),"Initial prior strength must be a float >0.0."
			assert isinstance(model_kwargs['InitialPriorInformationParameters']['Smoothing'],float) and (model_kwargs['InitialPriorInformationParameters']['Smoothing']>0.0) and (model_kwargs['InitialPriorInformationParameters']['Smoothing']<1.0),"Initial prior smoothing must be a float in (0.0,1.0)."
			assert isinstance(model_kwargs['InitialPriorInformationParameters']['LogAnnotRateParam'],float) and (model_kwargs['InitialPriorInformationParameters']['LogAnnotRateParam']>0.0) and (model_kwargs['InitialPriorInformationParameters']['LogAnnotRateParam']<1.0),"Initial LogAnnotRateParam must be a float in (0.0,1.0)."
			assert isinstance(model_kwargs['InitialPriorInformationParameters']['LogSymptomFreqParam'],float) and (model_kwargs['InitialPriorInformationParameters']['LogSymptomFreqParam']>0.0) and (model_kwargs['InitialPriorInformationParameters']['LogSymptomFreqParam']<1.0),"Initial LogSymptomFreqParam must be a float in (0.0,1.0)."		

			hyperparameters['InitialPriorInformationParameters']=model_kwargs['InitialPriorInformationParameters']
		else:
			hyperparameters['InitialPriorInformationParameters']={'Strength':1.0,'Smoothing':0.99,'LogAnnotRateParam':0.5,'LogSymptomFreqParam':0.5}

		hyperparameters['StrengthCoupled']=CoupleStrengths


		disease_specific_inference_structures={}
		print('Step 1: Computing disease-specific data structures required for inference...')
		for DisId in tqdm.tqdm(DiseaseSpecificSubjects.keys()):
			combined_subject_list=list(DiseaseSpecificSubjects[DisId])+list(DiseaseSpecificControls[DisId])
			disease_filtered_sparse_matrix = self.SparseSymptomMatrix[self.SubjectIndexMap.loc[combined_subject_list],:]
			disease_filtered_subject_index = pd.Series(np.arange(len(combined_subject_list)),index=combined_subject_list)
			disease_filtered_hpo_map = self.HPOIndexMap.loc[DiseaseSpecificPriorInformation[DisId].index]

			disease_specific_inference_structures[DisId]=InferenceDataStruct(disease_filtered_sparse_matrix,disease_filtered_subject_index,disease_filtered_hpo_map)

		disease_specific_background_models={}
		print('Step 2: Computing disease-specific background models...')
		for DisId in tqdm.tqdm(DiseaseSpecificControls.keys()):
			if hyperparameters['BackgroundModel']=='Independent':
				disease_specific_background_models[DisId]=self._null_independent_model(DiseaseSpecificControls[DisId],disease_specific_inference_structures[DisId],hyperparameters['IndependentFreqPrior'])
			else:
				disease_specific_background_models[DisId]=self._null_arbitrary_model(DiseaseSpecificControls[DisId],disease_specific_inference_structures[DisId],hyperparameters['ArbitraryFreqPriorParam'])

		print('Step 3: Building heirarchical prior...')
		hierarchical_prior=DirichletSymptomPrior(self.HPOIndexMap,DiseaseSpecificPriorInformation,disease_specific_inference_structures,init_log_symptom_freq_param=hyperparameters['InitialPriorInformationParameters']['LogSymptomFreqParam'],init_log_annot_rate_param=hyperparameters['InitialPriorInformationParameters']['LogAnnotRateParam'],init_smoothing=hyperparameters['InitialPriorInformationParameters']['Smoothing'],init_strength=hyperparameters['InitialPriorInformationParameters']['Strength'],couple_strengths=CoupleStrengths,update_strength=True,update_smoothing=True,update_param_coeff=True)


		#initalize model parameters
		penetrance_parameters=pd.Series([hyperparameters['PenetrancePrior'].copy() for x in range(len(DiseaseSpecificPriorInformation))],index=list(DiseaseSpecificPriorInformation.keys()))
		penetrance_indicators={}
		symptoms_set_posteriors={}
		for dis_id in DiseaseSpecificSubjects.keys():
			penetrance_indicators[dis_id]=pd.Series(np.zeros(len(DiseaseSpecificSubjects[dis_id])),index=DiseaseSpecificSubjects[dis_id])
			symptoms_set_posteriors[dis_id]=hierarchical_prior.disease_specific_dirichlet_params[dis_id].copy()
		marginal_likelihoods=pd.Series(np.zeros(len(DiseaseSpecificPriorInformation)),index=list(DiseaseSpecificPriorInformation.keys()))


		print('Step 4: Optimizing model parameters...')
		symptom_set_counts={}
		print('Initiating disease-specific penetrance models...')
		for dis_id in tqdm.tqdm(DiseaseSpecificSubjects.keys()):
			dis_specific_penetrance_indicators,dis_specific_penetrance_posterior,dis_specific_symptom_set_posterior,ELBO=self._FitSpecificDisease(dis_id,DiseaseSpecificSubjects[dis_id],disease_specific_inference_structures[dis_id],penetrance_parameters[dis_id],symptoms_set_posteriors[dis_id],hyperparameters['PenetrancePrior'],hierarchical_prior.disease_specific_dirichlet_params[dis_id],disease_specific_background_models[dis_id],max_iter,error_tol,verbose)
			penetrance_parameters.loc[dis_id]=dis_specific_penetrance_posterior
			penetrance_indicators[dis_id]=dis_specific_penetrance_indicators.copy()
			symptoms_set_posteriors[dis_id]=dis_specific_symptom_set_posterior.copy()
			marginal_likelihoods.loc[dis_id]=ELBO
			symptom_set_counts[dis_id]=symptoms_set_posteriors[dis_id]-hierarchical_prior.disease_specific_dirichlet_params[dis_id]

		print('Initiating hierarchical prior...')
		hierarchical_prior.UpdatePriorParams(symptom_set_counts,verbose=verbose,error_tol=error_tol)

		#adjust marginal likelihood
		for dis_id in DiseaseSpecificSubjects.keys():
			symptoms_set_posteriors[dis_id]=symptom_set_counts[dis_id]+hierarchical_prior.disease_specific_dirichlet_params[dis_id]
			marginal_likelihoods.loc[dis_id]=self._PenetranceModelMargLike(penetrance_indicators[dis_id],disease_specific_inference_structures[dis_id],penetrance_parameters.loc[dis_id],symptoms_set_posteriors[dis_id],hyperparameters['PenetrancePrior'],hierarchical_prior.disease_specific_dirichlet_params[dis_id],disease_specific_background_models[dis_id])
		dirichlet_loss,regularizer_loss,global_loss=hierarchical_prior.ReturnLossComponents(symptom_set_counts)
		GlobalLoss=marginal_likelihoods.sum()+regularizer_loss

		print('Completed iteration {0:d} of model fitting. Global loss: {1:f}'.format(1,GlobalLoss))
		priorGlobalLoss=GlobalLoss

		for fit_iter in range(1,max_iter):
			print('Updating disease-specific penetrance models...')
			symptom_set_counts={}
			for dis_id in tqdm.tqdm(DiseaseSpecificSubjects.keys()):
				dis_specific_penetrance_indicators,dis_specific_penetrance_posterior,dis_specific_symptom_set_posterior,ELBO=self._FitSpecificDisease(dis_id,DiseaseSpecificSubjects[dis_id],disease_specific_inference_structures[dis_id],penetrance_parameters[dis_id],symptoms_set_posteriors[dis_id],hyperparameters['PenetrancePrior'],hierarchical_prior.disease_specific_dirichlet_params[dis_id],disease_specific_background_models[dis_id],max_iter,error_tol,verbose)
				penetrance_parameters.loc[dis_id]=dis_specific_penetrance_posterior
				penetrance_indicators[dis_id]=dis_specific_penetrance_indicators.copy()
				symptoms_set_posteriors[dis_id]=dis_specific_symptom_set_posterior.copy()
				marginal_likelihoods.loc[dis_id]=ELBO
				symptom_set_counts[dis_id]=symptoms_set_posteriors[dis_id]-hierarchical_prior.disease_specific_dirichlet_params[dis_id]

			print('Updating hierarchical prior...')
			hierarchical_prior.UpdatePriorParams(symptom_set_counts,verbose=verbose,error_tol=error_tol)

			#adjust marginal likelihood
			for dis_id in DiseaseSpecificSubjects.keys():
				symptoms_set_posteriors[dis_id]=symptom_set_counts[dis_id]+hierarchical_prior.disease_specific_dirichlet_params[dis_id]
				marginal_likelihoods.loc[dis_id]=self._PenetranceModelMargLike(penetrance_indicators[dis_id],disease_specific_inference_structures[dis_id],penetrance_parameters.loc[dis_id],symptoms_set_posteriors[dis_id],hyperparameters['PenetrancePrior'],hierarchical_prior.disease_specific_dirichlet_params[dis_id],disease_specific_background_models[dis_id])
			dirichlet_loss,regularizer_loss,global_loss=hierarchical_prior.ReturnLossComponents(symptom_set_counts)
			GlobalLoss=marginal_likelihoods.sum()+regularizer_loss

			error=(GlobalLoss-priorGlobalLoss)/np.abs(GlobalLoss)
			if error<=error_tol:
				print('Inference complete. Final Global Loss (Error): {0:f} ({1:e}).'.format(GlobalLoss,error))
				break
			else:
				priorGlobalLoss=GlobalLoss
				print('Completed {0:d} iterations. Current Log-Marginal Likelihood (Error): {1:f} ({2:e})'.format(fit_iter+1,GlobalLoss,error))

		#post-processing
		results_dictionary={}
		results_dictionary['PenetrancePosteriors']=penetrance_parameters
		results_dictionary['SubjectLevelPenetranceProbabilities']=penetrance_indicators
		results_dictionary['SymptomSetPosteriors']={}
		for dis_id in DiseaseSpecificPriorInformation.keys():
			weights=[]
			index=[]
			for set_idx,posterior_weight in symptoms_set_posteriors[dis_id].items():
				weights+=[posterior_weight]
				index+=[';'.join([disease_specific_inference_structures[dis_id].oringal_index_map_to_hpo.loc[x] for x in disease_specific_inference_structures[dis_id].unique_symptom_sets.loc[set_idx]])]
			results_dictionary['SymptomSetPosteriors'][dis_id]=pd.Series(weights,index=index)

		results_dictionary['HierarchicalPriorParameters']=hierarchical_prior.parameters
		return results_dictionary





	def PredictPenetrance_SingleDisease(self,RareDiseaseSubjects,ControlSubjects,HPOPriorInfo,PriorInformationParameters={'Strength':1.0,'Smoothing':0.99,'LogAnnotRateParam':0.5,'LogSymptomFreqParam':0.5},max_iter=50,error_tol=1e-8,verbose=False,**model_kwargs):

		"""This function fits the probabilistic SymptomSetModel in a semi-supervised fashion to a single disease. Inference is conducted using a Variational Bayes framework. The function returns penetrance predictions for all the rare disease cases. Because only a single disease is analyzed, the hierarchical prior cannot be optimized.  
		
		Args:
		    RareDiseaseSubjects (list-like): The list of rare disease variant carriers.

		    ControlSubjects (list-like): The list of control subjects.

		    HPOPriorInfo (pd.DataFrame): A pandas.DataFrame with two columns and S rows, where S denotes the number of symptoms annotated to the disease. The two columns contain: 1) the annotation probability and 2) the symptom-set frequency information. The latter must either be a vector of length 5, which indicates the probability mass assigned to an ordinal set of frequecies ('VR', 'OC','F','VF', 'O'; see HPO for details), or a tuple containing the following information (number of cases with symptom, total number of cases)

		    PriorInformationParameters (dict, optional): PriorInformationParameters must be a dictionary that defines the the parameters that specify the heirarchical prior model for symptom set frequency. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam.

		    max_iter (int, optional): Maximum number of iterations used to fit model. Default is 50 (typically converges in <10 iterations)

		    error_tol (float, optional): Error tolerance to assess convergence. Default is 1e-8.

		    verbose (bool, optional): Indicates whether to print convergence informtion during model inference. Used for debugging. Default is False.

		    **model_kwargs: Additional optional model parameters. These include:
				'BackgroundModel': Must be either ['Independent','Arbitrary']. Default is 'Arbitrary', which is equivalent to a generic symptom set model. 
				'PenetrancePrior': Parameters specifying the prior distribution over disease penetrance, provided as iterable with length 2. Default is [0.5,0.5].
				'IndependentFreqPrior': Iterable of length 2, which specifies the prior distribution for an Independent frequency background prior. Default is [0.5,0.5].
				'ArbitraryFreqPriorParam': ArbitraryFreqPriorParam defines the concentration of a symmetric Dirichlet distribution (alpha), where alpha=ArbitraryFreqPriorParam/N_dim. Default is 1.0, which is equivalent to Jeffrey's prior for the symmetric Dirichlet distribution.
		
		Returns:
		    Results Dictionary: Dictionary of results with the following key-value pairs:
				'PenetrancePosterior': An array of length 2, which contains the parameters that define the variational posterior over penetrance for the disease.
				'SubjectLevelPenetranceProbabilities': pd.Series that contains the subject-level penetrance estimates for the carriers specific to the disease.
				'SymptomSetPosteriors': pd.Series that contains the posterior distribution over symptom sets for the disease. 
				'HierarchicalPriorParameters': Dictionary containing the parameters that define the hierarchical prior. 

		"""
		assert len(set(RareDiseaseSubjects).intersection(ControlSubjects))==0,"Set of RareDiseaseSubjects is not disjoint from the ControlSubjects"
		assert isinstance(HPOPriorInfo, pd.DataFrame),"Prior information for each disease must be a pandas.DataFrame."
		assert len(HPOPriorInfo.columns)==2,"HPOPriorInfo must contain at least two columns. The first must contain the probability that the symptom is correctly annotated, and the second should specify a prior distribution over symptom frequency."
		if len(HPOPriorInfo.index.difference(self.HPOIndexMap.index)):
			if verbose:
				print("Symptoms {0:s} were not observed in the dataset. Dropping them from the analysis.".format(','.join(HPOPriorInfo.index.difference(self.HPOIndexMap.index))))

			observed_symptoms=self.HPOIndexMap.index.intersection(HPOPriorInfo.index)
			if len(observed_symptoms):
				HPOPriorInfo=HPOPriorInfo.loc[observed_symptoms]
			else:
				raise ValueError("No rare disease symptoms were observed in the dataset. Unable to fit penentrance model.")
		hyperparameters={}

		if 'BackgroundModel' in model_kwargs.keys():
			assert model_kwargs['BackgroundModel'] in ['Independent','Arbitrary'],'Only two background models available: Independent (assumes symptoms occur independently) and Arbitrary (estimates a probability rate for all observed symptom sets).'
			hyperparameters['BackgroundModel']=model_kwargs['BackgroundModel']
		else:
			hyperparameters['BackgroundModel']='Arbitrary'

		if 'PenetrancePrior' in model_kwargs.keys():
			assert len(model_kwargs['PenetrancePrior'])==2, "Penetrance prior distribution is expected to be an iterable of length 2. It specifies the beta prior distribution over rare variant penentrance. Default is [0.5,0.5]."
			assert (model_kwargs['PenetrancePrior'][0]>0.0) and (model_kwargs['PenetrancePrior'][1]>0.0), "Both penetrance prior parameters must be > 0.0"
			hyperparameters['PenetrancePrior']=np.array(model_kwargs['PenetrancePrior'])
		else:
			hyperparameters['PenetrancePrior']=np.array([0.5,0.5])

		if 'IndependentFreqPrior' in model_kwargs.keys():
			assert len(model_kwargs['IndependentFreqPrior'])==2, "Independent frequenqy prior distribution is expected to be an iterable of length 2. It specifies the beta prior distribution over symptom prevalence in general population. Default is [0.5,0.5]."
			assert (model_kwargs['IndependentFreqPrior'][0]>0.0) and (model_kwargs['IndependentFreqPrior'][1]>0.0), "Both independent frequency prior parameters must be > 0.0"
			hyperparameters['IndependentFreqPrior']=np.array(model_kwargs['IndependentFreqPrior'])	
		else:
			hyperparameters['IndependentFreqPrior']=np.array([0.5,0.5])

		if 'ArbitraryFreqPriorParam' in model_kwargs.keys():
			assert isinstance(model_kwargs['ArbitraryFreqPriorParam'],float),"ArbitraryFreqPriorParam defines the concentration of a symmetric Dirichlet distribution (alpha), where alpha=ArbitraryFreqPriorParam/N_dim. Default is 1.0, which is equivalent to Jeffrey's prior for the symmetric Dirichlet distribution. "
			assert (model_kwargs['ArbitraryFreqPriorParam']>0.0),"ArbitraryFreqPriorParam must be greater than zero."
			hyperparameters['ArbitraryFreqPriorParam']=model_kwargs['ArbitraryFreqPriorParam']
		else:
			hyperparameters['ArbitraryFreqPriorParam']=1.0

		assert isinstance(PriorInformationParameters,dict),"PriorInformationParameters must be a dictionary of prior-specific parameters."
		assert set(PriorInformationParameters.keys()).symmetric_difference(['Strength', 'Smoothing', 'LogAnnotRateParam', 'LogSymptomFreqParam'])==set(),"PriorInformationParameters must be a dictionary that defines the the parameters that specify the heirarchical prior model for symptom set frequency. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam."
		assert isinstance(PriorInformationParameters['Strength'],float) and (PriorInformationParameters['Strength']>0.0),"Initial prior strength must be a float >0.0."
		assert isinstance(PriorInformationParameters['Smoothing'],float) and (PriorInformationParameters['Smoothing']>0.0) and (PriorInformationParameters['Smoothing']<1.0),"Initial prior smoothing must be a float in (0.0,1.0)."
		assert isinstance(PriorInformationParameters['LogAnnotRateParam'],float) and (PriorInformationParameters['LogAnnotRateParam']>0.0) and (PriorInformationParameters['LogAnnotRateParam']<1.0),"Initial LogAnnotRateParam must be a float in (0.0,1.0)."
		assert isinstance(PriorInformationParameters['LogSymptomFreqParam'],float) and (PriorInformationParameters['LogSymptomFreqParam']>0.0) and (PriorInformationParameters['LogSymptomFreqParam']<1.0),"Initial LogSymptomFreqParam must be a float in (0.0,1.0)."		

		print('Step 1: Building data structures required for inference...')
		combined_subject_list=list(RareDiseaseSubjects)+list(ControlSubjects)
		disease_filtered_sparse_matrix = self.SparseSymptomMatrix[self.SubjectIndexMap.loc[combined_subject_list],:]
		disease_filtered_subject_index = pd.Series(np.arange(len(combined_subject_list)),index=combined_subject_list)
		disease_filtered_hpo_map = self.HPOIndexMap.loc[HPOPriorInfo.index]
		inference_data_structure=InferenceDataStruct(disease_filtered_sparse_matrix,disease_filtered_subject_index,disease_filtered_hpo_map)

		print('Step 2: Computing disease-specific background models...')
		if hyperparameters['BackgroundModel']=='Independent':
			background_model=self._null_independent_model(ControlSubjects,inference_data_structure,hyperparameters['IndependentFreqPrior'])
		else:
			background_model=self._null_arbitrary_model(ControlSubjects,inference_data_structure,hyperparameters['ArbitraryFreqPriorParam'])

		print('Step 3: Building heirarchical prior...')
		hierarchical_prior=DirichletSymptomPrior(self.HPOIndexMap,{'NA':HPOPriorInfo},{'NA':inference_data_structure},init_log_symptom_freq_param=PriorInformationParameters['LogSymptomFreqParam'],init_log_annot_rate_param=PriorInformationParameters['LogAnnotRateParam'],init_smoothing=PriorInformationParameters['Smoothing'],init_strength=PriorInformationParameters['Strength'])
		


		print('Step 4: Optimizing model parameters...')
		#initalize model parameters
		symptom_set_prior=hierarchical_prior.disease_specific_dirichlet_params['NA']
		penetrance_parameters=hyperparameters['PenetrancePrior'].copy()
		penetrance_indicators=pd.Series(np.zeros(len(RareDiseaseSubjects)),index=RareDiseaseSubjects)
		symptoms_set_posteriors=symptom_set_prior.copy()

		penetrance_indicators,penetrance_posterior,symptom_set_posterior,ELBO=self._FitSpecificDisease('NA',RareDiseaseSubjects,inference_data_structure,penetrance_parameters,symptoms_set_posteriors,hyperparameters['PenetrancePrior'],symptom_set_prior,background_model,max_iter,error_tol,verbose)

		results_dictionary={}
		results_dictionary['PenetrancePosterior']=penetrance_posterior
		results_dictionary['SubjectLevelPenetranceProbabilities']=penetrance_indicators
		weights=[]
		index=[]
		for set_idx,posterior_weight in symptoms_set_posteriors.items():
			weights+=[posterior_weight]
			index+=[';'.join([inference_data_structure.oringal_index_map_to_hpo.loc[x] for x in inference_data_structure.unique_symptom_sets.loc[set_idx]])]
		results_dictionary['SymptomSetPosteriors']=pd.Series(weights,index=index)
		results_dictionary['HierarchicalPriorParameters']=hierarchical_prior.parameters
		return results_dictionary





	def PredictSymptomaticCarrierStatus(self,TargetSubjectIndex,HPOPriorInfo,CarrierFrequencyPriorInterval,CI=0.99,PriorInformationParameters={'Strength':1.0,'Smoothing':0.99,'LogAnnotRateParam':0.5,'LogSymptomFreqParam':0.5},max_iter=50,error_tol=1e-8,verbose=False,**model_kwargs):

		"""Assuming complete penetrance, this function predicts the carrier status for a set of target individuals based on their diagnosed symptoms. Note, even after imposing strong prior information regarding prevelence, it is difficult to simultaneously estimate penetrance and carrier status simultaneously, as carrier status->1 as penetrance->0. Therefore, penetrance is fixed at 1.0. 
		
		Args:
		    TargetSubjectIndex (list-like): The list of individuals to analyze.

		    HPOPriorInfo (pd.DataFrame): A pandas.DataFrame with two columns and S rows, where S denotes the number of symptoms annotated to the disease. The two columns contain: 1) the annotation probability and 2) the symptom-set frequency information. The latter must either be a vector of length 5, which indicates the probability mass assigned to an ordinal set of frequecies ('VR', 'OC','F','VF', 'O'; see HPO for details), or a tuple containing the following information (number of cases with symptom, total number of cases).

		    CarrierFrequencyPriorInterval (list-like, length 2): A list of two floats that define the upper and lower bounds for the prevalence credibile interval. Both values must be less than 0.0, with the first number less than the second. 

		    CI (float, optional): Float <1.0 that specifies the credible interval for the prevelence. Default is 0.99.

		    PriorInformationParameters (dict, optional): PriorInformationParameters must be a dictionary that defines the the parameters that specify the heirarchical prior model for symptom set frequency. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam.

		    max_iter (int, optional): Maximum number of iterations used to fit model. Default is 50 (typically converges in <10 iterations)

		    error_tol (float, optional): Error tolerance to assess convergence. Default is 1e-8.

		    verbose (bool, optional): Indicates whether to print convergence informtion during model inference. Used for debugging. Default is False.

		    **model_kwargs: Additional optional model parameters. These include:
				'BackgroundModel': Must be either ['Independent','Arbitrary']. Default is arbitrary, which is equivalent to a generic symptom set model. 
				'PenetrancePrior': Parameters specifying prior distribution over disease penetrance, provided as an iterable with 2 elements. Default is [0.5,0.5].
				'IndependentFreqPrior': Iterable of length 2, which specifies the prior distribution for an Independent Frequency background prior. Default is [0.5,0.5].
				'ArbitraryFreqPriorParam': ArbitraryFreqPriorParam defines the concentration of a symmetric Dirichlet distribution (alpha), where alpha=ArbitraryFreqPriorParam/N_dim. Default is 1.0, which is equivalent to Jeffrey's prior for the symmetric Dirichlet distribution.
		
	    Results Dictionary: Dictionary of results with the following key-value pairs:
			'CarrierFrequencyPosterior': A length 2 array, which contains the parameters that define the variational posterior over the carrier frequency within the target cohort.
			'SubjectLevelCarrierProbabilities': pd.Series that contains the subject-level carrier status estimates for the subjects in the target index.
			'SymptomSetPosteriors': pd.Series that contains the posterior distribution over symptom sets for the disease. 
			'HierarchicalPriorParameters': Dictionary containing the parameters that define the hierarchical prior. 

		"""
		assert isinstance(HPOPriorInfo, pd.DataFrame),"Prior information for each disease must be a pandas.DataFrame."
		assert len(HPOPriorInfo.columns)==2,"HPOPriorInfo must contain at least two columns. The first must contain the probability that the symptom is correctly annotated, and the second should specify a prior distribution over symptom frequency."
		if len(HPOPriorInfo.index.difference(self.HPOIndexMap.index)):
			if verbose:
				print("Symptoms {0:s} were not observed in the dataset. Dropping them from the analysis.".format(','.join(HPOPriorInfo.index.difference(self.HPOIndexMap.index))))

			observed_symptoms=self.HPOIndexMap.index.intersection(HPOPriorInfo.index)
			if len(observed_symptoms):
				HPOPriorInfo=HPOPriorInfo.loc[observed_symptoms]
			else:
				raise ValueError("No rare disease symptoms were observed in the dataset. Unable to fit penentrance model.")
		hyperparameters={}

		if 'BackgroundModel' in model_kwargs.keys():
			assert model_kwargs['BackgroundModel'] in ['Independent','Arbitrary'],'Only two background models available: Independent (assumes symptoms occur independently) and Arbitrary (estimates a probability rate for all observed symptom sets).'
			hyperparameters['BackgroundModel']=model_kwargs['BackgroundModel']
		else:
			hyperparameters['BackgroundModel']='Arbitrary'


		if 'IndependentFreqPrior' in model_kwargs.keys():
			assert len(model_kwargs['IndependentFreqPrior'])==2, "Independent frequenqy prior distribution is expected to be an iterable of length 2. It specifies the beta prior distribution over symptom prevalence in general population. Default is [0.5,0.5]."
			assert (model_kwargs['IndependentFreqPrior'][0]>0.0) and (model_kwargs['IndependentFreqPrior'][1]>0.0), "Both independent frequency prior parameters must be > 0.0"
			hyperparameters['IndependentFreqPrior']=np.array(model_kwargs['IndependentFreqPrior'])	
		else:
			hyperparameters['IndependentFreqPrior']=np.array([0.5,0.5])

		if 'ArbitraryFreqPriorParam' in model_kwargs.keys():
			assert isinstance(model_kwargs['ArbitraryFreqPriorParam'],float),"ArbitraryFreqPriorParam defines the concentration of a symmetric Dirichlet distribution (alpha), where alpha=ArbitraryFreqPriorParam/N_dim. Default is 1.0, which is equivalent to Jeffrey's prior for the symmetric Dirichlet distribution. "
			assert (model_kwargs['ArbitraryFreqPriorParam']>0.0),"ArbitraryFreqPriorParam must be greater than zero."
			hyperparameters['ArbitraryFreqPriorParam']=model_kwargs['ArbitraryFreqPriorParam']
		else:
			hyperparameters['ArbitraryFreqPriorParam']=1.0


		assert isinstance(PriorInformationParameters,dict),"PriorInformationParameters must be a dictionary of prior-specific parameters."
		assert set(PriorInformationParameters.keys()).symmetric_difference(['Strength', 'Smoothing', 'LogAnnotRateParam', 'LogSymptomFreqParam'])==set(),"PriorInformationParameters must be a dictionary that defines the the parameters that specify the heirarchical prior model for symptom set frequency. Four parameters must be present: Strength, Smoothing, LogAnnotRateParam, and LogSymptomFreqParam."
		assert isinstance(PriorInformationParameters['Strength'],float) and (PriorInformationParameters['Strength']>0.0),"Initial prior strength must be a float >0.0."
		assert isinstance(PriorInformationParameters['Smoothing'],float) and (PriorInformationParameters['Smoothing']>0.0) and (PriorInformationParameters['Smoothing']<1.0),"Initial prior smoothing must be a float in (0.0,1.0)."
		assert isinstance(PriorInformationParameters['LogAnnotRateParam'],float) and (PriorInformationParameters['LogAnnotRateParam']>0.0) and (PriorInformationParameters['LogAnnotRateParam']<1.0),"Initial LogAnnotRateParam must be a float in (0.0,1.0)."
		assert isinstance(PriorInformationParameters['LogSymptomFreqParam'],float) and (PriorInformationParameters['LogSymptomFreqParam']>0.0) and (PriorInformationParameters['LogSymptomFreqParam']<1.0),"Initial LogSymptomFreqParam must be a float in (0.0,1.0)."		

		


		print('Step 1: Building data structures required for inference...')
		TargetSubjectIndex=list(TargetSubjectIndex)
		disease_filtered_sparse_matrix = self.SparseSymptomMatrix[self.SubjectIndexMap.loc[TargetSubjectIndex],:]
		disease_filtered_subject_index = pd.Series(np.arange(len(TargetSubjectIndex)),index=TargetSubjectIndex)
		disease_filtered_hpo_map = self.HPOIndexMap.loc[HPOPriorInfo.index]
		inference_data_structure=InferenceDataStruct(disease_filtered_sparse_matrix,disease_filtered_subject_index,disease_filtered_hpo_map)

		print('Step 2: Building heirarchical prior...')
		hierarchical_prior=DirichletSymptomPrior(self.HPOIndexMap,{'NA':HPOPriorInfo},{'NA':inference_data_structure},init_log_symptom_freq_param=PriorInformationParameters['LogSymptomFreqParam'],init_log_annot_rate_param=PriorInformationParameters['LogAnnotRateParam'],init_smoothing=PriorInformationParameters['Smoothing'],init_strength=PriorInformationParameters['Strength'])
		symptom_set_prior=hierarchical_prior.disease_specific_dirichlet_params['NA']


		print('Step 3: Initializing model parameters...')
		carrier_freq_prior=self._convert_bounds_to_beta_prior(CarrierFrequencyPriorInterval[0],CarrierFrequencyPriorInterval[1],CI=CI)
		carrier_freq_posterior=carrier_freq_prior.copy()
		if hyperparameters['BackgroundModel']=='Independent':
			background_prior=hyperparameters['IndependentFreqPrior']
		else:
			background_prior=hyperparameters['ArbitraryFreqPriorParam']


		#initialize background from full dataset.
		carrier_indicators=pd.Series(np.zeros(len(TargetSubjectIndex)),index=TargetSubjectIndex)
		symptom_set_posterior=symptom_set_prior.copy()
		if hyperparameters['BackgroundModel']=='Independent':
			background_posterior,background_symptom_set_log_prob=self._UpdateIndependentBackground(carrier_indicators,inference_data_structure,hyperparameters['IndependentFreqPrior'])
		else:
			background_posterior,background_symptom_set_log_prob=self._UpdateArbitraryBackground(carrier_indicators,inference_data_structure,hyperparameters['ArbitraryFreqPriorParam'])

		# #now initialize carrier_indicators
		carrier_indicators=self._UpdateCarrierIndicators(TargetSubjectIndex,inference_data_structure,carrier_freq_posterior,symptom_set_posterior,background_symptom_set_log_prob)

		# #now update parameters
		symptom_set_posterior=self._UpdateSetBasedPosterior(carrier_indicators,inference_data_structure,symptom_set_prior)
		carrier_freq_posterior=self._UpdateCarrierFreqPosterior(carrier_indicators,carrier_freq_prior)
		if hyperparameters['BackgroundModel']=='Independent':
			background_posterior,background_symptom_set_log_prob=self._UpdateIndependentBackground(carrier_indicators,inference_data_structure,hyperparameters['IndependentFreqPrior'])
		else:
			background_posterior,background_symptom_set_log_prob=self._UpdateArbitraryBackground(carrier_indicators,inference_data_structure,hyperparameters['ArbitraryFreqPriorParam'])

		ELBO=self._CarrierModelMargLike(carrier_indicators,inference_data_structure,carrier_freq_posterior,symptom_set_posterior,background_posterior,background_symptom_set_log_prob,carrier_freq_prior,symptom_set_prior,background_prior,hyperparameters['BackgroundModel'])

		print('Completed iteration {0:d} of model fitting. ELBO: {1:f}'.format(1,ELBO))

		prevELBO=ELBO
		for fit_iter in range(1,max_iter):
			carrier_indicators=self._UpdateCarrierIndicators(TargetSubjectIndex,inference_data_structure,carrier_freq_posterior,symptom_set_posterior,background_symptom_set_log_prob)
			symptom_set_posterior=self._UpdateSetBasedPosterior(carrier_indicators,inference_data_structure,symptom_set_prior)
			carrier_freq_posterior=self._UpdateCarrierFreqPosterior(carrier_indicators,carrier_freq_prior)
			if hyperparameters['BackgroundModel']=='Independent':
				background_posterior,background_symptom_set_log_prob=self._UpdateIndependentBackground(carrier_indicators,inference_data_structure,hyperparameters['IndependentFreqPrior'])
			else:
				background_posterior,background_symptom_set_log_prob=self._UpdateArbitraryBackground(carrier_indicators,inference_data_structure,hyperparameters['ArbitraryFreqPriorParam'])
			ELBO=self._CarrierModelMargLike(carrier_indicators,inference_data_structure,carrier_freq_posterior,symptom_set_posterior,background_posterior,background_symptom_set_log_prob,carrier_freq_prior,symptom_set_prior,background_prior,hyperparameters['BackgroundModel'])

			error=(ELBO-prevELBO)/np.abs(ELBO)
			if error<=error_tol:
				print('Inference complete. Final ELBO (Error): {0:f} ({1:e}).'.format(ELBO,error))
				break
			else:
				prevELBO=ELBO
				print('Completed {0:d} iterations. Current ELBO (Error): {1:f} ({2:e})'.format(fit_iter+1,ELBO,error))		


		results_dictionary={}
		results_dictionary['CarrierFrequencyPosterior']=carrier_freq_posterior
		results_dictionary['SubjectLevelCarrierProbabilities']=carrier_indicators
		weights=[]
		index=[]
		for set_idx,posterior_weight in symptom_set_posterior.items():
			weights+=[posterior_weight]
			index+=[';'.join([inference_data_structure.oringal_index_map_to_hpo.loc[x] for x in inference_data_structure.unique_symptom_sets.loc[set_idx]])]
		results_dictionary['SymptomSetPosteriors']=pd.Series(weights,index=index)
		results_dictionary['HierarchicalPriorParameters']=hierarchical_prior.parameters
		return results_dictionary



