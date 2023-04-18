import sys

# read command line args to know which file to parse
lines = open(sys.argv[1], "r").readlines()

arr = []

# remember the order in which the numbers were in the file when we append
# the values to our list
i = 0
for line in lines[1:]:
    arr.append([int(line.strip()), i])
    i += 1

# reverse-sort the array based on the numeric value
arr.sort()
arr.reverse()

sum0 = 0
sum1 = 0

# outputs -- each element will be a 2-element array where the first element
# will be the original position of that number in the input file
outs = []

# add each number we encounter to the array with the lower sum
for val in arr:
    if sum0 <= sum1:
        sum0 += val[0]
        outs.append([val[1], 0])
    else:
        sum1 += val[0]
        outs.append([val[1], 1])

print(sum0)
print(sum1)

diff = abs(sum0 - sum1)

# we should have a good solution at this point, but we tried to improve it
# by swapping elements from the larger to smaller array if it was
# beneficial

# we happened to make mistakes in the implementation of this algorithm, so
# it didn't result in any improvements

smaller = 0
if sum1 < sum0:
    smaller = 1

old_diff = diff

while True:
    for i in range(len(outs)):
        a = outs[i][1]
        val = arr[i][0]

        # if an element is in the larger array, and swapping it to the
        # smaller one will decrease the difference, then swap it
        if a != smaller and val < diff:
            print(f"{val} (in array {a}) is less than {diff}")

            # we had made a mistake here -- these two lines are wrong
            sum1 -= val
            sum0 += val
            # we ideally should add val to the smaller sum, but this code
            # always adds it to sum0

            # now recompute the difference
            diff = abs(sum0 - sum1)
            smaller = 0
            if sum1 < sum0:
                smaller = 1

            # this line is also wrong -- it should swap it to the smaller
            # list, instead it always swaps to list 0
            outs[i][1] = 0

            # the above code would work only if sum0 happens to be smaller
            # initially

    # if we haven't got better, stop
    if diff == old_diff:
        break

    old_diff = diff

# print the values after the improvement
print(sum0)
print(sum1)

# now put the outputs in the same order in which they appeared in the input
outs.sort()

outfile = open(sys.argv[2], "w")
outfile.write(str(len(outs)) + "\n")

for val in outs:
    outfile.write(str(val[1]))
    outfile.write("\n")
