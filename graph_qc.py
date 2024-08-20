from qiskit import *
import qiskit.quantum_info as qi
import numpy as np
from numpy import pi, sin, cos, sqrt, exp
import math
from qiskit.circuit import Parameter

def givens(p,q,theta):
    matrix = np.eye(4)
    matrix[p][p] = np.cos(theta/2)
    matrix[p][q] = np.sin(theta/2)
    matrix[q][p] = -np.sin(theta/2)
    matrix[q][q] = np.cos(theta/2)

    return matrix
def givens_qc(p,q,theta):
    qc = QuantumCircuit(2)
    if p > q:
        temp = p
        p = q
        q = temp
    if p == 0 and q == 1:
        qc.x(1)
        qc.cry(theta,1,0)
        qc.x(1)

    elif p ==0 and q ==2:
        qc.x(0)
        qc.cry(theta,0,1)
        qc.x(0)

    elif p ==0 and q ==3:
        qc.x(1)
        qc.cx(1,0)
        qc.cry(theta,1,0)
        qc.cx(1,0)
        qc.x(1)

    elif p ==1 and q ==2:
        qc.cx(1,0)
        qc.cry(theta,0,1)
        qc.cx(1,0)
        
    elif p ==1 and q ==3:
       
        qc.cry(theta,0,1)
     
        
    elif p ==2 and q ==3:
       
        qc.cry(theta,1,0)
    a = qc
    return a
def flip(p,q):
    matrix = np.eye(4)
    matrix[p][p] = 0
    matrix[q][q] = 0
    matrix[p][q] = 1
    matrix[q][p] = 1
    qc = QuantumCircuit(2)
    mat = qi.Operator(matrix)
    qc.unitary(mat,[0,1])
    return qc
def apply_cg(cg,bin,index,label):
    qc = QuantumCircuit(len(bin))
    if label == "lower":
        if(index == len(bin)-1):
            c_list = list(range(2,len(bin)))
            t_list = [0,1]
            qubit_list = c_list + t_list
            for i in range(len(bin)-2):
                if bin[i] == "0":
                    qc.x(len(bin)-i-1)
            qc.append(cg,qubit_list)
            for i in range(len(bin)-2):
                if bin[i] == "0":
                    qc.x(len(bin)-i-1)

        else:
            # index = 2 c[]
            #clist = [0,3,4]
            #tlist = [1,2]
            #0,1,2,3,4
            #4,3,2,1,0
            q_index = len(bin) - index -1
            if q_index-1 == 0:
                c_list = list(range(q_index+1, len(bin)))
            elif q_index == len(bin) -1:
                c_list = list(range(0,q_index-1))
            else:
                c_list_1 = list(range(0,q_index-1))
                c_list_2 = list(range(q_index+1,len(bin)))
                c_list = c_list_1 + c_list_2
            t_list = [q_index-1,q_index]
            qubit_list = c_list + t_list
          
            for i in range(len(bin)):
                if i != index and i != index + 1:
                    if bin[i] == "0":
                        qc.x(len(bin)-i-1)
            qc.append(cg,qubit_list)
            for i in range(len(bin)):
                if i != index and i != index + 1:
                    if bin[i] == "0":
                        qc.x(len(bin)-i-1)


    elif label == "upper":
        if(index == 0):
            t_list = [len(bin)-2, len(bin)-1]
            c_list = list(range(0,len(bin)-2))
            qubit_list = c_list + t_list
            for i in range(index+2,len(bin)):
                if bin[i] == "0":
                    qc.x(len(bin)-i-1)
            qc.append(cg,qubit_list)
            for i in range(index+2,len(bin)):
                if bin[i] == "0":
                    qc.x(len(bin)-i-1)
        else:
            # index = 1 c[]
            #clist = [0,1,2]
            #tlist = [3,4]
            #0,1,2,3,4
            #4,3,2,1,0
            q_index = len(bin) - index -1
            if q_index == 0:
                c_list = list(range(q_index+2,len(bin)))
            elif q_index + 1 == len(bin)-1:
                c_list = list(range(0,q_index))
            else:
                c_list_1 = list(range(0,q_index))
                c_list_2 = list(range(q_index+2,len(bin)))
                c_list = c_list_1 + c_list_2
            t_list = [q_index,q_index + 1]
            qubit_list = c_list + t_list
            for i in range(len(bin)):
                if i != index and i != index -1:
                    if bin[i] == "0":
                        qc.x(len(bin)-i-1)
            qc.append(cg,qubit_list)
            for i in range(len(bin)):
                if i != index and i != index - 1:
                    if bin[i] == "0":
                        qc.x(len(bin)-i-1)
    return qc

