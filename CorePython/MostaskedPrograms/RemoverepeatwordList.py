lst=["greek","for","greek"]
#if word is repeated more than once we need to delete it 
# take for loop iterate all items in list
# if that word appears 2nd time then delete that item from the list 
word="greek"
n=2 
count=0
for var in range(0,len(lst)):
    if lst[var]==word :
        count=count+1
        if count==n:
            del lst[var]
print(lst)

# ['greek', 'for']
