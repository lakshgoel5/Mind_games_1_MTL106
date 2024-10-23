"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
import numpy as np
M=1000000007

def mod_add(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a+b)%M

def mod_multiply(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return (a*b)%M

def mod_divide(a, b):
    a=(a%M+M)%M
    b=(b%M+M)%M
    return mod_multiply(a, pow(b, M-2, M))

# Problem 3b
def optimal_strategy(na, nb, tot_rounds):
    """
    Calculate the optimal strategy for Alice maximize her points in the future rounds
    given the current score of Alice(na) and Bob(nb) and the total number of rounds(tot_rounds).
    
    Return the answer in form of a list [p1, p2, p3],
    where p1 is the probability of playing Attacking
    p2 is the probability of playing Balanced
    p3 is the probability of playing Defensive
    """
    ans=E(na,nb,tot_rounds)
    # print(ans)
    if(ans[1]==0):
        return [1,0,0]
    elif(ans[1]==1):
        return [0,1,0]
    else:
        return [0,0,1]

def expected_points(tot_rounds):
    """
    Given the total number of rounds(tot_rounds), calculate the expected points that Alice can score after the tot_rounds,
    assuming that Alice plays optimally.

    Return : The expected points that Alice can score after the tot_rounds.
    """
    return 1 + E(1, 1, tot_rounds - 2)[0]



#Function which return expected number of points of allice in next T rounds
def E(alice_wins, bob_wins, T):
    dp = [[[-1 for _ in range(max(alice_wins,bob_wins)+T + 3)] for _ in range(max(bob_wins,alice_wins)+T + 3)] for _ in range(T + 1)]

    return E_dp(alice_wins,bob_wins,T,dp)

def E_dp(alice_wins, bob_wins, T, dp):

    payoff_matrix = np.array([
        [(bob_wins/(bob_wins+alice_wins),0,alice_wins/(alice_wins+bob_wins)), (0.7,0,0.3), (5/11,0,6/11)],  
        [(0.3, 0, 0.7), (1/3,1/3,1/3), (0.3,0.5,0.2)], 
        [(6/11,0,5/11), (0.2,0.5,0.3), (0.1,0.8,0.1)]
        ])

    if(dp[T][alice_wins][bob_wins]!=-1):
        return dp[T][alice_wins][bob_wins]
    if(T==1):
        #Return greedy
        e1=payoff_matrix[0][0][0]*(1)+payoff_matrix[0][0][1]*(0.5)+payoff_matrix[0][0][2]*(0)
        e2=payoff_matrix[0][1][0]*(1)+payoff_matrix[0][1][1]*(0.5)+payoff_matrix[0][1][2]*(0)
        e3=payoff_matrix[0][2][0]*(1)+payoff_matrix[0][2][1]*(0.5)+payoff_matrix[0][2][2]*(0)
        e4=payoff_matrix[1][0][0]*(1)+payoff_matrix[1][0][1]*(0.5)+payoff_matrix[1][0][2]*(0)
        e5=payoff_matrix[1][1][0]*(1)+payoff_matrix[1][1][1]*(0.5)+payoff_matrix[1][1][2]*(0)
        e6=payoff_matrix[1][2][0]*(1)+payoff_matrix[1][2][1]*(0.5)+payoff_matrix[1][2][2]*(0)
        e7=payoff_matrix[2][0][0]*(1)+payoff_matrix[2][0][1]*(0.5)+payoff_matrix[2][0][2]*(0)
        e8=payoff_matrix[2][1][0]*(1)+payoff_matrix[2][1][1]*(0.5)+payoff_matrix[2][1][2]*(0)
        e9=payoff_matrix[2][2][0]*(1)+payoff_matrix[2][2][1]*(0.5)+payoff_matrix[2][2][2]*(0)
        Attack=(1/3)*(e1+e2+e3)
        Balanced=(1/3)*(e4+e5+e6)
        Defence=(1/3)*(e7+e8+e9)
        # print(Attack,Balanced,Defence,"d") 
        if(Attack>Balanced and Attack>Defence):
            dp[T][alice_wins][bob_wins]= Attack
            return (Attack,0)
        elif(Balanced>Attack and Balanced>Defence):
            dp[T][alice_wins][bob_wins]= Attack
            return (Balanced,1)
        else:
            dp[T][alice_wins][bob_wins]= Attack
            return (Defence,2)
    elif(T>0):
        
        
        if(dp[T-1][alice_wins+1][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"a")
            dp[T-1][alice_wins+1][bob_wins]=E_dp(alice_wins+1,bob_wins,T-1,dp)[0]
        if(dp[T-1][alice_wins][bob_wins+1]==-1):
            # print(alice_wins,bob_wins,T,'b')
            dp[T-1][alice_wins][bob_wins+1]=E_dp(alice_wins,bob_wins+1,T-1,dp)[0]
        if (dp[T-1][alice_wins][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"c")
            dp[T-1][alice_wins][bob_wins]=E_dp(alice_wins,bob_wins,T-1,dp)[0]
        e1=payoff_matrix[0][0][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][0][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][0][2]*(dp[T-1][alice_wins][bob_wins+1])
        e2=payoff_matrix[0][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        e3=payoff_matrix[0][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        e4=payoff_matrix[1][0][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][0][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][0][2]*(dp[T-1][alice_wins][bob_wins+1])
        e5=payoff_matrix[1][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        e6=payoff_matrix[1][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        e7=payoff_matrix[2][0][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][0][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][0][2]*(dp[T-1][alice_wins][bob_wins+1])
        e8=payoff_matrix[2][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        e9=payoff_matrix[2][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        Attack=(1/3)*(e1+e2+e3)
        Balanced=(1/3)*(e4+e5+e6)
        Defence=(1/3)*(e7+e8+e9)
        # print(Attack,Balanced,Defence)
        if(Attack>Balanced and Attack>Defence):
            # print("0")
            return (Attack,0)
        elif(Defence>Attack and Defence>Balanced):
            # print("here2")
            return (Defence,2)
        else:
            return (Balanced,1)
        

# optimal_strategy(1,1,30)