def add_lower(bin,index,last):
    '''
    CX1.decompose().to_instruction()
    new_CX1=CX1.control(2)

    qc.x(0)
    qc.append(new_CX1,[0,1,2,3,4])
    qc.x(0)
    '''
    qc = QuantumCircuit(len(bin))
    theta = Parameter('theta')
   
    if(index == len(bin)-1):
        # 0->1
        if bin[index] == "0" and bin[index-1] == "0":  
            bin[index] = "1"
            if last == 1:
                g = flip(0,1)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(0,1,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
        # 2->3
        elif bin[index] == "0" and bin[index-1] == "1":
            bin[index] = "1"
            if last == 1:
                g = flip(2,3)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(2,3,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
        # 1->2
        elif bin[index] == "1" and bin[index-1] == "0":
            bin[index] = "0"
            if last == 1:
                g = flip(1,2)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(1,2,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
        # 3->2
        elif bin[index] == "1" and bin[index-1] == "1":
            bin[index] ="0"
            if last == 1:
                g = flip(3,2)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(3,2,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
    else:
        # 0->2
        if bin[index] == "0" and bin[index+1] == "0":
            bin[index] = "1"
            if last == 1:
                g = flip(0,2)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(0,2,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
        # 1->3
        elif bin[index] == "0" and bin[index+1] == "1":
            bin[index] = "1"
            if last == 1:
                g = flip(1,3)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(1,3,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
        # 2->1
        elif bin[index] == "1" and bin[index+1] == "0":
            bin[index] = "0"
            bin[index+1] ="1"
            if last == 1:
                g = flip(2,1)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(2,1,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
        # 3->0
        elif bin[index] == "1" and bin[index+1] == "1":
            bin[index] = "0"
            bin[index+1] = "0"
            if last == 1:
                g = flip(3,0)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
            else:
                g = givens_qc(3,0,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"lower")
    return bin, qc

def add_upper(bin,index,last):
    qc = QuantumCircuit(len(bin))
    theta = Parameter('theta')
    if(index == 0):
        # 0->2
        if bin[index] == "0" and bin[index+1] == "0":
            bin[index] = "1"
            if last == 1:
                g = flip(0,2)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(0,2,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
        # 1->3
        elif bin[index] == "0" and bin[index+1] == "1":
            bin[index] = "1"
            if last == 1:
                g = flip(1,3)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(1,3,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
        # 2->0
        elif bin[index] == "1" and bin[index+1] == "0":
            bin[index] = "0"
            if last == 1:
                g = flip(2,0)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(2,0,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
        # 3->1
        elif bin[index] == "1" and bin[index+1] == "1":
            bin[index] ="0"
            if last == 1:
                g = flip(3,1)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(3,1,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
    else:
        # 0->1
        if bin[index] == "0" and bin[index-1] == "0":
            bin[index] = "1"
            if last == 1:
                g = flip(0,1)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(0,1,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
        # 2->3
        elif bin[index] == "0" and bin[index-1] == "1":
            bin[index] = "1"
            if last == 1:
                g = flip(2,3)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(2,3,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
        # 1->2
        elif bin[index] == "1" and bin[index-1] == "0":
            bin[index] = "0"
            bin[index-1] ="1"
            if last == 1:
                g = flip(1,2)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(1,2,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
        # 3->0
        elif bin[index] == "1" and bin[index-1] == "1":
            bin[index] ="0"
            bin[index-1] ="0"
            if last == 1:
                g = flip(3,0)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
            else:
                g = givens_qc(3,0,np.pi)
                cg = g.control(len(bin)-2)
                qc = apply_cg(cg,bin,index,"upper")
    return bin, qc
def list_to_string(list):
    converted_list = map(str, list)
    result = ''.join(converted_list)
   
    #print(result)
    return result
    
def transition(p,q,N):
    #l = max(len(np.binary_repr(p)),len(np.binary_repr(q)))
    l = N
    b_p = list(np.binary_repr(p,width = l))
    b_q = list(np.binary_repr(q,width = l))
    #print(b_p)
    #print(b_q)

    qc = QuantumCircuit(l)
    qubits = list(range(0,l))

    
    #print(int(list_to_string(b_p),2))
    #print(int(list_to_string(b_q),2))
    dif = int(list_to_string(b_q),2) - int(list_to_string(b_p),2)
    #print(dif)
    stack = []
    while(dif!=0):
        temp = b_p
        if dif < 0:
            dif = -dif
            '''
            if dif == 1:
                if b_p[l-1] == "0":
                    b_p[l-1] = "1"
                   
                elif b_p[l-1] == "1":
                    b_p[l-1] = "0"   
            else:
            '''
            index = l - math.ceil(math.log2(dif)) -1
            #print(index)
            b_p,cg= add_lower(b_p,index,0)
            stack.append(cg)
            
            #print(b_p)
            dif = int(list_to_string(b_q),2) - int(list_to_string(b_p),2)
            if dif == 0:
                b_p,cg = add_lower(temp,index,1)
                stack.pop()
                stack.append(cg)
            qc.append(cg,qubits)

        else:
            index = l - math.floor(math.log2(dif)) -1
            #print(index)
            '''
            if(index == 0):
                if b_p[0] == "0":
                    b_p[0] = "1"
            
                elif b_p[0] == "1":
                    b_p[0] = "0"
                   
            else:
            '''
            b_p,cg = add_upper(b_p,index,0)
            stack.append(cg)
            
            #print(b_p)  
            dif = int(list_to_string(b_q),2) - int(list_to_string(b_p),2)
            if dif == 0:
                b_p,cg = add_upper(temp,index,1)
                stack.pop()
                stack.append(cg)
            qc.append(cg,qubits)
        #print(dif)

    return qc, stack
            