
if __name__ == '__main__':
	'''
	For this one, the goal is to find lists of items where
	the items are all increasing or all decreasing by a value <=3.
	If there are repeats, or a combination of increasing and decreasing,
	or if the items increase or decrease outside of the specified range,
	then the list "fails".
	'''
	import numpy as np
	import polars as pl

	# The lists here are ragged, so we won't read with polars
	# Instead, we'll square off the matrix / fill in the ragged lines
	# to make a full matrix we can feed to polars
	with open('AoC_Day2.input','r') as infile:
		inputdata = [line.split() for line in infile]
		linelen   = max([len(line) for line in inputdata])
		inputdata = [line+[None]*(linelen - len(line)) for line in inputdata]

	###############
	# Part One
	###############
	# For the below, the all_horizontal function will return null if there are a mix of trues and nulls
	# but not if there is a mix of falses and nulls. Conversely, any_horizontal will return null if 
	# there is a mix of trues and nulls, but false if there is a mix of falses and nulls.
	# The nulls here actually come from the ragged lines, because 10-null is null by polars behavior,
	# and so is null-null. What this means is that the "ok" column is filled with nulls, trues, and falses.
	# the trues are only there when the len of the list was == max list len, the nulls are when the 
	# conditions were true, but the list was < max list len, and the falses are when the lists "failed".
	# In our case then, we'll fill nulls with true and filter out the positives.
	# Conversely, you could just subtract where ok == False from the overall df shape to get the same answer.
	part1answer = (pl.DataFrame(inputdata).cast(pl.Int32).select(pl.all().diff(null_behavior='drop')).transpose()
					 .with_columns(posok=pl.all_horizontal(pl.all().is_between(1,3)), 
								   negok=pl.all_horizontal(pl.all().is_between(-3,-1)))
					 .with_columns(   ok=pl.any_horizontal(pl.col(['posok','negok'])))
					 .filter(pl.col('ok').fill_null(True) != False).shape[0])

	print(f'Part one answer: {part1answer}')

	###############
	# Part Two
	###############
	# New problem, we can remove any single number from the list, and if that makes it safe
	# then the list is considered safe. There's likely a way to find the exact element that's at fault
	# and remove it (the part1answer identifies the pair at fault, and you could just remove one or the other there)
	# but we really don't have that much data, and so it's pretty easy to just check all multiset permutations
	# of true/false of linelen (which is 8 for my input data). 
	# Could use sympy multiset permutations, or do permutations and take the set, but easier to just make a 
	# square matrix and set the diagonal to False in this case, as it makes a LOO mask matrix we can use.
	mask = np.array([[True]*8]*8)
	np.fill_diagonal(mask, False) # In place operation.
	mask = np.vstack([[[True]*8], mask]) # Add in the original case

	part2answer = (pl.concat([pl.DataFrame(inputdata)
	                            .filter(pl.Series(submask)).cast(pl.Int32)
	                            .select(pl.all().diff(null_behavior='drop'))
	                            .transpose()
	                            .with_columns(posok=pl.all_horizontal(pl.all().is_between(1,3)), 
	                                          negok=pl.all_horizontal(pl.all().is_between(-3,-1)))
	                            .with_columns(pl.any_horizontal(pl.col(['posok','negok'])).alias(f'{i}_ok'))
	                            .select(f'{i}_ok').fill_null(True).with_row_index() for i,submask in enumerate(mask)], how='align')
					 .drop('index')
					 .with_columns(allok=pl.any_horizontal(pl.all())).filter(pl.col("allok") == True)).shape[0]
	print(f'Part two answer: {part2answer}')
	
			
