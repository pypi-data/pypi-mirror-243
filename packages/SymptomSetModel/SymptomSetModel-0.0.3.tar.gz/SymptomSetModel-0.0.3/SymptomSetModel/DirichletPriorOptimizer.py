import numpy as np
import pandas as pd
from scipy.special import logit as scipylogit
from PiecewiseBeta.PiecewiseBeta import PiecewiseBeta
import torch
from tensordict import TensorDict
from torchmin import Minimizer
from torch.special import gammaln as _tgammaln
from torch.special import digamma as _tdigamma
import copy

SMALL_FLOAT=torch.tensor(torch.finfo(torch.float64).eps)
MINLOG = torch.log(torch.tensor(torch.finfo(torch.float64).eps))

class _vb_dirichlet_map_loss(torch.nn.Module):

	def _multivariate_log_beta(self,alpha_tensor):
		return torch.sum(_tgammaln(alpha_tensor))-_tgammaln(torch.sum(alpha_tensor))

	def _dirichlet_exp_logx(self,p_tensor):
		return _tdigamma(p_tensor)-_tdigamma(torch.sum(p_tensor))

	def _dirichlet_log_like(self,log_prob_tensor,param_tensor):
		return torch.sum((param_tensor-1.0)*log_prob_tensor)-self._multivariate_log_beta(param_tensor)

	def _dirichlet_entropy(self,ptensor):
		return self._multivariate_log_beta(ptensor)+(torch.sum(ptensor)-ptensor.shape[0])*_tdigamma(torch.sum(ptensor))-torch.sum((ptensor-1.0)*_tdigamma(ptensor))


	def __init__(self,parent_inference_class):
		super(_vb_dirichlet_map_loss, self).__init__()
		self.parent_inference_class=parent_inference_class

	def _dirichlet_component(self,set_counts,dirichlet_params):

		post_params=set_counts*self.parent_inference_class.current_temperature+dirichlet_params*self.parent_inference_class.current_temperature-self.parent_inference_class.current_temperature+1.0
		exp_log_vals=self._dirichlet_exp_logx(post_params)

		loss=torch.sum(exp_log_vals*set_counts)+self._dirichlet_log_like(exp_log_vals,dirichlet_params)+(1.0/self.parent_inference_class.current_temperature)*self._dirichlet_entropy(post_params)
		return loss

	def _regularization_component(self,logit_freq_param,logit_annot_param,log_strength,logit_smoothing):
		loss=0.0
		loss+=-1.0*(logit_freq_param**2.0)*self.parent_inference_class.regularization_penalty
		loss+=-1.0*(logit_annot_param**2.0)*self.parent_inference_class.regularization_penalty
		loss+=-1.0*(logit_smoothing**2.0)*self.parent_inference_class.regularization_penalty
		if self.parent_inference_class.strengths_coupled:
			loss+=-1.0*(log_strength**2.0)*self.parent_inference_class.regularization_penalty
		else:
			for dis_id in self.parent_inference_class.disease_specific_set_indices.keys():
				loss+=-1.0*(log_strength[dis_id]**2.0)*self.parent_inference_class.regularization_penalty
		return loss

	def forward(self, disease_specific_dirichlet_params,logit_freq_param,logit_annot_param,log_strength,logit_smoothing):

		#model likelihood
		dirichlet_loss=0.0
		for dis_id,parameter_vec in disease_specific_dirichlet_params.items():
			dirichlet_loss+=self._dirichlet_component(self.parent_inference_class.disease_specific_set_counts[dis_id],parameter_vec)
		prior_loss=self._regularization_component(logit_freq_param,logit_annot_param,log_strength,logit_smoothing)
		return -1.0*(dirichlet_loss+prior_loss)


