#!/usr/bin/env python
# -*- coding: utf-8 -*-

A = ['C','A','B','A','A','X','B','Y','A']
n = len(A)
count = 0
operations = 0
for i in range(0, n):
	operations = operations + 1
	if A[i] == 'A':
		for j in range(i+1, n-1):
			operations = operations + 1
			if A[j] == 'B':

				count = count + 1

print(count)
print(operations)