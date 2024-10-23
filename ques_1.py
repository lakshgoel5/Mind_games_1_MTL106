"""
Use the following functions to add, multiply and divide, taking care of the modulo operation.
Use mod_add to add two numbers taking modulo 1000000007. ex : c=a+b --> c=mod_add(a,b)
Use mod_multiply to multiply two numbers taking modulo 1000000007. ex : c=a*b --> c=mod_multiply(a,b)
Use mod_divide to divide two numbers taking modulo 1000000007. ex : c=a/b --> c=mod_divide(a,b)
"""
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

def calc_prob_dp(alice_wins, bob_wins, dp):
    total = mod_add(alice_wins, bob_wins)

    if(dp[alice_wins][bob_wins]!=-1):
        return dp[alice_wins][bob_wins]
    
    if bob_wins == 1:
        ans = 1
        while total > 2:
            total = total - 1
            ans = mod_divide(ans, total)
        dp[alice_wins][bob_wins]=ans
          # Use modular inverse for division
        return ans
    elif alice_wins == 1:
        ans = 1
        while total > 2:
            total = total - 1
            ans = mod_divide(ans, total)  # Use modular inverse for division
        dp[alice_wins][bob_wins]=ans
        return ans
    else:
        win = mod_divide(bob_wins, (alice_wins + bob_wins - 1))  # mod division
        lose = mod_divide(alice_wins, (alice_wins + bob_wins - 1))  # mod division
        a = mod_multiply(calc_prob_dp(alice_wins - 1, bob_wins, dp), win)
        b = mod_multiply(calc_prob_dp(alice_wins, bob_wins - 1, dp), lose)
        dp[alice_wins][bob_wins] = mod_add(a, b)
        return dp[alice_wins][bob_wins]

def calc_prob(alice_wins, bob_wins):
    dp = [[-1 for _ in range(bob_wins + 1)] for _ in range(alice_wins + 1)]
    
    """
    Returns:
        The probability of Alice winning alice_wins times and Bob winning bob_wins times will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.
    """
    return calc_prob_dp(alice_wins, bob_wins, dp)


# Problem 1b (Expectation)      
def calc_expectation(t):
    """
    Returns:
        The expected value of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    expec=0
    # Using linearity of expectation
    for i in range(1, t+1):
        expec=mod_add(mod_add(prob_win(i),mod_multiply(prob_loss(i),-1)), expec)
    return expec

# Problem 1b (Variance)
def calc_variance(t):
    """
    Returns:
        The variance of \sum_{i=1}^{t} Xi will be of the form p/q,
        where p and q are positive integers,
        return p.q^(-1) mod 1000000007.

    """
    var=0
    #Sum of Xi is point of alice - points of bob
    #So this is my new random variable
    #It can vary from -t to t
    #var(X)=E(X^2)-(E(X))^2
    #E(X)=0 proved
    #So var(X)=E(X^2)
    #=sum(x^2*P(X=x))

    ####No need of below lines
    #X^2=(point of alice - (t-points of alice))^2
    #X^2=(2*point of alice - t)^2
    #X^2=4*point of alice^2 - 4*t*point of alice + t^2
    #E(X^2)=4*E(point of alice^2) - 4*t*E(point of alice) + t^2
    #E(x^2)=4*E(point of alice^2) - 4*t*0.5 + t^2

    for i in range(1, t):
        # print(i, var,'d')
        var=mod_add(mod_multiply(calc_prob(i,t-i), mod_multiply(i-(t-i),i-(t-i))), var)
    return var
    


#probability of alice winning at ith round dosen't depend on further rounds, therefore
def prob_win(i):
    total=i-1
    ans=0
    for j in range (1, total):
        ans=mod_add(ans, mod_multiply(mod_divide(total-j,total), calc_prob(j, total-j)))
        # print(calc_prob(j, total-j))
        # ans=ans+((total-j)/total)*calc_prob(j, total-j)
    return ans

def prob_loss(i):
    total=i-1
    ans=0
    for j in range (1, total):
        ans=mod_add(ans, mod_multiply(mod_divide(j,total), calc_prob(j, total-j)))
        # print(calc_prob(j, total-j))
        # ans=ans+(j/total)*calc_prob(j, total-j)
    return ans

    
"""
Alice wins first round and loses second.
Entry Number: 0848
T_1T_2=98
T_3T_4=48
T=98+48=146

"""


    

