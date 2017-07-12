import enchant

d = enchant.Dict("en_US")


# >>> d.check("Hello")
# True
# >>> d.check("Helo")
# False
# d.suggest("Helo")
# ['He lo, 'He-lo', 'Hello', 'Helot', 'Help', 'Halo', 'Hell', 'Held']

word = "T3st"
word = word.lower()
print(word)
word = word.replace("3", "e")
print(word)
