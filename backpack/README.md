Tucker Jaenicke
11/6/18

The problem presented was the classic backpack problem where your backpack
can only hold a set amount of weight. You want to maximize the value of 
the backpack without going overweight. This can be solved as with a genetic
algorithm where a chromosome is a binary string where each bit represents
whether an item is in or out of the bag. Reproduction occurs with two
random chromosomes. Part of the binary string of one parent is combined with
part of the binary string of the other parent. Occasionally the offsping has
a mutation where one bit is randomly flipped. The fitness of each chromosome
was equal to the value of the items, but 0 if the items were overweight.
The algorithm continues until the generation limit is reached.

The program can be run on the command line witht he command 
'python3 backpack.py'. The algorithm runs as expected and gets the correct
answer most of them time, but not every time. Usually when the incorrect
answer is obtained, a mutation occured to get it there.

The weights and values of the items in the backpack are hardcoded into the
program, but can easily be editted to accept user input.
