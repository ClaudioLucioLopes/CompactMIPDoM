import numpy as np
from mip import Model, minimize, CBC,GRB, BINARY, OptimizationStatus,CONTINUOUS,xsum

def DOM_distance(A, B):
    dist = 0
    for i in range(len(A)):
        if (A[i] > B[i]):
            dist += (A[i] - B[i])
    return dist


def DOM_distance_point_set(A, B):
    B_min = np.min(B, axis=0)
    return DOM_distance(A, B_min)

# eliminate some points already dominated in P and Q
def adjust_P_Q(P, Q):
    nobj = P.shape[1]
    # print('Q is dominated by P:')
    q_dominated_by_p = []
    for q_i, q in enumerate(Q):
        if np.sum(np.sum(np.greater_equal(q, P), axis=1) == nobj) > 0:
            # print(q_i, q)'
            q_dominated_by_p.append(q_i)
    # print('Q is dominated by someone other member o q:')
    q_dominated_by_q = []
    for q_i, q in enumerate(Q):
        if np.sum(np.sum(np.greater(q, Q), axis=1) == nobj) > 0:
            # print(q_i, q)
            q_dominated_by_q.append(q_i)
    # print('P is dominated by someone other member o p:')
    p_dominated_by_p = []
    for p_i, p in enumerate(P):
        if np.sum(np.sum(np.greater(p, P), axis=1) == nobj) > 0:
            # print(p_i, p)
            p_dominated_by_p.append(p_i)
    print('p_dominated_by_p',np.array(p_dominated_by_p).shape)
    print('q_dominated_by_q',np.array(q_dominated_by_q).shape)
    if len(q_dominated_by_p) !=0 and len(q_dominated_by_q) !=0:
        Q = np.delete(Q, np.hstack([q_dominated_by_p, q_dominated_by_q]).tolist(), axis=0)
    elif len(q_dominated_by_p) !=0:
        Q = np.delete(Q, q_dominated_by_p, axis=0)
    elif len(q_dominated_by_q) !=0:
        Q = np.delete(Q, q_dominated_by_q, axis=0)

    if len(p_dominated_by_p) != 0:
        P = np.delete(P, p_dominated_by_p, axis=0)
    return P, Q

###################################################################################################
#Input: P set, Q set, logprint(True or false) if the log should be presented, model_name with the path to save the LP model
#Output: MIP-DoM value, and the P' generated by the method(dictionary with the p index  as key and the coordinates for the P')
###################################################################################################
def compact_mip_dom(P, Q, logprint=True, gapperc=1e-04, model=CBC, model_name='MIPDoMCompact'):
    model = Model(solver_name=model,name=model_name)

    P1, Q1 = adjust_P_Q(P, Q)
    if Q1.shape[0] != 0:
        Q = Q1
    if P1.shape[0] != 0:
        P = P1

    num_P = P.shape[0]
    num_Q = Q.shape[0]
    num_J = P.shape[1]

    ZPO = [ [model.add_var(var_type=CONTINUOUS,name='ZPO_'+str(p)+'_'+str(j)) for j in range(num_J)] for p in range(num_P) ]
    XPQ = [ [model.add_var(var_type=BINARY,name='XPQ_'+str(p)+'_'+str(q)) for q in range(num_Q) ] for p in range(num_P)]

    # objective function

    obj_ZPO = xsum(ZPO[p][j] for j in range(num_J) for p in range(num_P))
    model.objective = minimize(obj_ZPO)
    for p in range(num_P):
        for q in range(num_Q):
            for j in range(num_J):
                model.add_constr( P[p][j] - ZPO[p][j] <= Q[q][j] + (1-XPQ[p][ q])*100000)

    for q in range(num_Q):
        model.add_constr(xsum(XPQ[p] [q] for p in range(num_P)) == 1)

    print('model has {} vars, {} constraints and {} nzs'.format(model.num_cols, model.num_rows, model.num_nz))
    # model.write("/home/model.lp")
    # return 1
    model.max_mip_gap =gapperc

    status = model.optimize()


    p_line_ret = []
    zpq_ret = []
    if status == OptimizationStatus.OPTIMAL:
        if logprint:
            print('model has {} vars, {} constraints and {} nzs'.format(model.num_cols, model.num_rows, model.num_nz))
            print('Total distance = {0:.4f}'.format(model.objective_value))
        all_plines =[]
        for p in range(num_P):
            print_p = True
            if np.sum([XPQ[p][q].x for q in range(num_Q)]) >=1:
                p_actual = []
                for j in range(num_J):
                    p_actual.append(P[p, j] - ZPO[p][j].x)
                p_actual = np.array(p_actual)
                all_plines.append(p_actual)
            if (np.sum([ ZPO[ p ][ j ].x for j in range(num_J) ])) > 0:
                if p not in p_line_ret:
                    p_line_ret.append(p)
                print('Improvement on P%d , total of %5.5f:' % (p + 1, (np.sum([ ZPO[ p ][ j ].x for j in range(num_J) ]))),
                      [ZPO[ p ][ j ].x for j in range(num_J)] )
                for q in range(num_Q):
                    dominance_movement = 0
                    if ((np.sum([ ZPO[ p ][ j ].x for j in range(num_J) ])) > 0):
                        if print_p:
                            print_p = False
                    if XPQ[p][q].x > 0:
                        dominance_movement += (np.sum([ ZPO[ p ][ j ].x for j in range(num_J) ]))
                        if logprint:
                            print('P%d  dominates Q%d, distance of %5.5f:' % (p + 1, q + 1, dominance_movement))

        return model.objective_value,p_line_ret,all_plines

