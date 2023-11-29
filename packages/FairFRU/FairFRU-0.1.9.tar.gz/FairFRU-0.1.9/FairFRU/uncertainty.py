import numpy as np

def uncertainty(full, prot, decision_class):
    '''
    Parameters
    ----------
    full: membership values of instances to the boundary regions using the full set of features,
    prot: membership values of instances to the boundary regions using the set of features without including the protected feature
    decision_class: index of the decision class
    Returns
    -------
    FRU-value attached to the specified decision class for the protected attribute that was removed
    '''
    
    POS_full, NEG_full, BND_full = full
    POS_prot, NEG_prot, BND_prot = prot

    #diff_prot = BND_prot[decision_class] - BND_full[decision_class]
    #diff_prot = np.where(diff_prot < 0, 0, diff_prot)
    #from numpy import linalg as la
    #round((float(la.norm(diff_prot) / la.norm(BND_prot[decision_class]))),2)

    return (np.sum((BND_prot[decision_class] - BND_full[decision_class])**2))**0.5