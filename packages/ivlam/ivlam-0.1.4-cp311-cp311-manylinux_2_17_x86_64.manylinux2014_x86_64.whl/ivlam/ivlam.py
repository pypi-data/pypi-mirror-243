from . import _ivlam

# TODO: 封装所有_ivlam函数

import os

_dir = os.path.dirname(os.path.abspath(__file__))


def getdirection(prograde, rveca, rvecb):
    """
    This function converts prograde/retrograde to the d variable

    Parameters
    ----------
    prograde: bool : if true/false, the output d represents prograde/retrograde solution
    rveca: input rank-1 array('d') with bounds (3): The initial position vector.
    rvecb: input rank-1 array('d') with bounds (3): The final position vector.

    Returns:
    -------
    d: The direction of travel. d=1 is 0<=theta<=pi, d=-1 i is pi<theta<2pi
    """
    return _ivlam.ivlam_getdirection(prograde, rveca, rvecb)


def getkandtbysbottomslow(absn, tau):
    """
    kbottom,tbysbot,info = ivlam_getkandtbysbottomslow(absn,tau)

    This function provides the k and T/S at the bottom of the multirev time curve
    Not called by any other routines, the routine is provided as a supplement in case a user wants the exact solution at the bottom
    The slow label is there to indicate it may not be tuned for speed, but is accurate as possible, however it is not particularly slow.
    the approach requires one interpolation look up plus iterations on a function value until convergence.

    Parameters
    ----------
    absn : input int
    tau : input float

    Returns
    -------
    kbottom : float
    tbysbot : float
    info : int
    """
    return _ivlam.ivlam_getkandtbysbottomslow(absn, tau)


def initialize(
    saveallsolutionsupton=-1, path=_dir + "/ivLamTree_20210202_160219_i2d8.bin"
):
    """
    info = ivlam_initialize(saveallsolutionsupton,path)

    Parameters
    ----------
    saveallsolutionsupton : input int. nominally set this to -1
    Note: for ivLam_thruN calls where you want access to all the details (not just velocities from the call) of every solution,
    you must set this to the largest value of |N| that you will call the ivLam_thruN routine
    - if you dont want all the details (i.e. avoid copying the data and allocating a big defined type if N is big) then set to -1;
    - if you have plenty of memory, you can set saveAllSolutionsUptoN to the largest |N| value you plan to use; if N is ~100 there is almost no penalty in terms of memory, speed etc, but it gets a bit wasteful for huge N.
    - if a user only wants a single N solution or a single pair of a multiple rev solution, then the user should set saveAllSolutionsUptoN=-1 so there is not a huge array allocated for storage of every multi-rev case
    - if a user will never use or want details from an allN call with Nrev>50, then set saveAllSolutionsUptoN=50 here and the berN(-N:N) matrix will be available outside with all the details of each solution
    - note saveAllSolutionsUptoN is not the maximum possible N for the algorithm, it only affects what data the user wants to store
    - in the first release of this algorithm, we explicitly stored coefficients for up to N=100; now the improved algorithm includes all N (tested up to 300000)

    path : input string(len=-1). full path of the directory that includes the .bin files (biquintic_Nrev<Ntilde>.bin for Ntilde=-Nmax..Nmax except 0; and bottombiquintic_Nrev<N> for N=0..Nmax)

    Returns
    -------
    info : int !0 on successful return, nonzero otherwise
    """
    return _ivlam.ivlam_initialize(saveallsolutionsupton, path)


