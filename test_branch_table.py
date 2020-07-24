
branch_table = {
    0b0:
        lambda:
        value = "test"
        print(value),
    0b1:
        lambda:
        print("one")
}



def branch(i=input("Type something: ")):
    return branch_table[int(i)]()
    
branch()