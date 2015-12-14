#!/usr/bin/env python

# From adventofcode.com

# Who is naughty or nice

# A nice string is one with all of the following properties:

# - It contains at least three vowels (aeiou only), 
#   like aei, xazegov, or aeiouaeiouaeiou.
# - It contains at least one letter that appears 
#   twice in a row, like xx, abcdde (dd), or 
#   aabbccdd (aa, bb, cc, or dd).
# - It does not contain the strings ab, cd, pq, or xy, 
#   even if they are part of one of the other requirements.

def isNice():
  with open('input.txt', 'r') as f:
    nice_list = []
    naughty_words = ['ab', 'cd', 'pq', 'xy']
    vowels = ['a', 'e', 'i', 'o', 'u']
    count = 0
    for l in f:
      dbl_ltr_check = False
      vowel_count = 0
      dbl_ltr = ''
      if not any(s in l for s in naughty_words):
        for i in range(len(l)-1):
          if l[i] in vowels:
            vowel_count += 1
          if l[i] == l[i+1]:
            dbl_ltr_check = True
        if dbl_ltr_check == True and vowel_count >= 3:
          nice_list.append(l)
    print 'number of nice words: ' + str(len(nice_list))



def main():
  isNice()

if __name__ == "__main__":
    main()