def singlen(r1vec, r2vec, tof, direction, ntilde, wantbothifmultirev):
    """
    v1veca,v2veca,v1vecb,v2vecb,inforeturnstatus,infohalfrevstatus = ivlam_singlen(r1vec,r2vec,tof,direction,ntilde,wantbothifmultirev)

    This routine is a wrapper around ivLam_singleN() with additional results: partials of the outputs z=[v1vec,v2vec] with respect to the inputs y=[r1vec,r2vec,tof].
    only inputs relating to the partials are described here, for all others see descriptions in the base subroutine


    Parameters
    ----------
    r1vec : input rank-1 array('d') with bounds (3).
    r2vec : input rank-1 array('d') with bounds (3).
    tof : input float.
    direction : input int. 1 if 0<theta<pi (short-way d=1 in paper), -1 if pi<theta<2pi (long way d=-1 in paper)
    ntilde : input int. signed number of revs; if negative the short-period solution is returned, if positive the long-period solution is returned; if wantBothIfMultiRev==TRUE, then both solutions are returned regardless of sign (see comment #7892) 
    wantbothifmultirev : input int. Only applicable if |Ntilde|>0.   If wantBothIfMultiRev==TRUE, then return both short-and long-period solutions (see comment #7892), otherwise return only the short- or long-period according to the sign of Ntile

    Returns
    -------
    v1veca : rank-1 array('d') with bounds (3). output velocities if a solution exists (comment #7892)
    v2veca : rank-1 array('d') with bounds (3). output velocities if a solution exists (comment #7892)
    v1vecb : rank-1 array('d') with bounds (3). output velocities if a solution exists (comment #7892)
    v2vecb : rank-1 array('d') with bounds (3). output velocities if a solution exists (comment #7892)
    inforeturnstatus : int. !comment #43655
                Positive value returns are considered ok and may have a warning; negative implies a more severe problem like the problem is ill-defined or the solver did not converge.
                Below are single digit returns without chance for any warning additions
                  0     : indicates normal return with either 1 or 2 solutions (converged), depending on what is requested 
                 -1     : tau is out of bounds, i.e. the only singularity (physical) of the problem is encountered or near encountered (i.e. r1vec==r2vec, magnitude AND direction) 
                 -2     : TOF/S is too small on the zero rev, i.e. its too hyperbolic (and violates the interpolation domain)
                 -3     : the initialize routine hasn't been run yet or its been unloaded
                 -4     : invalid direction input
                 -6     : requested to store multirev data but didnt allocate berN properly, rerun initialize with higher saveAllSolutionsUptoN or set it to 0 and dont store details
                 +5     : TOF/S is too low (or extremely close to the bottom of the curve) on the multi rev, i.e. a solution doesnt exist for this N rev and TOF.   The flag is a positive return because it's a result, not an problem. 
                Below are large negative values indicating solver did not converge. The latter digits can be non zero indicating warning flag as described below
                 -1XXXX : the zero rev solver ran into max iterations  (more details in bert%infoIter, and/or rerun with ivLamParam_printIters true).. 
                 -2XXXX : the multi-rev solver ran into max iterations (Ntilde)  
                 -3XXXX : the multi-rev solver ran into max iterations (-Ntilde)    
                Below are the warning indicators, specified by the trailing digits, several may be filled;  if only warnigs are present, the result is positive; if negative and large then the warnings accompany a non-convergence error.    
                  XXXX1, just a warning, indicates Ntilde is huge  (violates the interpolation domain, so proceed with caution, algorithm may fail with such aphysical inputs)
                  XXX1X, just a warning, indicates TOF/S is larger on the zero  rev case than the domain of the interpolation scheme, the algorithm will continue using the guess on the bound (for example if info=10 on exit, same as 00010) 
                  XXX2X, just a warning, indicates TOF/S is larger on the multi rev case than the domain of the interpolation scheme, ..
    infohalfrevstatus : int. !comment #43654
                 1 just a warning, indicates you are close to a half rev,according to user specified tolerance: nearNpiRevWarningThresh, so velocity outputs may be degraded in accuracy (although a solution will be returned)
                -1 indicates an exact half rev detected, in this case, the velocity outputs are completely bogus, but the root-solve is still completed and the bert%ksol is correct 
                 2 just a warning, means its getting close to the 2Npi, it's just a warning as its not a singularity unless r1mag=r2mag, and that will be caught by the tau boundaries (infoReturnStatus=-1 return)   
    """
    return _ivlam.ivlam_singlen(
        r1vec, r2vec, tof, direction, ntilde, wantbothifmultirev
    )


