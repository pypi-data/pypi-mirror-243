import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

_all_regions_ = [
    'Right-Hippocampus', 'rh.cuneus', 'rh.paracentral', 'lh.supramarginal', 'lh.isthmuscingulate', 
    'rh.postcentral', 'lh.lateralorbitofrontal', 'rh.lateralorbitofrontal', 'lh.rostralanteriorcingulate', 
    'lh.lateraloccipital', 'lh.fusiform', 'rh.fusiform', 'rh.middletemporal', 'lh.lingual', 'lh.parsopercularis', 
    'lh.caudalmiddlefrontal', 'rh.entorhinal', 'Right-Putamen', 'lh.caudalanteriorcingulate', 'lh.superiortemporal', 
    'rh.medialorbitofrontal', 'Left-Putamen', 'lh.parsorbitalis', 'rh.isthmuscingulate', 'Left-Caudate', 
    'Right-Thalamus-Proper', 'rh.posteriorcingulate', 'lh.parstriangularis', 'lh.paracentral', 'lh.superiorparietal', 
    'lh.medialorbitofrontal', 'rh.rostralanteriorcingulate', 'rh.superiorparietal', 'rh.inferiorparietal', 
    'lh.rostralmiddlefrontal', 'rh.parahippocampal', 'lh.middletemporal', 'rh.caudalmiddlefrontal', 'lh.superiorfrontal', 
    'lh.temporalpole', 'rh.parsopercularis', 'rh.superiortemporal', 'rh.caudalanteriorcingulate', 'lh.transversetemporal', 
    'rh.transversetemporal', 'rh.precentral', 'rh.frontalpole', 'lh.entorhinal', 'lh.postcentral', 'lh.insula', 
    'rh.lateraloccipital', 'Brain-Stem', 'rh.precuneus', 'Right-Amygdala', 'Right-Caudate', 'rh.parstriangularis', 
    'Left-Hippocampus', 'rh.supramarginal', 'Left-Thalamus-Proper', 'Left-Accumbens-area', 'rh.rostralmiddlefrontal', 
    'Right-Accumbens-area', 'lh.inferiorparietal', 'lh.frontalpole', 'rh.temporalpole', 'lh.posteriorcingulate', 
    'lh.parahippocampal', 'rh.inferiortemporal', 'lh.inferiortemporal', 'Left-Amygdala', 'lh.bankssts', 'lh.precuneus', 
    'rh.insula', 'rh.lingual', 'rh.parsorbitalis', 'rh.pericalcarine', 'rh.superiorfrontal', 'lh.pericalcarine', 
    'lh.precentral', 'lh.cuneus', 'Right-Pallidum', 'Left-Pallidum', 'rh.bankssts'
    ]


_colors_ = {
# "lh.unknown" :                      (25 , 5  , 25 , 0),
"lh.bankssts" :                     (25 , 100, 40 , 255),
"lh.caudalanteriorcingulate" :      (125, 100, 160, 255),
"lh.caudalmiddlefrontal" :          (100, 25 , 0  , 255),
# "lh.corpuscallosum" :               (120, 70 , 50 , 0),
"lh.cuneus" :                       (220, 20 , 100, 255),
"lh.entorhinal" :                   (220, 20 , 10 , 255),
"lh.fusiform" :                     (180, 220, 140, 255),
"lh.inferiorparietal" :             (220, 60 , 220, 255),
"lh.inferiortemporal" :             (180, 40 , 120, 255),
"lh.isthmuscingulate" :             (140, 20 , 140, 255),
"lh.lateraloccipital" :             (20 , 30 , 140, 255),
"lh.lateralorbitofrontal" :         (35 , 75 , 50 , 255),
"lh.lingual" :                      (225, 140, 140, 255),
"lh.medialorbitofrontal" :          (200, 35 , 75 , 255),
"lh.middletemporal" :               (160, 100, 50 , 255),
"lh.parahippocampal" :              (20 , 220, 60 , 255),
"lh.paracentral" :                  (60 , 220, 60 , 255),
"lh.parsopercularis" :              (220, 180, 140, 255),
"lh.parsorbitalis" :                (20 , 100, 50 , 255),
"lh.parstriangularis" :             (220, 60 , 20 , 255),
"lh.pericalcarine" :                (120, 100, 60 , 255),
"lh.postcentral" :                  (220, 20 , 20 , 255),
"lh.posteriorcingulate" :           (220, 180, 220, 255),
"lh.precentral" :                   (60 , 20 , 220, 255),
"lh.precuneus" :                    (160, 140, 180, 255),
"lh.rostralanteriorcingulate" :     (80 , 20 , 140, 255),
"lh.rostralmiddlefrontal" :         (75 , 50 , 125, 255),
"lh.superiorfrontal" :              (20 , 220, 160, 255),
"lh.superiorparietal" :             (20 , 180, 140, 255),
"lh.superiortemporal" :             (140, 220, 220, 255),
"lh.supramarginal" :                (80 , 160, 20 , 255),
"lh.frontalpole" :                  (100, 0  , 100, 255),
"lh.temporalpole" :                 (70 , 70 , 70 , 255),
"lh.transversetemporal" :           (150, 150, 200, 255),
"lh.insula" :                       (255, 192, 32 , 255),
"Left-Pallidum" :                   (13,  48,  255, 255),
"Left-Accumbens-area" :             (255, 165, 0,   255),
"Left-Amygdala" :                   (103, 255, 255, 255),
"Left-Thalamus-Proper" :            (0,   118, 14,  255),
"Left-Hippocampus" :                (220, 216, 20,  255),
"Left-Caudate" :                    (122, 186, 220, 255),
"Left-Putamen" :                    (236, 13,  176, 255),

# "rh.unknown" :                      (25 , 5  , 25 , 0),
"rh.bankssts" :                     (25 , 100, 40 , 255),
"rh.caudalanteriorcingulate" :      (125, 100, 160, 255),
"rh.caudalmiddlefrontal" :          (100, 25 , 0  , 255),
# "rh.corpuscallosum" :               (120, 70 , 50 , 0),
"rh.cuneus" :                       (220, 20 , 100, 255),
"rh.entorhinal" :                   (220, 20 , 10 , 255),
"rh.fusiform" :                     (180, 220, 140, 255),
"rh.inferiorparietal" :             (220, 60 , 220, 255),
"rh.inferiortemporal" :             (180, 40 , 120, 255),
"rh.isthmuscingulate" :             (140, 20 , 140, 255),
"rh.lateraloccipital" :             (20 , 30 , 140, 255),
"rh.lateralorbitofrontal" :         (35 , 75 , 50 , 255),
"rh.lingual" :                      (225, 140, 140, 255),
"rh.medialorbitofrontal" :          (200, 35 , 75 , 255),
"rh.middletemporal" :               (160, 100, 50 , 255),
"rh.parahippocampal" :              (20 , 220, 60 , 255),
"rh.paracentral" :                  (60 , 220, 60 , 255),
"rh.parsopercularis" :              (220, 180, 140, 255),
"rh.parsorbitalis" :                (20 , 100, 50 , 255),
"rh.parstriangularis" :             (220, 60 , 20 , 255),
"rh.pericalcarine" :                (120, 100, 60 , 255),
"rh.postcentral" :                  (220, 20 , 20 , 255),
"rh.posteriorcingulate" :           (220, 180, 220, 255),
"rh.precentral" :                   (60 , 20 , 220, 255),
"rh.precuneus" :                    (160, 140, 180, 255),
"rh.rostralanteriorcingulate" :     (80 , 20 , 140, 255),
"rh.rostralmiddlefrontal" :         (75 , 50 , 125, 255),
"rh.superiorfrontal" :              (20 , 220, 160, 255),
"rh.superiorparietal" :             (20 , 180, 140, 255),
"rh.superiortemporal" :             (140, 220, 220, 255),
"rh.supramarginal" :                (80 , 160, 20 , 255),
"rh.frontalpole" :                  (100, 0  , 100, 255),
"rh.temporalpole" :                 (70 , 70 , 70 , 255),
"rh.transversetemporal" :           (150, 150, 200, 255),
"rh.insula" :                       (255, 192, 32 , 255),
"Right-Pallidum" :                  (13,  48,  255, 255),
"Right-Accumbens-area" :            (255, 165, 0,   255),
"Right-Amygdala" :                  (103, 255, 255, 255),
"Right-Thalamus-Proper" :           (0,   118, 14,  255),
"Right-Hippocampus" :               (220, 216, 20,  255),
"Right-Caudate" :                   (122, 186, 220, 255),
"Right-Putamen" :                   (236, 13,  176, 255),

"Brain-Stem" :                      (119, 159, 176, 255)
}


