import numpy as np

class Alice:
    def __init__(self):
        self.past_play_styles = np.array([1,1])  
        self.results = np.array([1,0])           
        self.opp_play_styles = np.array([1,1])  
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round. If you think there is no better strategy than 2a,
        then implement the same strategy here. Else implement that non greedy strategy here.
        
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        t=100
        ans=E(self.points,len(self.results)-self.points,t)
        if(self.result[-1]==0):
            return ans[2]
        elif(self.result[-1]==0.5):
            return ans[1]
        else:
            return ans[0]
        
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Alice's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        self.past_play_styles=np.append(self.past_play_styles, own_style)
        self.results=np.append(self.results,result)
        self.opp_play_styles=np.append(self.opp_play_styles, opp_style)
        self.points+=result
       

class Bob:
    def __init__(self):
        # Initialize numpy arrays to store Bob's past play styles, results, and opponent's play styles
        self.past_play_styles = np.array([1,1]) 
        self.results = np.array([0,1])          
        self.opp_play_styles = np.array([1,1])   
        self.points = 1

    def play_move(self):
        """
        Decide Bob's play style for the current round.

        Returns: 
            Returns: 
            0 : attack
            1 : balanced
            2 : defence
        
        """
        if self.results[-1] == 1:
            return 2
        elif self.results[-1] == 0.5:
            return 1
        else:  
            return 0
        
        
    
    def observe_result(self, own_style, opp_style, result):
        """
        Update Bob's knowledge after each round based on the observed results.
        
        Returns:
            None
        """
        self.past_play_styles=np.append(self.past_play_styles, own_style)
        self.results=np.append(self.results,result)
        self.opp_play_styles=np.append(self.opp_play_styles, opp_style)
        self.points+=result
 

def simulate_round(alice, bob, payoff_matrix):
    """
    Simulates a single round of the game between Alice and Bob.
    
    Returns:
        None
    """
    prob = payoff_matrix[alice.play_move()][bob.play_move()]

    rand_val = np.random.uniform(0,1)

    if rand_val < prob[0]:  # Alice wins
        alice.observe_result(alice.play_move(), bob.play_move(), 1)
        bob.observe_result(bob.play_move(), alice.play_move(), 0)
        # print(alice.points,bob.points)
        return 1
    elif rand_val < prob[0] + prob[1]:  # Draw
        alice.observe_result(alice.play_move(), bob.play_move(), 0.5)
        bob.observe_result(bob.play_move(), alice.play_move(), 0.5)
        # print(alice.points,bob.points)
        return 0.5
    else:  # Bob wins
        alice.observe_result(alice.play_move(), bob.play_move(), 0)
        bob.observe_result(bob.play_move(), alice.play_move(), 1)
        # print(alice.points,bob.points)
        return 0
    


def monte_carlo(num_rounds):
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    alice=Alice()
    bob=Bob()
    payoff_matrix = np.array([
        [(bob.points/(bob.points+alice.points),0,alice.points/(alice.points+bob.points)), (0.7,0,0.3), (5/11,0,6/11)],  
        [(0.3, 0, 0.7), (1/3,1/3,1/3), (0.3,0.5,0.2)], 
        [(6/11,0,5/11), (0.2,0.5,0.3), (0.1,0.8,0.1)]])
    for i in range(10**5):
        simulate_round(alice,bob,payoff_matrix)
    return alice.points,bob.points
def E(alice_wins, bob_wins, T):
    dp_a = [[[-1 for _ in range(max(alice_wins,bob_wins)+T + 3)] for _ in range(max(bob_wins,alice_wins)+T + 3)] for _ in range(T + 1)]
    dp_b = [[[-1 for _ in range(max(alice_wins,bob_wins)+T + 3)] for _ in range(max(bob_wins,alice_wins)+T + 3)] for _ in range(T + 1)]
    dp_d = [[[-1 for _ in range(max(alice_wins,bob_wins)+T + 3)] for _ in range(max(bob_wins,alice_wins)+T + 3)] for _ in range(T + 1)]
    return E_dp_a(alice_wins,bob_wins,T,dp_a,dp_b,dp_d),E_dp_b(alice_wins,bob_wins,T,dp_a,dp_b),E_dp_d(alice_wins,bob_wins,T,dp_a,dp_b,dp_d)