def thrun(r1vec, r2vec, tof, direction, uptonwant, dimv):
    """
    v1vec,v2vec,uptonhave,inforeturnstatusn,infohalfrevstatus = ivlam_thrun(r1vec,r2vec,tof,direction,uptonwant,dimv)

    This routine provides all solutions including up to min(uptoNwant,NmaxTheory) revolutions,
    where NmaxTheory is the largest possible N for a given tau and TOF
    NOTE: ivLam_initialize() must be called prior so that all the interpolation coefficients are already loaded in memory
    NOTE: inputs assume that gravitational parameter is unity

    Parameters
    ----------
    r1vec : input rank-1 array('d') with bounds (3)
    r2vec : input rank-1 array('d') with bounds (3)
    tof : input double
    direction : input int. input int. 1 if 0<theta<pi (short-way d=1 in paper), -1 if pi<theta<2pi (long way d=-1 in paper)
    uptonwant : input int. indicates user wants all solutions from 0 revs thru uptoNwant revs; uptoNwant<=dimV
    dimv : input int.  column dimensions of the output v1vec and v2vec; if ivLam_initialize() was initialized with
                        - saveAllSolutionsUptoN=0, then no limit on dimV (since details of the solutions are not stored in berN)
                        - saveAllSolutionsUptoN>0, then dimv<=saveAllSolutionsUptoN

    Returns
    -------
    v1vec : rank-2 array('d') with bounds (3,1 + 2 * dimv)
    v2vec : rank-2 array('d') with bounds (3,1 + 2 * dimv). 
            on exit, these are filled with 2*uptoNhave+1 solutions;
            these vectors are dimensioned by the user prior to entry in the calling routine,
            a negitive/positive column number indicates the long/short period solution (0-rev just has 1 solution),
            for example v2vec(1:3,-2) is the long period arrival vel for 2 revs, v1vec(1:3,1) is the short period departure vel for 1 revs.
    uptonhave : int.
                - on a successful exit this is min(uptoNwant,NmaxTheory).  All 2*uptoNhave+1 solutions are returned in v1vec and v2vec
                - on unsuccessful exit, uptoNhave is the last value of |N| that the individual call succeeded,
                -                       and infoReturnStatusN contains details (see comment #43655) on the failure.

    inforeturnstatusn : int
        - 0 : succcesful, indicates normal return with requested solutions returned uptoNhave=uptoNwant, maybe more solutions exist with higher N
        - 4 : succcesful, indicates normal return, but user requested uptoNwant and solution bumped into NmaxTheory, so result is uptoNhave<uptoNwant
        - any negative value, the code returns as soon as it encounters an individual N call with a negative value, codes same as comment #43655
        - the detailed infoReturnStatus from comment #43655 (i.e. warnings and other info about iterations) from individual N calls is stored in berN(N)%infoReturn
    infohalfrevstatus : int
    """
    return _ivlam.ivlam_thrun(r1vec, r2vec, tof, direction, uptonwant, dimv)


def zerorev(r1vec, r2vec, tof, direction):
    """
    v1vec,v2vec,inforeturnstatus,infohalfrevstatus = ivlam_zerorev(r1vec,r2vec,tof,direction)

    This routine provides either 1) the unique zero rev solution, or 2) no solution, depending if the geometry parameters are within the interpolation domain
    the routine is a wrapper (with fewer inputs for convenience) around ivLam_singleN; see that routine for details on the input/output
    NOTE: inputs assume that gravitational parameter is unity
    NOTE: ivLam_initialize() must be called prior so that all the interpolation coefficients are already loaded in memory

    Parameters
    ----------
    r1vec : input rank-1 array('d') with bounds (3)
    r2vec : input rank-1 array('d') with bounds (3)
    tof : input float
    direction : input int. input int. 1 if 0<theta<pi (short-way d=1 in paper), -1 if pi<theta<2pi (long way d=-1 in paper)

    Returns
    -------
    v1vec : rank-1 array('d') with bounds (3)
    v2vec : rank-1 array('d') with bounds (3)
    inforeturnstatus : int
    infohalfrevstatus : int
    """
    return _ivlam.ivlam_zerorev(r1vec, r2vec, tof, direction)


def unloaddata(closeprntu):
    """
    info = ivlam_unloaddata(closeprntu)

    this routine deallocates all of the memory and closes the ivLam_log.txt if print unit (prntU) not equal to 6 (screen)
    it is used every time the initialization routine is run, before allocating,
    it also can be used by a user when done to free up all the memory

    Parameters
    ----------
    closeprntu : input int. true means to close the output file (if its not 6); false means to leave it open

    Returns
    -------
    info : int. 0 success, not otherwise
    """
    return _ivlam.ivlam_unloaddata(closeprntu)


