
// Correlation Matrix Memory class
//
// The training set consists of k Input-Output pairs, {Ik, Ok}, which are logical-OR'd together to form the corresponding 
// associations in M.
//
//
//
//  [    ]  [             ]
//  [    ]  [             ]
//  [ Ik ]  [      M      ]
//  [    ]  [             ]
//  [    ]  [             ]
//  [    ]  [             ]
//                         
//          [      Ok     ]
//
// As the k Input-Output pairs are presented to the network, building up the associations in the matrix, M.
// Upon recall, we get: O = MIr, where Ir is the input pattern, and O is the output from the network trained with M.
// The desired output pattern, Or, is currently combined with noise from other patterns stored in the network, er, hence:
//     O = Or + er
//    er = sum_{k=1;k!=r}^N (I^T_k.I_r).Ok
// By thresholding the output, O, to an appropriate (!) level, we can retrieve the desired output pattern, Or.
//
#ifndef __CMM_H
#define __CMM_H

class CMM
{
    // association matrix    
    bool *M;
    public:
        short numInputs;
        short numOutputs;
    
        CMM(short numInputs, short numOutputs);
        ~CMM();
        void addAssociation(bool* Ik, bool* Ok);
        void recall(short* Ir, short outputVec[]);
        void thresholdResults(short* O, short theta, bool invert, bool outputVec[]);
        void invertVectorInPlace(bool* v);
        
};
#endif


