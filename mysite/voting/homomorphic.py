from random import randrange
import random


#creates a random binary reference string
def create_ref(candidate_count):
    ref_list = []
    for i in range(candidate_count):
        ref_list.append(randrange(0, 2))
    print(ref_list)
    return ref_list


#randomly selects a set among A,B,C,D
def select_set():
    set_selected = random.choice('ABCD')
    print(set_selected)
    return set_selected


#encrypt the reference string using the set  to generate beta string
def encrypt(ref_list, set_selected, vote_index):
    #list to store beta string
    beta_list = []
    #encryption rules for each sets
    set_A = [[0, 'Y', 1], [1, 'Y', 0], [0, 'N', 0], [1, 'N', 1]]
    set_B = [[0, 'Y', 1], [1, 'Y', 1], [0, 'N', 0], [1, 'N', 0]]
    set_C = [[0, 'Y', 0], [1, 'Y', 1], [0, 'N', 1], [1, 'N', 0]]
    set_D = [[0, 'Y', 0], [1, 'Y', 0], [0, 'N', 1], [1, 'N', 1]]
    if set_selected == 'A':
        for i in range(ref_list.__len__()):
            if i == vote_index:
                if ref_list[i] == 1:
                    beta_list.append(set_A[1][2])
                else:
                    beta_list.append(set_A[0][2])
            else:
                if ref_list[i] == 1:
                    beta_list.append(set_A[3][2])
                else:
                    beta_list.append(set_A[2][2])
    if set_selected == 'B':
        for i in range(ref_list.__len__()):
            if i == vote_index:
                if ref_list[i] == 1:
                    beta_list.append(set_B[1][2])
                else:
                    beta_list.append(set_B[0][2])
            else:
                if ref_list[i] == 1:
                    beta_list.append(set_B[3][2])
                else:
                    beta_list.append(set_B[2][2])
    if set_selected == 'C':
        for i in range(ref_list.__len__()):
            if i == vote_index:
                if ref_list[i] == 1:
                    beta_list.append(set_C[1][2])
                else:
                    beta_list.append(set_C[0][2])
            else:
                if ref_list[i] == 1:
                    beta_list.append(set_C[3][2])
                else:
                    beta_list.append(set_C[2][2])
    if set_selected == 'D':
        for i in range(ref_list.__len__()):
            if i == vote_index:
                if ref_list[i] == 1:
                    beta_list.append(set_D[1][2])
                else:
                    beta_list.append(set_D[0][2])
            else:
                if ref_list[i] == 1:
                    beta_list.append(set_D[3][2])
                else:
                    beta_list.append(set_D[2][2])

    print(beta_list)
    return beta_list


#function to decrypt the strings using set, returns the count for each candidates
def decrypt(ref_list, set_list, beta_list):
    vote_count = []
    #initialise the count for each candidate to zero
    for i in range(len(ref_list[0])):
        vote_count.append(0)
    set_A = [[0, 'Y', 1], [1, 'Y', 0], [0, 'N', 0], [1, 'N', 1]]
    set_B = [[0, 'Y', 1], [1, 'Y', 1], [0, 'N', 0], [1, 'N', 0]]
    set_C = [[0, 'Y', 0], [1, 'Y', 1], [0, 'N', 1], [1, 'N', 0]]
    set_D = [[0, 'Y', 0], [1, 'Y', 0], [0, 'N', 1], [1, 'N', 1]]
    #iterate for all the voters in that region by selecting individual strings
    for i in range(ref_list.__len__()):
        set_selected = set_list[i][0]
        ref_string = ref_list[i]
        beta_string = beta_list[i]
        if set_selected == 'A':
            for j in range(ref_string.__len__()):
                if ref_string[j] == 0 and beta_string[j] == 1:
                    vote_count[j] += 1
                if ref_string[j] == 1 and beta_string[j] == 0:
                    vote_count[j] += 1
        if set_selected == 'B':
            for j in range(ref_string.__len__()):
                if ref_string[j] == 0 and beta_string[j] == 1:
                    vote_count[j] += 1
                if ref_string[j] == 1 and beta_string[j] == 1:
                    vote_count[j] += 1
        if set_selected == 'C':
            for j in range(ref_string.__len__()):
                if ref_string[j] == 0 and beta_string[j] == 0:
                    vote_count[j] += 1
                if ref_string[j] == 1 and beta_string[j] == 1:
                    vote_count[j] += 1
        if set_selected == 'D':
            for j in range(ref_string.__len__()):
                if ref_string[j] == 0 and beta_string[j] == 1:
                    vote_count[j] += 1
                if ref_string[j] == 1 and beta_string[j] == 0:
                    vote_count[j] += 1
    print(vote_count)
    return vote_count


def get_betabit(ref_string, set_selected, beta_string):
    betabit = ""
    if set_selected == 'A':
        for j in range(ref_string.__len__()):
            if ref_string[j] == 0 and beta_string[j] == 1:
                betabit = beta_string[j]
            if ref_string[j] == 1 and beta_string[j] == 0:
                betabit = beta_string[j]
    if set_selected == 'B':
        for j in range(ref_string.__len__()):
            if ref_string[j] == 0 and beta_string[j] == 1:
                betabit = beta_string[j]
            if ref_string[j] == 1 and beta_string[j] == 1:
                betabit = beta_string[j]
    if set_selected == 'C':
        for j in range(ref_string.__len__()):
            if ref_string[j] == 0 and beta_string[j] == 0:
                betabit = beta_string[j]
            if ref_string[j] == 1 and beta_string[j] == 1:
                betabit = beta_string[j]
    if set_selected == 'D':
        for j in range(ref_string.__len__()):
            if ref_string[j] == 0 and beta_string[j] == 1:
                betabit = beta_string[j]
            if ref_string[j] == 1 and beta_string[j] == 0:
                betabit = beta_string[j]
    return betabit


#print("Homomorphic Encryption")

# r_list = []
# s_list = []
# b_list = []
# for i in range(10):
#     ref = create_ref(5)
#     set = select_set()
#     r_list.append(ref)
#     s_list.append(set)
#     beta = encrypt(ref, set, 3)
#     b_list.append(beta)
# #print("Beta :")
#
# decrypt(r_list, s_list, b_list)