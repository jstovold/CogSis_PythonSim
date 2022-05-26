#include "cmm.h"

//    bool *M;
//    public:
//        short numInputs;
//        short numOutputs;
//    
//        
//        CMM(short numInputs, short numOutputs);
//        ~CMM();
//        void addAssociation(bool* Ik, bool* Ok);
//        short* recall(bool* Ir);
//        bool* thresholdResults(short* O, short theta);
//        bool* invertVector(bool* v);

    CMM::CMM(short numIn, short numOut)
    {
        numInputs   = numIn;
        numOutputs  = numOut;
        M = new bool[numInputs * numOutputs];
        for (int i = 0; i < numInputs * numOutputs; i++)
        {
            M[i] = false;
        }
    }
    
    CMM::~CMM()
    {
        delete [] M;
        delete M;
    }
    
    void CMM::addAssociation(bool* Ik, bool* Ok)
    {
        for (int i = 0; i < numInputs; i++)
        {
            if (Ik[i] == true)
            {
                for (int o = 0; o < numOutputs; o++)
                {
                    if (Ok[o] == true)
                    {
                        M[i * numOutputs + o] = true;
                    }
                }
            }
        }
    }
    
    
    void CMM::recall(short* Ir, short outputArr[])
    {
//        short outputArr[numOutputs];
        for (int o = 0; o < numOutputs; o++)
        {
            int sum = 0;
            for (int i = 0; i < numInputs; i++)
            {
                sum += Ir[i] * M[i * numOutputs + o];
//                if (Ir[i] * M[i * numOutputs + o])
//                {
//                    sum++;
//                }
            }
            outputArr[o] = sum;
        }
//        return &outputArr[0];
    //  let Irow (list Ir)
    //  let Im matrix:from-row-list Irow
    //  let O matrix:times Im M
    //  report first matrix:to-row-list O

    }
    
    void CMM::thresholdResults(short* O, short theta, bool invert, bool outputArr[])
    {
        if (!invert)
        {
            for (int o = 0; o < numOutputs; o++)
            {
                if (O[o] >= theta)
                {
                    outputArr[o] = true;
                }
                else
                {
                    outputArr[o] = false;
                }
            }
        }
        else
        {
            for (int o = 0; o < numOutputs; o++)
            {
                if (O[o] <= -theta)
                {
                    outputArr[o] = true;
                }
                else
                {
                    outputArr[o] = false;
                }
            }
        }
            
    }
    
    void CMM::invertVectorInPlace(bool* v)
    {
        for (int o = 0; o < numOutputs; o++)
        {
            v[o] = v[o] xor 1;
        }
//        return &v[0];
    }
    