def ntildewithderivs(r1vec, r2vec, tof, direction, ntilde, includesecondorder):
    """
    v1vec,v2vec,inforeturnstatus,infohalfrevstatus,dzdyt,d2zdyt = ivlam_ntildewithderivs(r1vec,r2vec,tof,direction,ntilde,includesecondorder)

    this routine provides either the 0 rev or the one side of the multi-rev solution with a specified N.  The side of the multirev case is determined by the sign of Ntilde where N=|Ntilde|
    the routine is a wrapper (with fewer inputs for convenience) around ivLam_singleNwithDerivs; see that routine for details on the input/output
    This routine is likely the most common one to be used when a user needs partials, meaning they will know which solution they want, for partials, 
    they most likely will not want an all-n or even both sides of a single N. 

    Parameters
    ----------
    r1vec : input rank-1 array('d') with bounds (3)
    r2vec : input rank-1 array('d') with bounds (3)
    tof : input float
    direction : input int. input int. 1 if 0<theta<pi (short-way d=1 in paper), -1 if pi<theta<2pi (long way d=-1 in paper)
    ntilde : input int
    includesecondorder : input int. 
    TRUE returns the first and second order partials.  FALSE returns just the first order, and all second order inputs/outputs not touched    
    below are the partials for the A and B solutions, the variables are appended with 't' to emphasize the results are not the propoer matrices dzdy and tensor d2zdy2 because of the contiguous memory ordering
    ny=7 and nz=6 are defined in partialparams, but they are hardcoded and will never change.  The user calling routine must define these variables with the correct dimensions. 

    Returns
    -------
    v1vec : rank-1 array('d') with bounds (3)
    v2vec : rank-1 array('d') with bounds (3)
    inforeturnstatus : int
    infohalfrevstatus : int
    dzdyt : rank-2 array('d') with bounds (7,6)
    d2zdyt : rank-3 array('d') with bounds (7,7,6)
    """
    return _ivlam.ivlam_ntildewithderivs(
        r1vec, r2vec, tof, direction, ntilde, includesecondorder
    )


def singlenwithderivs(
    r1vec, r2vec, tof, direction, ntilde, wantbothifmultirev, includesecondorder
):
    """
    v1veca,v2veca,v1vecb,v2vecb,inforeturnstatus,infohalfrevstatus,dzdyta,d2zdyta,dzdytb,d2zdytb = ivlam_singlenwithderivs(r1vec,r2vec,tof,direction,ntilde,wantbothifmultirev,includesecondorder)

    This routine is a wrapper around ivLam_singleN() with additional results: partials of the outputs z=[v1vec,v2vec] with respect to the inputs y=[r1vec,r2vec,tof].   
    only inputs relating to the partials are described here, for all others see descriptions in the base subroutine 

    Parameters
    ----------
    r1vec : input rank-1 array('d') with bounds (3)
    r2vec : input rank-1 array('d') with bounds (3)
    tof : input float
    direction : input int. input int. 1 if 0<theta<pi (short-way d=1 in paper), -1 if pi<theta<2pi (long way d=-1 in paper)
    ntilde : input int
    wantbothifmultirev : input int
    includesecondorder : input int. TRUE returns the first and second order partials.  FALSE returns just the first order, and all second order inputs/outputs not touched    
    !below are the partials for the A and B solutions, the variables are appended with 't' to emphasize the results are not the propoer matrices dzdy and tensor d2zdy2 because of the contiguous memory ordering
    !ny=7 and nz=6 are defined in partialparams, but they are hardcoded and will never change.  The user calling routine must define these variables with the correct dimensions. 

    Returns
    -------
    v1veca : rank-1 array('d') with bounds (3)
    v2veca : rank-1 array('d') with bounds (3)
    v1vecb : rank-1 array('d') with bounds (3)
    v2vecb : rank-1 array('d') with bounds (3)
    inforeturnstatus : int
    infohalfrevstatus : int
    dzdyta : rank-2 array('d') with bounds (7,6). (:,i)   is the jacobian of the ith output, ordered this way so each jacobian is in contiguous memory; 
    d2zdyta : rank-3 array('d') with bounds (7,7,6).(:,:,i) is the hessian  of the ith output, ordered this way so each hessian  is in contiguous memory.
    dzdytb : rank-2 array('d') with bounds (7,6)
    d2zdytb : rank-3 array('d') with bounds (7,7,6)
    """
    return _ivlam.ivlam_singlenwithderivs(
        r1vec, r2vec, tof, direction, ntilde, wantbothifmultirev, includesecondorder
    )


def zerorev_multipleinput(r1vec, r2vec, tof, direction):
    """
    v1vec,v2vec,inforeturnstatus,infohalfrevstatus = ivlam_zerorev_multipleinput(r1vec,r2vec,tof,direction)

    seek Q solutions, where each solution inputs/outputs is stored in the last dimension (1:Q) of the corresponding variables.

    Parameters
    ----------
    r1vec : input rank-2 array('d') with bounds (3,q)
    r2vec : input rank-2 array('d') with bounds (3,q)
    tof : input rank-1 array('d') with bounds (q)
    direction : input rank-1 array('i') with bounds (q)

    Other Parameters
    ----------------
    q : input int, optional
        Default: shape(r1vec, 1)

    Returns
    -------
    v1vec : rank-2 array('d') with bounds (3,q)
    v2vec : rank-2 array('d') with bounds (3,q)
    inforeturnstatus : rank-1 array('i') with bounds (q)
    infohalfrevstatus : rank-1 array('i') with bounds (q)
    """
    return _ivlam.ivlam_zerorev_multipleinput(r1vec, r2vec, tof, direction)


