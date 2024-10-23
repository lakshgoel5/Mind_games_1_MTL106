import numpy as np

class Alice:
    def __init__(self):
        self.past_play_styles = np.array([1,1])  
        self.results = np.array([1,0])           
        self.opp_play_styles = np.array([1,1])  
        self.points = 1

    def play_move(self):
        """
        Decide Alice's play style for the current round. Implement your strategy for 2a here.
         
        Returns: 
            0 : attack
            1 : balanced
            2 : defence

        """
        nb=len(self.results)-self.points
        na=self.points
        if self.results[-1] == 0:
            return 1
        elif self.results[-1] == 0.5:
            return 0
        else:  
            if((nb/(na+nb))>6/11):
                return 0
            else:
                return 2
        
    
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
        # print(self.points,'a')
 

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
    alice=Alice()
    bob=Bob()
    payoff_matrix = np.array([
        [(bob.points/(bob.points+alice.points),0,alice.points/(alice.points+bob.points)), (0.7,0,0.3), (5/11,0,6/11)],  
        [(0.3, 0, 0.7), (1/3,1/3,1/3), (0.3,0.5,0.2)], 
        [(6/11,0,5/11), (0.2,0.5,0.3), (0.1,0.8,0.1)]])
    for i in range(10**5):
        simulate_round(alice,bob,payoff_matrix)
    return alice.points,bob.points
    """
    Runs a Monte Carlo simulation of the game for a specified number of rounds.
    
    Returns:
        None
    """
    
    
 

# Run Monte Carlo simulation with a specified number of rounds
if __name__ == "__main__":
    print(monte_carlo(num_rounds=10**5))


