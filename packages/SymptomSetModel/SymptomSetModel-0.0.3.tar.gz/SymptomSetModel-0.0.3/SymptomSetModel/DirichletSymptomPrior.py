import pandas as pd 
import numpy as np
from scipy.special import betaln,logsumexp,logit,expit
from scipy.stats import beta as beta_dist
from PiecewiseBeta.PiecewiseBeta import PiecewiseBeta
from collections.abc import Iterable

from .DirichletPriorOptimizer import DirichletPriorOptimizer

SMALL_FLOAT=np.finfo(np.float64).eps
MINLOG = np.log(np.finfo(np.float64).eps)

class DirichletSymptomPrior:

	def _simple_beta_marg_like(self,a,b,successes,failures):
		return betaln(a+successes,b+failures)-betaln(a,b)

	def _symptom_log_marginals_beta_pieces(self,segment_probs):

		segment_probs=np.array(segment_probs)
		segment_probs/=segment_probs.sum()

		pbeta=PiecewiseBeta(self.piecewise_beta_cut_points,self.linked_frequency_prior_params[0],self.linked_frequency_prior_params[1])

		log_symptom_freq=pbeta.MarginalLogLikelihood(segment_probs,1,1)
		
		return np.exp(log_symptom_freq)


	def _symptom_log_marginals_counts(self,successes, total):

		log_symptom_freq=self._simple_beta_marg_like(self.linked_frequency_prior_params[0]+successes,self.linked_frequency_prior_params[1]+total-successes,1,0)

		return np.exp(log_symptom_freq)


	def _process_freq_info(self,hpo,freq_info):

		if isinstance(freq_info,tuple):
			assert len(freq_info)==2,"Frequency information for HPO {0:s} data type 'tuple' does not match expectations. Must have two entries.".format(hpo)
			assert freq_info[1]>=freq_info[0],"Frequency counts for HPO {0:s} are improper. Must be in (successes, total) format."
			return self._symptom_log_marginals_counts(freq_info[0],freq_info[1]),False
		elif isinstance(freq_info,Iterable):
			freq_info=np.array(freq_info)
			assert len(freq_info)==(self.piecewise_beta_cut_points.shape[0]-1),"Frequency information for HPO {0:s} data type 'frequency classes' does not match expectations. Number of entries must match provided beta distribution cut points".format(hpo)
			return self._symptom_log_marginals_beta_pieces(freq_info),True
		else: 
			raise ValueError("Error in frequency informaton for HPO {0:s}. Frequency information must either be a tuple of length 2 or a vector of frequency classes.".format(hpo))

	def __init__(self,hpo_to_index_map,disease_specific_hpo_info,disease_specific_inference_data_structs,init_log_symptom_freq_param=0.999,init_log_annot_rate_param=0.999,init_smoothing=0.99,init_strength=1.0,regularization_penalty=0.01,piecewise_beta_cut_points=[0.0,0.04,0.3,0.8,0.99,1.0],linked_frequency_prior_params=[1.25,1.25],couple_strengths=False,update_strength=True,update_smoothing=True,update_param_coeff=True):

		"""Builds and optimizes a hierarchical dirichlet prior over all possible symptom sets for a collection of diseases, where the prior distribution over each disease is conditionally indepedendent given a set of annotation and frequency evidence parameters. The probability mass assigned to a single symptom set for disease D is:

		P(Set_{D,i}|alpha,beta,nu,zeta_{D})=(zeta_{D} times |Set_{D}|) times (sum{s in Set_{D,i}} annot_{s,D}^{alpha} times freq_{s,D}^{beta})^{nu}/(sum_{i}(sum{s in Set_{D,i}} annot_{s,D}^{alpha} times freq_{s,D}^{beta})^{nu}),

		where alpha represents the dataset-wide annotation rate evidence prior, beta represents the dataset-wide frequency evidence prior, nu represents a dataset-wide smoothing parameter, and zeta_{D} represents the strength of the prior for disease D. 

		As alpha,beta -> zero, then then model weighs sets with more symptoms heavier than those with fewer, regardless of their annotate probability or frequency. As nu->0, the dirichlet distribution approaches uniform, meaning that number of symptoms/their annotation information no longer matters. The diseease specific strengths control the attraction of the prior for new data, with larger strength parameters having a stronger attraction for new data.  
		
		Args:
		    hpo_to_index_map (pd.Series): Map that aligns each symptom to an index in the primary data array
		    disease_specific_hpo_info (dict of pd.DataFrame's): Dictionary of pandas DataFrames that contain the symptom annotation rates and their frequency information. The latter is converted into a simple float by taking an expectation.
		    disease_specific_inference_data_structs (dictionary of InferenceDataStruct's): Dictionary of InferenceDataStruct's (see PDSBase), one for each disease.
		    init_log_symptom_freq_param (float, optional): Initial value for the symptom frequency evidence parameter. Default is 0.999
		    init_log_annot_rate_param (float, optional): Initial value for the symptom annotation rate evidence parameter. Default is 0.999 
		    init_smoothing (float, optional): Initial value for the dirichlet smoothing parameter. Default is 0.99.
		    init_strength (float, optional): Initial value for the strength parameter(s). Default is 1.0
		    regularization_penalty (float, optional): Penalty used to regularize inference, which ensures that inference converges in the face of no evidence. Default is 0.01.
		    piecewise_beta_cut_points (list, optional): Cutpoints for the piecewise prior used to define ordinal symptom frequencies. Default is [0.0,0.04,0.3,0.8,0.99,1.0], which represents the cutpoints defined by the HPO frequency categories. 
		    linked_frequency_prior_params (list, optional): Parameters of the beta distribution used to compute posterior expectations. Default is [1.25,1.25], which defines a relatively diffuse prior centered at 0.5.
		    couple_strengths (bool, optional): Whether or not to couple the strengths across diseases. Default is False, which allows each disease to build it's own relevance. 
		    update_strength (bool, optional):  Indicates whether to update strength parameter(s). Used for debugging. 
		    update_smoothing (bool, optional): Indicates whether to update smoothing parameters. Used for debugging. 
		    update_param_coeff (bool, optional):  Indicates whether to update evidence parameters. Used for debugging. 
		"""
		self.hpo_to_index_map=hpo_to_index_map
		self.piecewise_beta_cut_points=np.array(piecewise_beta_cut_points)
		self.linked_frequency_prior_params=np.array(linked_frequency_prior_params)
		self.disease_specific_inference_data_structs=disease_specific_inference_data_structs
		self.parameters={'LogSymptomFreqParam':init_log_symptom_freq_param,'LogAnnotRateParam':init_log_annot_rate_param,'Strength':init_strength,'Smoothing':init_smoothing}

		self.disease_specific_prior_info={}
		for dis_id in self.disease_specific_inference_data_structs.keys():
			prior_info=pd.DataFrame([],columns=['AnnotProb','IsPiecewise','FreqPrior','SymptomFreq'],index=disease_specific_hpo_info[dis_id].index)
			prior_info=prior_info.astype({"AnnotProb": float, "IsPiecewise": bool,'SymptomFreq':float})

			annot_dataframe=disease_specific_hpo_info[dis_id]
			for hpo,annot_info in annot_dataframe.iterrows():
				rate=annot_info.iloc[0]
				freq_prior=annot_info.iloc[1]
				output=self._process_freq_info(hpo,freq_prior)
				prior_info.at[hpo,'FreqPrior']=freq_prior
				prior_info.loc[hpo,'AnnotProb']=rate
				prior_info.loc[hpo,'IsPiecewise']=output[1]			
				prior_info.loc[hpo,'SymptomFreq']=output[0]
			self.disease_specific_prior_info[dis_id]=prior_info.copy()


		self.prior_optimizer=DirichletPriorOptimizer(self.hpo_to_index_map,self.disease_specific_prior_info,self.disease_specific_inference_data_structs,couple_strengths=couple_strengths,update_param_coeff=update_param_coeff,update_smoothing=update_smoothing,update_strength=update_strength,init_log_symptom_freq_param=init_log_symptom_freq_param,init_log_annot_rate_param=init_log_annot_rate_param,init_smoothing=init_smoothing,init_strength=init_strength,regularization_penalty=regularization_penalty)

		self.disease_specific_dirichlet_params=self.prior_optimizer.ReturnDirichletParamSet()

	def UpdatePriorParams(self,new_set_counts,error_tol=1e-8,verbose=False,learning_rate=1.0,temperature=1.0):
		"""Updates dirichlet symptom prior given some new collection of symptom set counts.
		
		Args:
		    new_set_counts (dictionary of pd.Series): Dictionary of disease-specific observed counts for each symptom set, with set counts stored in a pd.Series with index defined in InferenceDataStruct
		    error_tol (float, optional):  Error tolerance for convergence monitoring.
		    verbose (bool, optional): Determines if update information should be printed to StdOut. Default is False
		    learning_rate (float, optional):  Float that determines step size for inference algorithm, which is the BFGS implemented in torchmin.
		    temperature (float, optional):  Float in (0.0,1.0] that determines if temperature should be added for smoothing during inference. Not currently implemented. 
		
		Returns:
		    float: Total loss after optimization is complete
		"""
		loss=self.prior_optimizer.Fit(new_set_counts,error_tol,verbose=verbose,learning_rate=learning_rate,temperature=temperature)
		self.disease_specific_dirichlet_params=self.prior_optimizer.ReturnDirichletParamSet()

		if self.prior_optimizer.strengths_coupled:
			self.parameters['Strength']=np.exp(self.prior_optimizer.log_strength_parameter.detach().numpy())
		else:
			self.parameters['Strength']=pd.Series(np.exp([x.detach().numpy() for x in self.prior_optimizer.log_strength_parameter.values()]),index=list(self.prior_optimizer.log_strength_parameter.keys()))
		self.parameters['Smoothing']=expit(self.prior_optimizer.logit_smoothing_parameter.detach().numpy())
		self.parameters['LogAnnotRateParam']=expit(self.prior_optimizer.log_annot_rate_param_logit.detach().numpy())
		self.parameters['LogSymptomFreqParam']=expit(self.prior_optimizer.log_symptom_freq_param_logit.detach().numpy())

		return loss

	def ReturnLossComponents(self,set_counts,temperature=1.0):
		"""Summary
		
		Args:
		    set_counts (dictionary of pd.Series):  Dictionary of pd.Series. Each series contains the observed set counts for a given disease.
		    temperature (float,optional): Float in (0.0,1.0] that determines if temperature should be added for smoothing during inference. Not currently implemented. 
		
		Returns:
		    dict of pd.Series: Returns a tuple of loss componenents. 
		"""
		self.prior_optimizer._set_new_counts(set_counts)
		return self.prior_optimizer.ReturnLossComponents(set_counts,temperature=temperature)

	