# Normalize colors
_colors_ = { key : (R/255., G/255., B/255., A/255.) for key,[R,G,B,A] in _colors_.items() }


class Connectome:
    
    def __init__(self, G_conn, G_prox=None, quantities = None, time = None):
        
        if isinstance(G_conn, str):
            self.G_conn = nx.read_graphml(G_conn)
        else:
            self.G_conn = G_conn

        try:
            weight_test = list(self.G_conn.edges(data=True))[0]
            weight_test[2]["weight"]
            self.G_conn = nx.read_graphml(self.G_conn)
            del weight_test
        except:
            import warnings
            warnings.warn(f"\nWARNING: Graph has no weight attribute. The edge weights will be considered binary.\n", RuntimeWarning)

        self._nodesPosition = None # Use to save processing power in the property
        self.nodes_info = self._relabel_nodes()

        # FOR LOG
        self._elapsed_time = 0
        self.source_region = ['lh.entorhinal', 'rh.entorhinal']
        self._min_max_tau = [0.,0.]
        self._min_max_amyloid = [0.,0.]
        # ----------------------

        self.quantities = quantities
        self.time = time
        self.a = self._get_a_range()
        self.proximity_df = None
        self.G_prox = None

        self.all_regions = list(set([dict(self.G_conn.nodes(data=True))[n]['dn_name'].split("_")[0] for n in self.G_conn.nodes()]))

        
        # ////// Define model parameters //////
        self.r_prox = 12.
        self.CG = 0.1
        self.CS = 0.01
        self.CW = 0.01
        self.CF = 10.
        self.mu0 = 0.01 # in F
        self.U_bar = 0.001 # for u2 in v
        self.d1 = 0.1
        self.d2 = 0.1
        self.dw = 1.
        self.Ck = 1.

        self.alpha = np.ones(shape=(3,3))*10

        self.s1 = 0.1
        self.s2 = 0.1
        self.s3 = 0.1
        self.Cw = 10.
        self.uw = 0.001
        self.s4 = 0.1

        self.Xi = 10.
        self.Lambda = 25.

        self.source_val = 5.

        if G_prox is not None: # If we specified a proximity connectome ..
            if isinstance(G_prox, tuple): # .. if it is a tuple (Graph, radius), then use the radius to create the proximity
                self.r_prox = G_prox[1]
                self.getProximityConnectome(r_max = self.r_prox, G_temp=G_prox[0], weighted=False)
            elif isinstance(G_prox, nx.Graph): # or if it is a networkx object just select that proximity graph as proximity
                self.G_prox=G_prox
            else: # If it is a path to a graphml object, use that to create the proximity (must have the positions of course)
                self.getProximityConnectome(r_max = self.r_prox, G_temp=G_prox, weighted=False)
        
        self.G_cont = None

    @property
    def nodesPosition(self):
        
        if self._nodesPosition is None:
            positions = {k: [self.nodes_info[k][v] for v in ['dn_position_x','dn_position_y','dn_position_z']] \
                                for k in self.nodes_info.keys()}
            self._nodesPosition =  np.vstack(list(positions.values()))

        return self._nodesPosition

    @property
    def proximityConnectome(self):
        if self.G_prox is None:
            self.getProximityConnectome(r_max=self.r_prox)

        return self.G_prox

    @property
    def getAllRegionsWithNodes(self):

        regionsWithNodes = dict()
        for region in _all_regions_:
            regionsWithNodes[region] = self.getNodesInRegion(region).tolist()

        return regionsWithNodes
    

    def printAllParameters(self):

        if self.a is None: # If there is no a, just create a list of nones
            self.a = [None,None]

        output = f""" *--------- Model Parameters ---------*

 - Proximity radius: {self.r_prox} mm
 - Integration time: [{self.time[0]}, {self.time[-1]}] s
 - a range: [{self.a[0]}, {self.a[-1]}]

 - CG: {self.CG}
 - CS: {self.CS}
 - CW: {self.CW}
 - CF: {self.CF}
 - Ck: {self.Ck}
 - mu0: {self.mu0}
 - U_bar: {self.U_bar}
 - d1: {self.d1}
 - d2: {self.d2}
 - dw: {self.dw}
 - s1: {self.s1}
 - s2: {self.s2}
 - s3: {self.s3}
 - s4: {self.s4}
 - Cw: {self.Cw}
 - uw: {self.uw}
 - Xi: {self.Xi}
 - Lambda: {self.Lambda}

 - sources: {self.source_val} # If 'H', then it uses Xi*exp(-t/Lambda)
 - alpha: \n{self.alpha}

*-----------------------------------------------------*
"""
        print(output)


    def saveSimulation(self, path='', suffix='', log = None):

        if self.a is None: # If there is no a, just create a list of nones
            self.a = [None,None]

        np.save(f'{path}time_{suffix}', self.time)
        np.save(f'{path}f_sol_{suffix}', self.quantities[0])
        np.save(f'{path}u1_sol_{suffix}', self.quantities[1])
        np.save(f'{path}u2_sol_{suffix}', self.quantities[2])
        np.save(f'{path}u3_sol_{suffix}', self.quantities[3])
        np.save(f'{path}w_sol_{suffix}', self.quantities[4])

        if log is not None:
            with open(log, 'w') as f:
                f.write(f"####### Simulation {log.split('/')[-1]} ########\n")
                f.write(f""" - GENERALITIES:
 - Brain Graph Nodes: {len(self.G_conn.nodes())}
 - Simulation Elapsed Time: {self._elapsed_time} s
 - Source Nodes Region: {self.source_region}
 - Tau Laplacian Min/Max Values: {self._min_max_tau[0]}/{self._min_max_tau[1]}
 - Amyloid Laplacian Min/Max Values: {self._min_max_amyloid[0]}/{self._min_max_amyloid[1]}

 - NETWORK COMPONENTS:
 - Tau connectome components: {len(self.getNetworkComponents(graph='tau'))}
 - Amyloid connectome components: {len(self.getNetworkComponents(graph='amyloid'))}
CONTINUE..
 
 - Proximity radius: {self.r_prox} mm
 - Integration time: [{self.time[0]}, {self.time[-1]}] s
 - Integration time steps: {len(self.time)}
 - a range: [{self.a[0]}, {self.a[-1]}]
 - a range steps (M): {len(self.a)}

 - CG: {self.CG}
 - CS: {self.CS}
 - CW: {self.CW}
 - CF: {self.CF}
 - Ck: {self.Ck}
 - mu0: {self.mu0}
 - U_bar: {self.U_bar}
 - d1: {self.d1}
 - d2: {self.d2}
 - dw: {self.dw}
 - s1: {self.s1}
 - s2: {self.s2}
 - s3: {self.s3}
 - s4: {self.s4}
 - Cw: {self.Cw}
 - uw: {self.uw}
 - Xi: {self.Xi}
 - Lambda: {self.Lambda}

 - sources: {self.source_val} # If 'H', then it uses Xi*exp(-t/Lambda)
 - alpha: \n{self.alpha}""")
    

    def saveConnectome(self, path : str = ""):
        """
        Save the Connectome object by specifying the save path with also the file name, without any extension. 
        """
        import pickle
        with open(path+'.pkl', 'wb') as connectome:
            pickle.dump(self, connectome, pickle.HIGHEST_PROTOCOL)


    def loadConnectome(path :  str):
        """
        Load the Connectome object by specifying the whole path and the file name. It should be a pickle file.
        """
        import pickle
        with open(path, 'rb') as file:
            return pickle.load(file)


    def getNetworkComponents(self, graph):
        
        if graph == 'tau':
            G = self.G_conn
        elif graph == 'amyloid':
            G = self.G_prox
        else:
            raise ValueError(f"\nERROR: No graph found with name '{graph}'\n")
            
        components = []
        components.append(list(nx.node_connected_component(G, list(G.nodes())[0])))

        for n in list(G.nodes())[1:]:
            
            found = False
            for component in components:
                if n in component:
                    found = True

            if not found:
                components.append(list(nx.node_connected_component(G,n)))

        return components


    def alzheimerModelSimulation(self, seed=10, G_cont=None):

        from scipy.integrate import solve_ivp
        from scipy.integrate import trapezoid

        np.random.seed(seed)

        G_conn = None
        G_prox = None

        if self.G_prox is None:
            try:
                self.getProximityConnectome(self.r_prox)
                G_prox = self.G_prox
            except:
                raise ValueError("\nERROR: The connectome doesn't have spatial information to built the proximity graph.\nPlease specify a graph that has spatial information using 'G_prox' in the constructor.\n")
        else:
            G_prox = self.G_prox

        if self.G_conn is not None:
            G_conn = self.G_conn # If nothing just pass the self.G graph as connectivity connectome
        else:
            raise ValueError("\nERROR: No connectivity connectome selected.\n")

        N = len(self.G_conn.nodes())

        # Get proximity and connection laplacian
        L_prox = nx.laplacian_matrix(G_prox).toarray()
        L_conn = None

        if isinstance(G_cont, str): # Load contagion path
            L_conn = nx.laplacian_matrix(nx.read_graphml(G_cont)).toarray()
            print(f"Using contagion graph at '{G_cont}'..\n")
        elif isinstance(G_cont, nx.Graph): # Load contagion graphml
            print(f"Using contagion graph '{G_cont}'..\n")
            L_conn = nx.laplacian_matrix(G_cont).toarray()
        elif G_cont is None: # Use connection graph
            L_conn = nx.laplacian_matrix(G_conn).toarray()

        M_a0 = len(self.a) # adding a0
        M = M_a0-1 # a variable points without a0
        h_a = 1./M_a0

        # Boundary conditions
        mask = np.ones(N*M_a0, bool)
        mask[::M_a0] = False
        C = np.zeros(N*M_a0)
        C[mask] = 0. # f(a0, t) = 0, for all t

        # Declare variables
        f = np.zeros(N*M)
        u1 = np.zeros(N)
        u2 = np.zeros(N)
        u3 = np.zeros(N)
        w = np.zeros(N)

        # Initial conditions
        u1_0 = np.maximum(np.random.normal(loc=0.5, scale=0.1, size=N),0)
        f[::M] = 1. # f(a1,t0)
        u1[:] = u1_0
        u2[:] = 0.
        u3[:] = 0.
        z0 = np.concatenate([f, u1, u2, u3, w])

        # Get nodes with source
        source_nodes = self.getNodesInRegion(self.source_region)

        # ------- LOG --------
        self._min_max_tau[0], self._min_max_tau[1] = np.min(L_conn), np.max(L_conn)
        self._min_max_amyloid[0], self._min_max_amyloid[1] = np.min(L_prox), np.max(L_prox)
        # --------------------

        w[source_nodes] = 0.
        
        del f, u1, u2, u3, w

        # Time dependent source definition
        def H(t, Xi, Lambda):
            return Xi*np.exp(-t/Lambda)

        # Alpha should be a matrix, since it can be different according to u coupling
        if np.array(self.alpha).size == 1:
            self.alpha = np.ones(shape=(3,3))*self.alpha

        def alzheimerModel(t, y, L_tau, L_abeta, C):

            dydt = np.zeros(N*M+4*N) # Derivative variables
            w_source = np.zeros(N)

            # Choose if to use a time dependent source or a constant one
            if self.source_val == "H":
                w_source[source_nodes] = H(t, Xi=self.Xi, Lambda=self.Lambda)
            else:
                w_source[source_nodes] = self.source_val

            C[mask] = y[:N*M] # The intial condition on a are not entering the derivative. mask avoids their positions

            fv = [C[k*M_a0:(k+1)*M_a0]*(self.CG * np.array([trapezoid(np.maximum(self.a-a_i, 0) * C[k*M_a0:(k+1)*M_a0], self.a) for a_i in self.a]) +\
                  self.CS*(1-self.a)*np.maximum(y[N*M+N:N*M+2*N][k]-self.U_bar,0) + \
                  self.CW*(1-self.a)*y[N*M+3*N:N*M+4*N][k]) for k in range(N)]

            # f
            for k in range(N): # Slide all nodes to assign the M values of a
                dydt[k*M:(k+1)*M] = -(np.diff(fv[k]))/(h_a)

            # u1
            dydt[N*M:N*M+N] = -self.d1*L_abeta @ y[N*M:N*M+N] - y[N*M:N*M+N]*(self.alpha[0,0]*y[N*M:N*M+N]+self.alpha[0,1]*y[N*M+N:N*M+2*N]+self.alpha[0,2]*y[N*M+2*N:N*M+3*N])+\
                              self.CF*np.array([trapezoid((self.mu0+self.a)*(1-self.a)*C[k*M_a0:(k+1)*M_a0], self.a) for k in range(N)])+\
                              -self.s1*y[N*M:N*M+N]
            # u2
            dydt[N*M+N:N*M+2*N] = -self.d2*L_abeta @ y[N*M+N:N*M+2*N] + 0.5*self.alpha[0,0]*y[N*M:N*M+N]*y[N*M:N*M+N]-y[N*M+N:N*M+2*N]*\
                                   (self.alpha[1,0]*y[N*M:N*M+N]+self.alpha[1,1]*y[N*M+N:N*M+2*N]+self.alpha[1,2]*y[N*M+2*N:N*M+3*N])+\
                                   -self.s2*y[N*M+N:N*M+2*N]
            # u3
            dydt[N*M+2*N:N*M+3*N] = 0.5*(self.alpha[0,1]*y[N*M:N*M+N]*y[N*M+N:N*M+2*N]+self.alpha[0,2]*y[N*M:N*M+N]*y[N*M+2*N:N*M+3*N]+\
                                         self.alpha[1,1]*y[N*M+N:N*M+2*N]*y[N*M+N:N*M+2*N]+self.alpha[1,2]*y[N*M+N:N*M+2*N]*y[N*M+2*N:N*M+3*N])+\
                                    -self.s3*y[N*M+2*N:N*M+3*N]
            # w
            dydt[N*M+3*N:N*M+4*N] = (self.Cw*np.maximum(y[N*M+N:N*M+2*N]-self.uw,0) + \
                                    -self.dw*L_tau @ y[N*M+3*N:N*M+4*N] + \
                                    -self.s4*y[N*M+3*N:N*M+4*N] + w_source)

            return dydt
            
        # Integration
        import time as tm
        t1 = tm.perf_counter()
        sol = solve_ivp(alzheimerModel, t_span=[self.time[0], self.time[-1]], t_eval=self.time, y0=z0,
                        method='RK23', args=(L_conn, L_prox, C))
        self._elapsed_time = tm.perf_counter()-t1

        print("\nSimulation compleated.\n")

        # ///// Integrator solutions /////
        f = np.ones(shape=(N*M_a0,len(self.time))) # The initial condition of f is 1 in f(a0,t), so we put ones everywhere for now..
        # .. and here we insert the results each time step.
        for t in range(len(self.time)):
            f[mask,t] = sol.y[:N*M,t]

        self.quantities = [f, sol.y[N*M:N*M+N,:], sol.y[N*M+N:N*M+2*N,:], sol.y[N*M+2*N:N*M+3*N,:], sol.y[N*M+3*N:N*M+4*N,:]]

        del sol


    def setIntegrationTime(self, time):
        """
        Description
        -----------
        Specify the time integration range for the simulation.
        """

        self.time = time

    
    def setA_Range(self, a_range):
        """
        Description
        -----------
        Sepcify the range of a variable. It must be between 0 and 1.
        """

        self.a = a_range


    def insertQuantities(self, quantities, time, a_range):
        """
        Description
        -----------
        Give the quantities to the nodes in the connectome.

        """
        
        self.quantities = quantities
        self.time = time
        self.a = a_range


    def _get_a_range(self) -> np.ndarray:
        """
        Description
        -----------
        Since we know exactly what is the structure of our data, we can determine what is the a range.

        """

        if self.quantities is not None:
            # since solution shape is (val_dim, time), and f_sol is (N*M, time)
            return np.linspace(0,1,int(self.quantities[0].shape[0]/len(self.G_conn.nodes())))
        
        else: return None
    

    def _relabel_nodes(self) -> dict:
        """
        Description
        -----------
        Relabel the nodes as integers from 0 to N-1, so that we always have a corrispondence between
        any node in the network and its position in the adjacency matrix.

        """

        old_keys = list(dict(self.G_conn.nodes(data=True)).keys())
            
        relabel_map = dict()

        for new_key, old_key in enumerate(old_keys):

            relabel_map[old_key] = new_key
        
        # Relabel nodes to integer keeping 1 to 1 corresponence (with -1, so node '22' is associated to 21)
        nx.relabel_nodes(self.G_conn, relabel_map, copy=False)

        # Create auxiliary network so that we can reorder nodes
        H = nx.Graph()
        H.add_nodes_from(sorted(self.G_conn.nodes(data=True)))
        H.add_edges_from(self.G_conn.edges(data=True))

        self.G_conn = H
        del H

        return dict(self.G_conn.nodes(data=True))
    

    def getNodesInRegion(self, region : str) -> list:
        """
        Description
        -----------
        Get the integer ID of the nodes in the specified region.

        """
        # {Region : index} dictionary
        nodes_locations = {reg: self.nodes_info[reg]['dn_name'] for reg in self.nodes_info.keys()}

        # This is consistent because the nodes dictionary above is ORDERED, starting from 0 to N-1!
        nodes_in_region = []
        if isinstance(region, list):
            for reg in region:
                nodes_in_region.extend(list(np.where(np.array([r.split("_")[0] for r in nodes_locations.values()])==reg)[0]))
        else:
            nodes_in_region = list(np.where(np.array([r.split("_")[0] for r in nodes_locations.values()])==region)[0])
        return nodes_in_region
    

    def getProximityConnectome(self, r_max, G_temp=None, weighted=False):
        """
        Description
        -----------
        Generate the proximity connectome of the current graph or a given one. This is possible only if the graph has the positions.

        """
        
        if G_temp is not None: # It can be both a networkx object or a path to a graphml
            G_temp = Connectome(G_conn=G_temp)
            
        if self.proximity_df is None: # If not given, create the proximity dataframe
            N = len(self.G_conn.nodes())

            if G_temp: # If we have G_temp (basically everytime), use the positions of the G_temp graph as node positions
                nodes_position = {k: [G_temp.nodes_info[k][v] for v in ['dn_position_x','dn_position_y','dn_position_z']] \
                                for k in G_temp.nodes_info.keys()}
                for n in self.G_conn.nodes():
                    self.G_conn.nodes[n]['dn_position_x'] = nodes_position[n][0]
                    self.G_conn.nodes[n]['dn_position_y'] = nodes_position[n][1]
                    self.G_conn.nodes[n]['dn_position_z'] = nodes_position[n][2]
            else: # If G_temp is None, use the positions specified in the nodes_info of the current graph.
                nodes_position = {k: [self.nodes_info[k][v] for v in ['dn_position_x','dn_position_y','dn_position_z']] \
                                for k in self.nodes_info.keys()}

            # Create a completely connected graph, whose link weights are the euclidean distance between the nodes
            from scipy.spatial import distance

            p = np.vstack(list(nodes_position.values()))
            distances = distance.cdist(p,p, metric='euclidean').flatten()
            nodes_id = list(nodes_position.keys())
            self.proximity_df = pd.DataFrame({'node1':np.repeat(nodes_id,N), 'node2': np.tile(nodes_id,N), 'weight':distances})
            self.proximity_df = self.proximity_df[self.proximity_df['node1']!=self.proximity_df['node2']]

        # Use copy so we can perform this procedure multiple times in the same run.
        # Drop all the links that are above r_max, and remove self loops (with zero distance).
        df_copy = self.proximity_df.copy()
        df_copy = df_copy[df_copy['weight']<r_max]
        df_copy = df_copy[df_copy['node1']!=df_copy['node2']]
        self.resetProximityDf()

        # Initialize self.G_prox all the times we run this function, cause if we change threshold we want it to change too.
        self.G_prox = nx.Graph()
        # Add all the nodes with info in the G_prox graph
        if G_temp: 
             self.G_prox.add_nodes_from(G_temp.G_conn.nodes(data=True))
        else:
            self.G_prox.add_nodes_from(self.G_conn.nodes(data=True))

        del G_temp # Free space

        # Decide if you want to give a weight to the proximity edges, or just leave them unitary
        if weighted:
            self.G_prox.add_weighted_edges_from(list(df_copy.itertuples(index=False, name=None)))
        else:
            df_copy['weight'] = 1
            self.G_prox.add_weighted_edges_from(list(df_copy.itertuples(index=False, name=None)))

        # Check if the proximity graph has some nodes that are not connected with anything
        if not nx.is_connected(self.G_prox):
            import warnings
            warnings.warn("\nWARNING: The created proximity network is disconnected. You might want to increase the sphere radius.\n", RuntimeWarning)


    def resetProximityDf(self):
        """
        Description
        -----------
        Free space required for proximity csv. It like a cache.

        """

        self.proximity_df = None


    def getAtrophy(self, regions : list = None, numpy_out=False) -> dict:
        """
        Description
        -----------
        Evaluate the atrophy once we have the function 'f' as defined in Tesi's paper.
        We can calculate only in specific regions or globally.
        The dimension of the output will be RxT, with R the number of selected regions (max 83) and T the number of timesteps. 

        """
        
        N = len(self.G_conn.nodes())
        M = len(self.a)

        # Atrophy: this tests that the dimensions are correct, should be Nxt
        atrophy = np.zeros(shape=(int(self.quantities[0].shape[0]/M), self.quantities[0].shape[1]))

        for t in range(len(self.time)):
            atrophy[:,t] = [np.trapz(self.a * self.quantities[0][k*M:(k+1)*M, t], self.a) for k in range(N)]

        if regions is None:
            regions = self.all_regions

        # Define dictionary of atrophy    
        regionsAtrophy = dict()

        nodesToKeep = []
        for reg in regions:
            nodes_in_region = self.getNodesInRegion(region=reg)
            reg_size = len(nodes_in_region)
            for t,_ in enumerate(self.time):
                atrophy[nodes_in_region, t] = np.sum(atrophy[nodes_in_region, t])/reg_size

            # We only need one node, since in the region the atrophy value is averaged
            regionsAtrophy[reg] = atrophy[nodes_in_region[0], :]
            nodesToKeep.extend(nodes_in_region) # In case of numpy_out=True

        # If numpy output is required return this 
        if numpy_out:
            return atrophy[nodesToKeep,:]
        else: # Else the dictionary
            return regionsAtrophy


    def drawConnectome(self, highlight_nodes = None, region = None, links = False,
                        normal_size=40, highlight_size=40, link_size = 0.1, title = 'Connectome'):
        """
        Description
        -----------
        Connectome visualization function. Is it also possible to highlight specific nodes/regions.

        """

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(projection='3d')
        ax.view_init(elev=10, azim=-90)

        for node in self.G_conn.nodes():      
            ax.scatter(self.nodes_info[node]['dn_position_x'],
                       self.nodes_info[node]['dn_position_y'],
                       self.nodes_info[node]['dn_position_z'],
                       marker='o', s=normal_size, color=[(1.,1.,1.,1.)], edgecolors='black')
        if links:
            for n1,n2 in self.G_conn.edges():
                ax.plot([self.nodes_info[n1]['dn_position_x'],self.nodes_info[n2]['dn_position_x']],
                        [self.nodes_info[n1]['dn_position_y'],self.nodes_info[n2]['dn_position_y']],
                        [self.nodes_info[n1]['dn_position_z'],self.nodes_info[n2]['dn_position_z']], 'black', linestyle='-', linewidth=link_size)        
            
        if highlight_nodes is not None:

            if isinstance(highlight_nodes, int):
                highlight_nodes = [highlight_nodes]
            
            plt.title(f'{title}, nodes: {[self.nodes_info[i]["dn_name"] for i in highlight_nodes]}', fontsize=16, fontweight='bold')

            for node in highlight_nodes:
                ax.scatter(self.nodes_info[node]['dn_position_x'], self.nodes_info[node]['dn_position_y'], self.nodes_info[node]['dn_position_z'],
                            marker='o', s=highlight_size, color=[(1.,0.,0.,1.)], edgecolors='black')
           
        elif region is not None:
            highlight_nodes = self.getNodesInRegion(region=region)
            plt.title(f'{title}, Region: {region}', fontsize=16, fontweight='bold')

            for node in highlight_nodes:
                ax.scatter(self.nodes_info[node]['dn_position_x'], self.nodes_info[node]['dn_position_y'], self.nodes_info[node]['dn_position_z'],
                            marker='o', s=highlight_size, color=[(1.,0.,0.,1.)], edgecolors='black')

        else: plt.title(f'{title}', fontsize=16, fontweight='bold')

        ax.set_xlabel('x position', fontsize=12)
        ax.set_ylabel('y position', fontsize=12)
        ax.set_zlabel('z position', fontsize=12)
        plt.grid(alpha=0.4)
        plt.show()
        

    def drawRegions(self, regions, links=True, normal_size = 50, region_size = 50, link_size = 0.1, title = "Connectome"):
        """
        Description
        -----------
        Connectome visualization function for regions. The colors are the ones given by FreeSurfer
        """

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(projection='3d')
        ax.view_init(elev=10, azim=-90)

        if links:
            for n1,n2 in self.G_conn.edges():
                ax.plot([self.nodes_info[n1]['dn_position_x'],self.nodes_info[n2]['dn_position_x']],
                        [self.nodes_info[n1]['dn_position_y'],self.nodes_info[n2]['dn_position_y']],
                        [self.nodes_info[n1]['dn_position_z'],self.nodes_info[n2]['dn_position_z']], 'black', linestyle='-', linewidth=link_size)        
            

        if regions == 'all':
            regions = _all_regions_
            colors = _colors_
        
        colors = [_colors_[reg] for reg in regions] 

        highlighted_nodes = [self.getNodesInRegion(region) for region in regions]
       
        flat = [n for region in highlighted_nodes for n in region]

        for node in [n for n in self.G_conn.nodes() if n not in flat]:
            ax.scatter(self.nodes_info[node]['dn_position_x'], self.nodes_info[node]['dn_position_y'], self.nodes_info[node]['dn_position_z'],
                        marker='o', s=normal_size, color=[(1.,1.,1.,1.)], edgecolors='black')
            
        for ind, highlighted_nodes_sub in enumerate(highlighted_nodes):
            for ind2,node in enumerate(highlighted_nodes_sub):
                
                if ind2==0: # Label only on the first one
                    ax.scatter(self.nodes_info[node]['dn_position_x'], self.nodes_info[node]['dn_position_y'], self.nodes_info[node]['dn_position_z'],
                                marker='o', s=region_size, c=list(colors[ind]), label=regions[ind], edgecolors='black')
                else:
                    ax.scatter(self.nodes_info[node]['dn_position_x'], self.nodes_info[node]['dn_position_y'], self.nodes_info[node]['dn_position_z'],
                                marker='o', s=region_size, c=list(colors[ind]), edgecolors='black')

        plt.legend()
        ax.set_xlabel('x position', fontsize=12)
        ax.set_ylabel('y position', fontsize=12)
        ax.set_zlabel('z position', fontsize=12)
        plt.title(f"{title}", fontsize=16, fontweight='bold')
        plt.grid(alpha=0.4)
        plt.show()


    def drawConnectomeQuantity(self, quantity, visualization = 'spatial', links=False, title='Connectome quantity evaluation'):
        """
        Description
        -----------
        Quantities dynamical visualization on the connectome. The time evolution is the one given to the constructor and has obiously
        to match the simulation points.

        """

        from matplotlib.widgets import Slider

        quantity_copy = quantity.copy()

        maxQuantityValue = np.max(quantity_copy)
        color = (1,1,1,1) # white, changes to balck

        if visualization == 'spatial':
        
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(projection='3d')
            ax.view_init(elev=10, azim=-90)

            scatter_plots = []

            if links:
                for n1,n2 in self.G_conn.edges():

                    ax.plot([self.nodes_info[n1]['dn_position_x'],self.nodes_info[n2]['dn_position_x']],
                            [self.nodes_info[n1]['dn_position_y'],self.nodes_info[n2]['dn_position_y']],
                            [self.nodes_info[n1]['dn_position_z'],self.nodes_info[n2]['dn_position_z']], 'b', linestyle='-', linewidth=0.3)
          
            def update_color(t):

                t = int(t)
                for node, sp in enumerate(scatter_plots):
                    sp.set_color((color[0]*(maxQuantityValue-quantity_copy[node, t])/maxQuantityValue, 
                                  color[1]*(maxQuantityValue-quantity_copy[node, t])/maxQuantityValue, 
                                  color[2]*(maxQuantityValue-quantity_copy[node, t])/maxQuantityValue, 
                                  color[3]))

                    sp.set_edgecolor('black')


            for node in self.G_conn.nodes():
                    
                sp = ax.scatter(self.nodes_info[node]['dn_position_x'],
                                self.nodes_info[node]['dn_position_y'],
                                self.nodes_info[node]['dn_position_z'],
                                marker='o', s=100, edgecolors='black')
                
                scatter_plots.append(sp)

            # Create a slider widget to control the value of val
            t_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
            slider = Slider(t_slider, 'Time [ind]', 0, len(self.time)-1, 0)
            slider.on_changed(update_color)

            ax.set_xlabel('x position', fontsize=12)
            ax.set_ylabel('y position', fontsize=12)
            ax.set_zlabel('z position', fontsize=12)

            plt.grid(alpha=0.4)
            plt.title(f'{title}, time: [{self.time[0], self.time[len(self.time)-1]}]', fontsize=16, fontweight='bold')
            plt.show()

        elif visualization == 'linear':
            
            import matplotlib
            cmap = matplotlib.cm.get_cmap('Reds')
  
            N = len(self.G_conn.nodes())
            sp = plt.scatter([i for i in range(N)], [j for j in quantity_copy[:,0]], vmin=0, vmax=maxQuantityValue,
                                            c=[j for j in quantity_copy[:,0]], s=[20]*N, marker='o', cmap=cmap)

            def update_color(t):

                t = int(t)
                sp.set_offsets(np.column_stack(([i for i in range(N)], [j for j in quantity_copy[:,t]])))
                sp.set_color([cmap(quantity_copy[node,t]/maxQuantityValue) for node in range(N)])


            plt.colorbar(sp) # Draw color bar on the right

            plt.ylim([0, maxQuantityValue+0.05*maxQuantityValue]) # Y axis limit, to keep the initial scale, otherwise it resizes everytime

            plt.title(f'{title}, time: [{self.time[0], self.time[len(self.time)-1]}]', fontsize=16, fontweight='bold')
            plt.xlabel('node id', fontsize=12)
            plt.ylabel('quantity', fontsize=12)
            plt.grid(alpha=0.7)

             # Create a slider widget to control the value of val
            t_slider = plt.axes([0.15, 0.02, 0.65, 0.03])
            slider = Slider(t_slider, 'Time [ind]', 0, len(self.time)-1, 0)
            slider.on_changed(update_color)
            plt.show()


    def drawQuantityInRegions(self, quantitiesDict, timeEvolution=True, links=False, normal_size=100, highlight_size=150, title='Connectome quantity evaluation'):
        """
        Description
        -----------
        Quantities dynamical visualization on the connectome. The time evolution is the one given to the constructor and has obiously
        to match the simulation points.

        """

        from matplotlib.widgets import Slider
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(projection='3d')
        ax.view_init(elev=10, azim=-90)

        scatter_plots = dict()

        # Create empty lists
        for reg in quantitiesDict.keys():
            scatter_plots[reg] = []

        maxQuantityValue = np.max(list(quantitiesDict.values()))

        if links:
            for n1,n2 in self.G_conn.edges():

                ax.plot([self.nodes_info[n1]['dn_position_x'],self.nodes_info[n2]['dn_position_x']],
                        [self.nodes_info[n1]['dn_position_y'],self.nodes_info[n2]['dn_position_y']],
                        [self.nodes_info[n1]['dn_position_z'],self.nodes_info[n2]['dn_position_z']], 'b', linestyle='-', linewidth=0.3)
        
        regNodes = []
        for reg in quantitiesDict.keys():
            regNodes.extend(self.getNodesInRegion(reg))

        remainingNodes = [node for node in self.G_conn.nodes() if node not in regNodes] # Points not considered are white 
        del regNodes

        for node in remainingNodes:
                
            ax.scatter(self.nodes_info[node]['dn_position_x'],
                       self.nodes_info[node]['dn_position_y'],
                       self.nodes_info[node]['dn_position_z'],
                       marker='o', s=normal_size, color=[(1.,1.,1.,1.)], edgecolors='black')
        
        del remainingNodes

        if timeEvolution:

            for region in quantitiesDict.keys():

                for node in self.getNodesInRegion(region=region):
                        
                    sp = ax.scatter(self.nodes_info[node]['dn_position_x'],
                                    self.nodes_info[node]['dn_position_y'],
                                    self.nodes_info[node]['dn_position_z'],
                                    marker='o', s=highlight_size, edgecolors='black')
                    
                    scatter_plots[region].append(sp)

            def update_color(t):

                t = int(t)
                
                for reg, spList in scatter_plots.items():
                    color = _colors_[reg]
                    for sp in spList:
                        sp.set_sizes([highlight_size*(np.tanh(2.3*quantitiesDict[reg][t]/maxQuantityValue -2 ) + 1)])
                        sp.set_color((color[0], color[1], color[2], color[3]*(quantitiesDict[reg][t])/maxQuantityValue))
                        sp.set_edgecolor('black')


            # Create a slider widget to control the value of val
            t_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
            slider = Slider(t_slider, 'Time [ind]', 0, len(self.time)-1, 0)
            slider.on_changed(update_color)

            ax.set_xlabel('x position', fontsize=12)
            ax.set_ylabel('y position', fontsize=12)
            ax.set_zlabel('z position', fontsize=12)

            plt.grid(alpha=0.4)
            plt.title(f'{title}, time: [{self.time[0], self.time[len(self.time)-1]}]', fontsize=16, fontweight='bold')
            plt.show()
        
        else:
            for region, val in quantitiesDict.items():
                color = _colors_[region]
                for node in self.getNodesInRegion(region=region):
                    
                    ax.scatter(self.nodes_info[node]['dn_position_x'],
                               self.nodes_info[node]['dn_position_y'],
                               self.nodes_info[node]['dn_position_z'],
                               marker='o', s=val*highlight_size, 
                               color=(color[0], color[1], color[2], 0.9), edgecolors='black')
                    
            ax.set_xlabel('x position', fontsize=12)
            ax.set_ylabel('y position', fontsize=12)
            ax.set_zlabel('z position', fontsize=12)

            plt.grid(alpha=0.4)
            plt.title(f'{title}', fontsize=16, fontweight='bold')
            plt.show()


    def drawQuantityOverTime(self, quantity, title="Quantity Evaluation", save_path=None, legend=True, **kwargs):
        """
        Draw the line plot for a given quantity over the nodes in the connectome. We can also give the quantity as a dictionary
        having as keys the labels of the lines.
        The keyword arguments are for the matplotlib plot (so points, colors, lines, ..).
        """

        import matplotlib.pyplot as plt
        
        plt.grid(alpha=0.4)
        plt.xlabel("time, a.u", fontsize=16)
        plt.ylabel("quantity", fontsize=16)
        plt.title(f"{title}", fontsize=17, fontweight='bold')

        if isinstance(quantity, dict):
            for reg, values in quantity.items():
                if reg in _colors_.keys():
                    plt.plot(self.time, values, label=reg, color=_colors_[reg], **kwargs)
                else:
                    plt.plot(self.time, values, label=reg, **kwargs)
            if legend: # In case we don't want to draw the legend when giving a dictionary
                plt.legend()
        else:
            for nodequantity in quantity:
                plt.plot(self.time, nodequantity, **kwargs)

        if save_path is None:
            plt.show()
        else:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
            

    def draw_f(self, title = "f Solution", save_path = None):
        """
        Description
        -----------
        f function 3D visualization
        """

        import matplotlib.pyplot as plt

        N = len(self.G_conn.nodes())
        M = len(self.a)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        X, Y = np.meshgrid(self.a, self.time)

        f_surf = np.array([np.mean(self.quantities[0][:,t_ind].reshape(N, M), axis=0) for t_ind, _ in enumerate(self.time)])

        from matplotlib import cm

        plt.title(f'{title}', fontsize=16, fontweight='bold')
        
        ax.plot_surface(X, Y, f_surf, cmap=cm.coolwarm)

        ax.set_xlabel('a')
        ax.set_ylabel('t')
        ax.set_zlabel('f')

        if save_path is None:
            plt.show()
        else:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()


    def drawAvgQuantities(self, title = 'Average quantites evaluation', save_path = None):
        """
        Description
        -----------
        Visualize the average concentration of all the quantities over time in the connectome.

        """
        
        avgu1 = np.mean(self.quantities[1], axis=0)
        avgu2 = np.mean(self.quantities[2], axis=0)
        avgu3 = np.mean(self.quantities[3], axis=0)
        avgw = np.mean(self.quantities[4], axis=0)
        
        plt.plot(self.time, avgu1, '-', label=r'avg $u1$')
        plt.plot(self.time, avgu2, '-', label=r'avg $u2$')
        plt.plot(self.time, avgu3, '-', label=r'avg $u3$')
        plt.plot(self.time, avgw, '-', label=r'avg $w$')
        
        plt.xlabel('Time, a.u.', fontsize=15)
        plt.ylabel(r'$\vec{\varphi}(t)$', fontsize=15)

        plt.title(f'{title}', fontweight='bold', fontsize=16)
        plt.grid(True)
        plt.tight_layout()

        plt.plot([],[], ' ', 
                 label = r'$(u1_{0},u2_{0},u3_{0}, w_{0})$'+f'={np.round([avgu1[0],avgu2[0],avgu3[0],avgw[0]],4)}')
        
        plt.plot([],[], ' ', 
                 label = r'$(u1_{f},u2_{f},u3_{f}, w_{f})$'+f'={np.round([avgu1[-1],avgu2[-1],avgu3[-1],avgw[-1]],4)}')
        plt.legend()

        if save_path is None:
            plt.show()
        else:
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()


    def getPathDistance(self, path):
        """
        Description
        -----------
        Get the Euclidean distance of the specified path. The 'path' argument must be a list of nodes in the Connectome format,
        thus integers. It will retrieve the rows of the nodes representing their spatial positions.
        It's essential to use the required formats, since the nodes ID correspond to the rows positions.

        Parameters
        ----------
        path : list
            Ordered list of the nodes.
        
        Return
        ------
        pathDistance : float
        """

        path = self.nodesPosition[path, :]
        return np.sum(np.linalg.norm(path[i+1]-path[i]) for i in range(len(path)-1))


    def getContagionGraph(self, steps=2, pathDistance=10., neighborhood=None, save : bool = False, path : str = None):
        """
        Description
        -----------
        Create and return the contagion graph associated to the connectome given. In order to create this graph we must have
        the all the nodes positions and the connection graph.

        Parameters
        ----------
        steps : int, optional
            Order of the neighborhood to be used in the contagion graph.
        pathDistance : float
            Maximum path distance treshold to keep the analyzed path.
        neighborhood : str
            Path to the m-order neighborhood in dictionary format. If None, it is created.
        save : bool
            Save the contagion graph in 'graphml' format.
        path : str
            Name of the contagion graph if saved.

        Return
        ------
        nx.Graph : Contagion Graph
        """
        
        import os

        if os.path.isfile(path):
            absPath = os.path.abspath("/".join(path.split("/")[:-1])).replace("\\","/")
            print(f'File "{path.split("/")[-1]}" already exists in path "{absPath}/", returning that file.')
            
            return nx.read_graphml(path)
        
        else:
            if neighborhood:
                neighborhood = Connectome.getNeighborhoods(self.G_conn, steps=steps, save=True, path=neighborhood)
            else:
                neighborhood = Connectome.getNeighborhoods(self.G_conn, steps=steps, save=False)
            
            # Copy in order to avoid removing self loops from the original G
            G_copy = Connectome(self.G_conn) 
            G_copy.G_conn.remove_edges_from(nx.selfloop_edges(G_copy.G_conn))
            
            # First define contagion graph as intersection between connection and proximity
            G_cont = G_copy.G_conn.copy()
            G_cont.remove_edges_from(list(G_cont.edges()))

            # Create list of new edges  
            newEdges = []

            from tqdm import tqdm

            for node in tqdm(G_copy.G_conn.nodes(), desc="Creating Contagion Graph .."):
                
                for neigh in neighborhood[node]["distance_1"]:

                    flag = True
                    newEdgeWeight = 0
                    u = node # Starting node
                    v = None

                    for pathToTarget in neigh[1]: # Go through every node in the neighborhood with all of their paths
                        if G_copy.getPathDistance(pathToTarget) <= pathDistance:
                            
                            if flag:
                                v = pathToTarget[-1] # Last node of the path
                            
                            newEdgeWeight+=nx.path_weight(G_copy.G_conn, pathToTarget, weight='weight') # Add to new weight the current path weight
                            
                            flag = False # To get the link we only need one path
                    
                    if not flag: # If flag is false, then we found at least one good path
                        newEdges.append((u, v, newEdgeWeight))
                
                if steps >= 2:
                    for neigh in neighborhood[node]["distance_2"]:

                        flag = True
                        newEdgeWeight = 0
                        u = node # Starting node
                        v = None

                        for pathToTarget in neigh[1]: # Go through every node in the neighborhood with all of their paths
                            if G_copy.getPathDistance(pathToTarget) <= pathDistance:
                                
                                if flag:
                                    v = pathToTarget[-1] # Last node of the path
                                
                                newEdgeWeight+=nx.path_weight(G_copy.G_conn, pathToTarget, weight='weight') # Add to new weight the current path weight
                                
                                flag = False # To get the link we only need one path
                        
                        if not flag: # If flag is false, then we found at least one good path
                            newEdges.append((u, v, newEdgeWeight))

                if steps >= 3:
                    for neigh in neighborhood[node]["distance_3"]:

                        flag = True
                        newEdgeWeight = 0
                        u = node # Starting node
                        v = None

                        for pathToTarget in neigh[1]: # Go through every node in the neighborhood with all of their paths
                            if G_copy.getPathDistance(pathToTarget) <= pathDistance:
                                
                                if flag:
                                    v = pathToTarget[-1] # Last node of the path
                                
                                newEdgeWeight+=nx.path_weight(G_copy.G_conn, pathToTarget, weight='weight') # Add to new weight the current path weight
                                
                                flag = False # To get the link we only need one path
                        
                        if not flag: # If flag is false, then we found at least one good path
                            newEdges.append((u, v, newEdgeWeight))

            # Add all found edges to contagion graph
            G_cont.add_weighted_edges_from(newEdges)

            if save:
                print(f"Contagion graph (steps={steps}, pathDistance={pathDistance}) saved at '{path}'")
                nx.write_graphml(G_cont, path)

            self.G_cont = G_cont

            return self.G_cont


    # STAND-ALONE FUNCTIONS

    def BFS(G : nx.Graph, u, steps : int):
        """
        Description
        -----------
        Breadth-first search Algorithm to find the nodes that are distant 'steps' steps from the current node 'u' given
        a generic network 'G'.
        This also returns all the simple paths from the current node 'u' and the ones at the specified distance.

        Parameters
        ----------
        G : nx.Graph
            Generic networkx.Graph object containing the network.
        u : any
            Node from where to start the search. It should be the networkx node ID (generally ints or strings).
        steps : int
            Number of steps required to find the nodes from the current one 'u'.
        
        Return
        ------
        result : list
            List of tuples, containing the sequence starting node and all the simple paths to the other nodes.
        """
        visited = set()
        queue = [(u, 0)] # Starting node / Distance from it (so it's zero)
        nodesAtDistance = set()
        result = []

        while queue: # Keep looping until queue is empty
            
            node, currentDistance = queue.pop(0) # Remove element from queue .. 
            visited.add(node) # .. and put it in visited

            if currentDistance == steps: # Add elements only if they are at the required distance
                nodesAtDistance.add(node) # Add node at required distance with also the weight

            if currentDistance < steps:
                neighbors = list(G[node].keys())

                for neighbor in neighbors: # Iterate over all the nodes in the neighborhood of the current node ..
                    if neighbor not in visited and neighbor not in [item[0] for item in queue]: # .. and add the node to the queue if is not in visited nor in the queue
                        queue.append((neighbor, currentDistance + 1))
        
        # Put all existing paths from node u to n
        for n in nodesAtDistance:
            result.append((n, list(nx.all_simple_paths(G, source=u, target=n, cutoff=steps))))#nx.shortest_path(G, source=u, target=n, method='dijkstra')))

        return result
    

    def getNeighborhoods(G : nx.Graph, steps : int, save : bool = True, path : str = None):
        """
        Description
        -----------
        Get the m-order neighborhood of all the nodes in the network as a dictionary of paths.

        Parameters
        ----------
        G : nx.Graph
            Generic networkx.Graph object containg the network.
        steps : int
            Order of the neighborhood. How much you want to go deep in the search.
        save : bool, optional
            Save neighborhood once created. The file is saved in pickle format.
        path : str, optional
            Specify path where to save the neighborhood.

        Return
        ------
        pathsUpToM : dict
            Dictionary containing all the m-order neighborhoods up to 'steps' of all the nodes in the graph.
        """

        import os
        import pickle
        from tqdm import tqdm
        
        if path is None:
            path = f"./{steps}-orderNeighborhood.pkl"

        if save and os.path.isfile(path):  
            absPath = os.path.abspath("/".join(path.split("/")[:-1])).replace("\\","/")
            print(f'File "{path.split("/")[-1]}" already exists in path "{absPath}/", returning that file.')

            with open(path, 'rb') as f:
                pathsUpToM = pickle.load(f)

            return pathsUpToM # Nothing is executed after this
            
        pathsUpToM = dict()
        for node in G.nodes():
            pathsUpToM[node] = {}

        for node in tqdm(G.nodes(), desc=f"Generating {steps}-order neighborhood .."):
            for distance in range(1, steps+1):
                pathsUpToM[node].update({f"distance_{distance}" : Connectome.BFS(G, node, steps=distance)})
        
        if save:
            absPath = os.path.abspath("/".join(path.split("/")[:-1])).replace("\\","/")
            print(f'Saving file "{path.split("/")[-1]}" in path "{absPath}/".')
            with open(path, 'wb') as f:
                pickle.dump(pathsUpToM, f)

        return pathsUpToM