def E_dp_a(alice_wins, bob_wins, T, dp_a,dp_b,dp_d):

    payoff_matrix = np.array([
        [(bob_wins/(bob_wins+alice_wins),0,alice_wins/(alice_wins+bob_wins)), (0.7,0,0.3), (5/11,0,6/11)],  
        [(0.3, 0, 0.7), (1/3,1/3,1/3), (0.3,0.5,0.2)], 
        [(6/11,0,5/11), (0.2,0.5,0.3), (0.1,0.8,0.1)]
        ])

    if(dp_a[T][alice_wins][bob_wins]!=-1):
        return dp_a[T][alice_wins][bob_wins]
    if(T==0):
        #Return greedy
        # e1=payoff_matrix[0][0][0]*(1)+payoff_matrix[0][0][1]*(0.5)+payoff_matrix[0][0][2]*(0)
        # e2=payoff_matrix[0][1][0]*(1)+payoff_matrix[0][1][1]*(0.5)+payoff_matrix[0][1][2]*(0)
        # e3=payoff_matrix[0][2][0]*(1)+payoff_matrix[0][2][1]*(0.5)+payoff_matrix[0][2][2]*(0)
        # e4=payoff_matrix[1][0][0]*(1)+payoff_matrix[1][0][1]*(0.5)+payoff_matrix[1][0][2]*(0)
        # e5=payoff_matrix[1][1][0]*(1)+payoff_matrix[1][1][1]*(0.5)+payoff_matrix[1][1][2]*(0)
        # e6=payoff_matrix[1][2][0]*(1)+payoff_matrix[1][2][1]*(0.5)+payoff_matrix[1][2][2]*(0)
        # e7=payoff_matrix[2][0][0]*(1)+payoff_matrix[2][0][1]*(0.5)+payoff_matrix[2][0][2]*(0)
        # e8=payoff_matrix[2][1][0]*(1)+payoff_matrix[2][1][1]*(0.5)+payoff_matrix[2][1][2]*(0)
        # e9=payoff_matrix[2][2][0]*(1)+payoff_matrix[2][2][1]*(0.5)+payoff_matrix[2][2][2]*(0)
        # Attack=(1/3)*(e1+e2+e3)
        # Balanced=(1/3)*(e4+e5+e6)
        # Defence=(1/3)*(e7+e8+e9)
        # # print(Attack,Balanced,Defence,"d") 
        # if(Attack>Balanced and Attack>Defence):
        #     dp_a[T][alice_wins][bob_wins]= Attack
        #     return (Attack,0)
        # elif(Balanced>Attack and Balanced>Defence):
        #     dp_a[T][alice_wins][bob_wins]= Attack
        #     return (Balanced,1)
        # else:
        #     dp_a[T][alice_wins][bob_wins]= Attack
        #     return (Defence,2)
        return 0
        
    elif(T>0):
        if(dp_a[T-1][alice_wins+1][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"a")
            dp_a[T-1][alice_wins+1][bob_wins]=E_dp_a(alice_wins+1,bob_wins,T-1,dp_a,dp_b,dp_d)
        if(dp_a[T-1][alice_wins][bob_wins+1]==-1):
            # print(alice_wins,bob_wins,T,'b')
            dp_a[T-1][alice_wins][bob_wins+1]=E_dp_a(alice_wins,bob_wins+1,T-1,dp_a,dp_b,dp_d)
        if (dp_a[T-1][alice_wins][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"c")
            dp_a[T-1][alice_wins][bob_wins]=E_dp_a(alice_wins,bob_wins,T-1,dp_a,dp_b,dp_d)
        e1=payoff_matrix[0][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[0][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e2=payoff_matrix[0][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        # e3=payoff_matrix[0][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        e4=payoff_matrix[1][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[1][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e5=payoff_matrix[1][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        # e6=payoff_matrix[1][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        e7=payoff_matrix[2][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[2][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e8=payoff_matrix[2][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        # e9=payoff_matrix[2][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        Attack=e1
        Balanced=e4
        Defence=e7
        # print(Attack,Balanced,Defence)
        if(Attack>Balanced and Attack>Defence):
            print("0")
            return (Attack,0)
        elif(Defence>Attack and Defence>Balanced):
            print("here2")
            return (Defence,2)
        else:
            return (Balanced,1)
        
def E_dp_b(alice_wins, bob_wins, T, dp_a,dp_b,dp_d):

    payoff_matrix = np.array([
        [(bob_wins/(bob_wins+alice_wins),0,alice_wins/(alice_wins+bob_wins)), (0.7,0,0.3), (5/11,0,6/11)],  
        [(0.3, 0, 0.7), (1/3,1/3,1/3), (0.3,0.5,0.2)], 
        [(6/11,0,5/11), (0.2,0.5,0.3), (0.1,0.8,0.1)]
        ])

    if(dp_b[T][alice_wins][bob_wins]!=-1):
        return dp_b[T][alice_wins][bob_wins]
    if(T==0):
        #Return greedy
        # e1=payoff_matrix[0][0][0]*(1)+payoff_matrix[0][0][1]*(0.5)+payoff_matrix[0][0][2]*(0)
        # e2=payoff_matrix[0][1][0]*(1)+payoff_matrix[0][1][1]*(0.5)+payoff_matrix[0][1][2]*(0)
        # e3=payoff_matrix[0][2][0]*(1)+payoff_matrix[0][2][1]*(0.5)+payoff_matrix[0][2][2]*(0)
        # e4=payoff_matrix[1][0][0]*(1)+payoff_matrix[1][0][1]*(0.5)+payoff_matrix[1][0][2]*(0)
        # e5=payoff_matrix[1][1][0]*(1)+payoff_matrix[1][1][1]*(0.5)+payoff_matrix[1][1][2]*(0)
        # e6=payoff_matrix[1][2][0]*(1)+payoff_matrix[1][2][1]*(0.5)+payoff_matrix[1][2][2]*(0)
        # e7=payoff_matrix[2][0][0]*(1)+payoff_matrix[2][0][1]*(0.5)+payoff_matrix[2][0][2]*(0)
        # e8=payoff_matrix[2][1][0]*(1)+payoff_matrix[2][1][1]*(0.5)+payoff_matrix[2][1][2]*(0)
        # e9=payoff_matrix[2][2][0]*(1)+payoff_matrix[2][2][1]*(0.5)+payoff_matrix[2][2][2]*(0)
        # Attack=(1/3)*(e1+e2+e3)
        # Balanced=(1/3)*(e4+e5+e6)
        # Defence=(1/3)*(e7+e8+e9)
        # # print(Attack,Balanced,Defence,"d") 
        # if(Attack>Balanced and Attack>Defence):
        #     dp_b[T][alice_wins][bob_wins]= Attack
        #     return (Attack,0)
        # elif(Balanced>Attack and Balanced>Defence):
        #     dp_b[T][alice_wins][bob_wins]= Attack
        #     return (Balanced,1)
        # else:
        #     dp_b[T][alice_wins][bob_wins]= Attack
        #     return (Defence,2)
        return 0
        
    elif(T>0):
        if(dp_b[T-1][alice_wins+1][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"a")
            dp_b[T-1][alice_wins+1][bob_wins]=E_dp_b(alice_wins+1,bob_wins,T-1,dp_a,dp_b,dp_d)
        if(dp_b[T-1][alice_wins][bob_wins+1]==-1):
            # print(alice_wins,bob_wins,T,'b')
            dp_b[T-1][alice_wins][bob_wins+1]=E_dp_b(alice_wins,bob_wins+1,T-1,dp_a,dp_b,dp_d)
        if (dp_b[T-1][alice_wins][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"c")
            dp_b[T-1][alice_wins][bob_wins]=E_dp_b(alice_wins,bob_wins,T-1,dp_a,dp_b,dp_d)
        # e1=payoff_matrix[0][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[0][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        e2=payoff_matrix[0][1][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][1][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[0][1][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e3=payoff_matrix[0][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        # e4=payoff_matrix[1][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[1][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        e5=payoff_matrix[1][1][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][1][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[1][1][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e6=payoff_matrix[1][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        # e7=payoff_matrix[2][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[2][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        e8=payoff_matrix[2][1][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][1][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[2][1][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e9=payoff_matrix[2][2][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][2][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][2][2]*(dp[T-1][alice_wins][bob_wins+1])
        Attack=e2
        Balanced=e5
        Defence=e8
        # print(Attack,Balanced,Defence)
        if(Attack>Balanced and Attack>Defence):
            print("0")
            return (Attack,0)
        elif(Defence>Attack and Defence>Balanced):
            print("here2")
            return (Defence,2)
        else:
            return (Balanced,1)


def E_dp_d(alice_wins, bob_wins, T, dp_a,dp_b,dp_d):

    payoff_matrix = np.array([
        [(bob_wins/(bob_wins+alice_wins),0,alice_wins/(alice_wins+bob_wins)), (0.7,0,0.3), (5/11,0,6/11)],  
        [(0.3, 0, 0.7), (1/3,1/3,1/3), (0.3,0.5,0.2)], 
        [(6/11,0,5/11), (0.2,0.5,0.3), (0.1,0.8,0.1)]
        ])

    if(dp_d[T][alice_wins][bob_wins]!=-1):
        return dp_d[T][alice_wins][bob_wins]
    if(T==0):
        #Return greedy
        # e1=payoff_matrix[0][0][0]*(1)+payoff_matrix[0][0][1]*(0.5)+payoff_matrix[0][0][2]*(0)
        # e2=payoff_matrix[0][1][0]*(1)+payoff_matrix[0][1][1]*(0.5)+payoff_matrix[0][1][2]*(0)
        # e3=payoff_matrix[0][2][0]*(1)+payoff_matrix[0][2][1]*(0.5)+payoff_matrix[0][2][2]*(0)
        # e4=payoff_matrix[1][0][0]*(1)+payoff_matrix[1][0][1]*(0.5)+payoff_matrix[1][0][2]*(0)
        # e5=payoff_matrix[1][1][0]*(1)+payoff_matrix[1][1][1]*(0.5)+payoff_matrix[1][1][2]*(0)
        # e6=payoff_matrix[1][2][0]*(1)+payoff_matrix[1][2][1]*(0.5)+payoff_matrix[1][2][2]*(0)
        # e7=payoff_matrix[2][0][0]*(1)+payoff_matrix[2][0][1]*(0.5)+payoff_matrix[2][0][2]*(0)
        # e8=payoff_matrix[2][1][0]*(1)+payoff_matrix[2][1][1]*(0.5)+payoff_matrix[2][1][2]*(0)
        # e9=payoff_matrix[2][2][0]*(1)+payoff_matrix[2][2][1]*(0.5)+payoff_matrix[2][2][2]*(0)
        # Attack=(1/3)*(e1+e2+e3)
        # Balanced=(1/3)*(e4+e5+e6)
        # Defence=(1/3)*(e7+e8+e9)
        # # print(Attack,Balanced,Defence,"d") 
        # if(Attack>Balanced and Attack>Defence):
        #     dp_a[T][alice_wins][bob_wins]= Attack
        #     return (Attack,0)
        # elif(Balanced>Attack and Balanced>Defence):
        #     dp_a[T][alice_wins][bob_wins]= Attack
        #     return (Balanced,1)
        # else:
        #     dp_a[T][alice_wins][bob_wins]= Attack
        #     return (Defence,2)
        return 0
        
    elif(T>0):
        if(dp_a[T-1][alice_wins+1][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"a")
            dp_a[T-1][alice_wins+1][bob_wins]=E_dp_a(alice_wins+1,bob_wins,T-1,dp_a,dp_b,dp_d)[0]
        if(dp_a[T-1][alice_wins][bob_wins+1]==-1):
            # print(alice_wins,bob_wins,T,'b')
            dp_a[T-1][alice_wins][bob_wins+1]=E_dp_a(alice_wins,bob_wins+1,T-1,dp_a,dp_b,dp_d)[0]
        if (dp_a[T-1][alice_wins][bob_wins]==-1):
            # print(alice_wins,bob_wins,T,"c")
            dp_a[T-1][alice_wins][bob_wins]=E_dp_a(alice_wins,bob_wins,T-1,dp_a,dp_b,dp_d)[0]
        # e1=payoff_matrix[0][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[0][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e2=payoff_matrix[0][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[0][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        e3=payoff_matrix[0][2][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[0][2][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[0][2][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e4=payoff_matrix[1][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[1][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e5=payoff_matrix[1][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[1][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        e6=payoff_matrix[1][2][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[1][2][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[1][2][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e7=payoff_matrix[2][0][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][0][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[2][0][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        # e8=payoff_matrix[2][1][0]*(1+dp[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][1][1]*(0.5+dp[T-1][alice_wins][bob_wins])+payoff_matrix[2][1][2]*(dp[T-1][alice_wins][bob_wins+1])
        e9=payoff_matrix[2][2][0]*(1+dp_a[T-1][alice_wins+1][bob_wins])+payoff_matrix[2][2][1]*(0.5+dp_b[T-1][alice_wins][bob_wins])+payoff_matrix[2][2][2]*(dp_d[T-1][alice_wins][bob_wins+1])
        Attack=e3
        Balanced=e6
        Defence=e9
        # print(Attack,Balanced,Defence)
        if(Attack>Balanced and Attack>Defence):
            print("0")
            return (Attack,0)
        elif(Defence>Attack and Defence>Balanced):
            print("here2")
            return (Defence,2)
        else:
            return (Balanced,1)

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    monte_carlo(num_rounds=10^5)