class DirichletPriorOptimizer(torch.nn.Module):


	def _multivariate_log_beta(self,alpha_tensor):
		return torch.sum(_tgammaln(alpha_tensor))-_tgammaln(torch.sum(alpha_tensor))

	def _dirichlet_exp_logx(self,p_tensor):
		return _tdigamma(p_tensor)-_tdigamma(torch.sum(p_tensor))

	def _dirichlet_log_like(self,log_prob_tensor,param_tensor):
		prior_norm_const=self._multivariate_log_beta(param_tensor)
		return torch.sum((param_vec-1.0)*log_prob_tensor)-prior_norm_const

	def _dirichlet_entropy(self,ptensor):
		return self._multivariate_log_beta(ptensor)+(torch.sum(ptensor)-ptensor.shape[0])*_tdigamma(torch.sum(pvec))-torch.sum((_tgammaln-1.0)*_tdigamma(_tgammaln))

	
	def __init__(self,symptom_to_array_index,disease_specific_annot_data,disease_specific_data_structs,couple_strengths=False,update_param_coeff=True,update_smoothing=True,update_strength=True,init_log_symptom_freq_param=0.999,init_log_annot_rate_param=0.999,init_smoothing=0.999999,init_strength=1.0,regularization_penalty=0.01):

		"""Builds and optimizes a hierarchical dirichlet prior over all possible symptom sets for a collection of diseases, where the prior distribution over each disease is conditionally indepedendent given a set of annotation and frequency evidence parameters. The probability mass assigned to a single symptom set for disease D is:

		P(Set_{D,i}|alpha,beta,nu,zeta_{D})=(zeta_{D} times |Set_{D}|) times (sum{s in Set_{D,i}} annot_{s,D}^{alpha} times freq_{s,D}^{beta})^{nu}/(sum_{i}(sum{s in Set_{D,i}} annot_{s,D}^{alpha} times freq_{s,D}^{beta})^{nu}),

		where alpha represents the dataset-wide annotation rate evidence prior, beta represents the dataset-wide frequency evidence prior, nu represents a dataset-wide smoothing parameter, and zeta_{D} represents the strength of the prior for disease D. 

		As alpha,beta -> zero, then then model weighs sets with more symptoms heavier than those with fewer, regardless of their annotate probability or frequency. As nu->0, the dirichlet distribution approaches uniform, meaning that number of symptoms/their annotation information no longer matters. The diseease specific strengths control the attraction of the prior for new data, with larger strength parameters having a stronger attraction for new data.  
		
		Args:
		    symptom_to_array_index (pd.Series/dictionary): Symptom-array index pairs for the symptoms in the dataset.
		    disease_specific_annot_data (dictionary of pd.DataFrame): Dictionary of pandas DataFrames that contain the symptom annotation rates and their frequency prior information, both of which are floats.
		    disease_specific_data_structs (TYPE): Dictionary of InferenceDataStruct's (see PDSBase), one for each disease
		    couple_strengths (bool, optional): Whether or not to couple the strengths across diseases. Default is False, which allows each disease to build it's own relevance. 
		    update_param_coeff (bool, optional): Indicates whether to update evidence parameters. Used for debugging. 
		    update_smoothing (bool, optional): Indicates whether to update smoothing parameters. Used for debugging. 
		    update_strength (bool, optional): Indicates whether to update strength parameter(s). Used for debugging. 
		    init_log_symptom_freq_param (float, optional): Initial value for the symptom annotation rate evidence parameter. Default is 0.999
		    init_log_annot_rate_param (float, optional):  Initial value for the symptom frequency evidence parameter. Default is 0.999
		    init_smoothing (float, optional):  Initial value for the dirichlet smoothing parameter. Default is 0.999999
		    init_strength (float, optional):  Initial value for the strength parameter(s). Default is 1.0
		    regularization_penalty (float, optional): Penalty used to regularize inference, which ensures that inference converges in the face of no evidence. Default is 0.01.
		"""
		super(DirichletPriorOptimizer,self).__init__()

		self.current_temperature=1.0
		self.strengths_coupled=couple_strengths

		self.symptom_to_array_index={}
		for symptom,idx in symptom_to_array_index.items():
			self.symptom_to_array_index[symptom]=idx

		self.array_index_to_symptoms={}
		for symptom,idx in symptom_to_array_index.items():
			self.array_index_to_symptoms[idx]=symptom
		

		if update_smoothing:
			self.logit_smoothing_parameter=torch.nn.Parameter(torch.tensor(scipylogit(init_smoothing),requires_grad=True))
		else:
			self.logit_smoothing_parameter=torch.tensor(scipylogit(init_smoothing),dtype=torch.float64,requires_grad=False)

		if self.strengths_coupled:
			if update_strength:
				self.log_strength_parameter=torch.nn.Parameter(torch.tensor(np.log(init_strength),requires_grad=True))
			else:
				self.log_strength_parameter=torch.tensor(np.log(init_strength),dtype=torch.float64,requires_grad=False)
		else:
			self.log_strength_parameter=torch.nn.ParameterDict({x:torch.tensor(np.log(init_strength),dtype=torch.float64) for x in disease_specific_annot_data.keys()})
			if update_strength==False:
				self.log_strength_parameter=self.log_strength_parameter.requires_grad_(False)

		if update_param_coeff:
			self.log_symptom_freq_param_logit=torch.nn.Parameter(torch.tensor(scipylogit(init_log_symptom_freq_param),requires_grad=True))
			self.log_annot_rate_param_logit=torch.nn.Parameter(torch.tensor(scipylogit(init_log_annot_rate_param),requires_grad=True))
		else:
			self.log_symptom_freq_param_logit=torch.nn.Parameter(torch.tensor(scipylogit(init_log_symptom_freq_param),requires_grad=False))
			self.log_annot_rate_param_logit=torch.nn.Parameter(torch.tensor(scipylogit(init_log_annot_rate_param),requires_grad=False))


		self.disease_specific_set_indices={}
		self.disease_specific_set_counts={}
		self.disease_log_num_sets={}
		for dis_id in disease_specific_data_structs.keys():
			self.disease_specific_set_indices[dis_id]=disease_specific_data_structs[dis_id].unique_symptom_sets
			self.disease_specific_set_counts[dis_id]=torch.zeros(len(disease_specific_data_structs[dis_id].unique_symptom_sets),dtype=torch.float64,requires_grad=False)
			self.disease_log_num_sets[dis_id]=torch.tensor(np.log(self.disease_specific_set_counts[dis_id].shape[0]),dtype=torch.float64,requires_grad=False)



		self.disease_specific_hpos={}	
		self.disease_specific_log_symptom_annot_probs={}
		self.disease_specific_log_symptom_frequencies={}
		for dis_id in self.disease_specific_set_indices.keys():
			self.disease_specific_hpos[dis_id]=pd.Series(np.arange(disease_specific_annot_data[dis_id].shape[0]),index=disease_specific_annot_data[dis_id].index)

			self.disease_specific_log_symptom_annot_probs[dis_id]=torch.nn.ParameterDict({x:torch.tensor(0.0,dtype=torch.float64) for x in self.disease_specific_hpos[dis_id].index})
			self.disease_specific_log_symptom_frequencies[dis_id]=torch.nn.ParameterDict({x:torch.tensor(0.0,dtype=torch.float64) for x in self.disease_specific_hpos[dis_id].index})
			for hpo,annot_data in disease_specific_annot_data[dis_id].iterrows():
				self.disease_specific_log_symptom_annot_probs[dis_id][hpo]=torch.tensor(np.log(annot_data.loc['AnnotProb']),dtype=torch.float64)
				self.disease_specific_log_symptom_frequencies[dis_id][hpo]=torch.tensor(np.log(annot_data.loc['SymptomFreq']),dtype=torch.float64)
			self.disease_specific_log_symptom_annot_probs[dis_id]=self.disease_specific_log_symptom_annot_probs[dis_id].requires_grad_(False)
			self.disease_specific_log_symptom_frequencies[dis_id]=self.disease_specific_log_symptom_frequencies[dis_id].requires_grad_(False)

		self.regularization_penalty=torch.tensor(regularization_penalty,dtype=torch.float64,requires_grad=False)


	def _set_new_counts(self, count_series_dict):
		for dis_id,count_series in count_series_dict.items():
			for i,set_idx in enumerate(self.disease_specific_set_indices[dis_id].index):
				self.disease_specific_set_counts[dis_id][i]=count_series.loc[set_idx]

	def _build_dirichlet_params(self,disease_specific_weighted_frequencies):
		disease_specific_dirichlet_params={}
		for dis_id,set_index_to_arrays in self.disease_specific_set_indices.items():
			dirichlet_params=torch.zeros(set_index_to_arrays.shape[0],dtype=torch.float64,requires_grad=False)
			for i,set_idx in enumerate(set_index_to_arrays.index):
				obs_hpos=[self.disease_specific_hpos[dis_id].loc[self.array_index_to_symptoms[x]] for x in set_index_to_arrays.loc[set_idx]]
				dirichlet_params[i]=torch.logsumexp(disease_specific_weighted_frequencies[dis_id][obs_hpos],dim=0)
			dirichlet_params[dirichlet_params<MINLOG]=MINLOG

			#now normalize the probabilities, including the smoothing parameter
			smoothed_dirichlet=torch.nn.functional.sigmoid(self.logit_smoothing_parameter)*dirichlet_params
			norm_const=torch.logsumexp(smoothed_dirichlet,dim=0)
			if self.strengths_coupled:
				dirichlet_params=torch.exp(smoothed_dirichlet-norm_const)*torch.exp(self.log_strength_parameter+self.disease_log_num_sets[dis_id])
			else:
				dirichlet_params=torch.exp(smoothed_dirichlet-norm_const)*torch.exp(self.log_strength_parameter[dis_id]+self.disease_log_num_sets[dis_id])

			disease_specific_dirichlet_params[dis_id]=dirichlet_params
		return disease_specific_dirichlet_params

	def _compute_weighted_frequencies(self,dis_id,hpo):
		return self.disease_specific_log_symptom_annot_probs[dis_id][hpo]*torch.special.expit(self.log_annot_rate_param_logit)+self.disease_specific_log_symptom_frequencies[dis_id][hpo]*torch.special.expit(self.log_symptom_freq_param_logit)

	def forward(self):
		"""Generates dictionary of dirichlet distributions, stored as torch.tensors. 
		
		Returns:
		    Dictionary of torch.tensor: Dirichlet distributions over symptom sets for each disease
		"""
		disease_specific_weighted_frequencies={}
		for dis_id,hpo_list in self.disease_specific_hpos.items():
			disease_specific_weighted_frequencies[dis_id]=torch.zeros(len(hpo_list),dtype=torch.float64,requires_grad=False)
			for hpo,idx in hpo_list.items():
				disease_specific_weighted_frequencies[dis_id][idx]=self._compute_weighted_frequencies(dis_id,hpo)
		disease_specific_dirichlet_params=self._build_dirichlet_params(disease_specific_weighted_frequencies)
		return disease_specific_dirichlet_params


	def Fit(self,set_counts,error_tol,temperature=1.0,verbose=False,max_iter=50,learning_rate=0.1):
		"""Given a dictionary of set counts for each disease (set counts are pd.Series with index corresponding to the set index in InferenceDataStruct), this function optimizes the model parameters (annotation evidence parameters, strength and smooting).
		
		Args:
		    set_counts (Dictionary of pd.Series): Dictionary of disease-specific observed counts for each symptom set, with set indices stored in pd.Series with index defined in InferenceDataStruct
		    error_tol (float): Error tolerance for convergence monitoring.
		    temperature (float,optional): Float in (0.0,1.0] that determines if temperature should be added for smoothing during inference. Not currently implemented. 
		    
		    verbose (bool, optional): Determines if update information should be printed to StdOut. Default is False
		    max_iter (int, optional): Maximum number of iteractions for inference. Default is 500
		    learning_rate (float, optional): Float that determines step size for inference algorithm, which is the BFGS implemented in torchmin.
		
		Returns:
		    float: The final loss after optimization. 
		"""
		self._set_new_counts(set_counts)
		self.current_temperature=temperature
		criterion = _vb_dirichlet_map_loss(self)
		num_failures=0

		def closure():
			optimizer.zero_grad()
			dirichlet_params_set=self.forward()
			loss = criterion(dirichlet_params_set,self.log_symptom_freq_param_logit,self.log_annot_rate_param_logit,self.log_strength_parameter,self.logit_smoothing_parameter)
			return loss 

		if verbose:
			with torch.no_grad():
				init_disease_specific_dirichlet_params=self.forward()
				prev_loss=-1.0*criterion.forward(init_disease_specific_dirichlet_params,self.log_symptom_freq_param_logit,self.log_annot_rate_param_logit,self.log_strength_parameter,self.logit_smoothing_parameter).item()
				print("Dirichlet Symptom Model Initial Loss: {0:.6f}".format(prev_loss))

		optimizer = Minimizer(self.parameters(),method='bfgs',max_iter=max_iter,disp=verbose,options={'lr':learning_rate})
		loss=optimizer.step(closure)
		if verbose:
			print("Dirichlet Symptom Model Optimized Loss: {0:.6f}".format(-1.0*loss))
		return loss

	def ReturnDirichletParamSet(self):
		"""Returns a dictionary of pd.Series. Each series is the dirichlet distribution for a given disease according to the current parameter estimates. 
		
		"""
		with torch.no_grad():
			new_dirichlet_param_set=self.forward()
		output_set={}
		for dis_id,params in new_dirichlet_param_set.items():
			output_set[dis_id]=pd.Series(params.detach().numpy(), self.disease_specific_set_indices[dis_id].index)
		return output_set

	def ReturnLossComponents(self,count_series_dict,temperature=1.0):
		"""Returns the current loss information for the model. 
		
		Args:
		    count_series_dict (dictionary of pd.Series): Dictionary of pd.Series. Each series contains the observed counts for a given disease.
		    temperature (float,optional): Float in (0.0,1.0] that determines if temperature should be added for smoothing during inference. Not currently implemented. 
		
		Returns:
		    Tuple of floats: Returns loss components as (dirichlet loss, regularization loss, total loss)
		"""
		self._set_new_counts(count_series_dict)
		self.current_temperature=temperature
		criterion = _vb_dirichlet_map_loss(self)
		with torch.no_grad():
			dirichlet_params_set=self.forward()
			dirichlet_loss=0.0
			for dis_id in self.disease_specific_set_indices.keys():
				dirichlet_loss+=criterion._dirichlet_component(self.disease_specific_set_counts[dis_id],dirichlet_params_set[dis_id])
			prior_loss=criterion._regularization_component(self.log_symptom_freq_param_logit,self.log_annot_rate_param_logit,self.log_strength_parameter,self.logit_smoothing_parameter)
		return dirichlet_loss.detach().numpy(),prior_loss.detach().numpy(),dirichlet_loss.detach().numpy()+prior_loss.detach().numpy()