def singlen_multipleinput(r1vec, r2vec, tof, direction, ntilde, wantbothifmultirev):
    """
    v1veca,v2veca,v1vecb,v2vecb,inforeturnstatus,infohalfrevstatus = ivlam_singlen_multipleinput(r1vec,r2vec,tof,direction,ntilde,wantbothifmultirev)

    Wrapper for ``ivlam_singlen_multipleinput``.

    Parameters
    ----------
    r1vec : input rank-2 array('d') with bounds (3,q)
    r2vec : input rank-2 array('d') with bounds (3,q)
    tof : input rank-1 array('d') with bounds (q)
    direction : input rank-1 array('i') with bounds (q)
    ntilde : input rank-1 array('i') with bounds (q)
    wantbothifmultirev : input int

    Other Parameters
    ----------------
    q : input int, optional
        Default: shape(r1vec, 1)

    Returns
    -------
    v1veca : rank-2 array('d') with bounds (3,q)
    v2veca : rank-2 array('d') with bounds (3,q)
    v1vecb : rank-2 array('d') with bounds (3,q)
    v2vecb : rank-2 array('d') with bounds (3,q)
    inforeturnstatus : rank-1 array('i') with bounds (q)
    infohalfrevstatus : rank-1 array('i') with bounds (q)
    """
    return _ivlam.ivlam_singlen_multipleinput(
        r1vec, r2vec, tof, direction, ntilde, wantbothifmultirev
    )


def thrun_multipleinput(r1vec, r2vec, tof, direction, uptonwant, dimv):
    """
    v1vec,v2vec,uptonhave,inforeturnstatusn,infohalfrevstatus = ivlam_thrun_multipleinput(r1vec,r2vec,tof,direction,uptonwant,dimv)

    Wrapper for ``ivlam_thrun_multipleinput``.

    Parameters
    ----------
    r1vec : input rank-2 array('d') with bounds (3,q)
    r2vec : input rank-2 array('d') with bounds (3,q)
    tof : input rank-1 array('d') with bounds (q)
    direction : input rank-1 array('i') with bounds (q)
    uptonwant : input int
    dimv : input int

    Other Parameters
    ----------------
    q : input int, optional
        Default: shape(r1vec, 1)

    Returns
    -------
    v1vec : rank-3 array('d') with bounds (3,1 + 2 * dimv,q)
    v2vec : rank-3 array('d') with bounds (3,1 + 2 * dimv,q)
    uptonhave : rank-1 array('i') with bounds (q)
    inforeturnstatusn : rank-1 array('i') with bounds (q)
    infohalfrevstatus : rank-1 array('i') with bounds (q)
    """
    return _ivlam.ivlam_thrun_multipleinput(
        r1vec, r2vec, tof, direction, uptonwant, dimv
    )


def ntildewithderivs_multipleinput(
    r1vec, r2vec, tof, direction, ntilde, includesecondorder
):
    """
    v1vec,v2vec,inforeturnstatus,infohalfrevstatus,dzdyt,d2zdyt = ivlam_ntildewithderivs_multipleinput(r1vec,r2vec,tof,direction,ntilde,includesecondorder)

    Wrapper for ``ivlam_ntildewithderivs_multipleinput``.

    Parameters
    ----------
    r1vec : input rank-2 array('d') with bounds (3,q)
    r2vec : input rank-2 array('d') with bounds (3,q)
    tof : input rank-1 array('d') with bounds (q)
    direction : input rank-1 array('i') with bounds (q)
    ntilde : input rank-1 array('i') with bounds (q)
    includesecondorder : input int

    Other Parameters
    ----------------
    q : input int, optional
        Default: shape(r1vec, 1)

    Returns
    -------
    v1vec : rank-2 array('d') with bounds (3,q)
    v2vec : rank-2 array('d') with bounds (3,q)
    inforeturnstatus : rank-1 array('i') with bounds (q)
    infohalfrevstatus : rank-1 array('i') with bounds (q)
    dzdyt : rank-3 array('d') with bounds (7,6,q)
    d2zdyt : rank-4 array('d') with bounds (7,7,6,q)
    """
    return _ivlam.ivlam_ntildewithderivs_multipleinput(
        r1vec, r2vec, tof, direction, ntilde, includesecondorder
    )
