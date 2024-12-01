def solve_via_numpy():
    '''
    numpy version of the solver with basic python
    and argsorts    
    '''
    import numpy as np
    
    with open('AoC_Day1.input','r') as infile:
        input_data = [list(map(int, line.strip().split())) for line in infile if line != '\n']

    input1, input2 = map(np.asarray, map(list, zip(*input_data)))

    return np.sum(np.abs(input1[np.argsort(input1)] - input2[np.argsort(input2)]))


def solve_via_polars():
    '''
    polars version of the solver    
    '''
    import polars as pl

    input_data = pl.read_csv('AoC_Day1.input', has_header=False, new_columns=['temp']).drop_nulls().select(pl.col('temp').str.split_exact(by='   ', n=1)).unnest('temp')

    return input_data.with_columns((pl.col('field_0').cast(pl.Int32).sort() - pl.col('field_1').cast(pl.Int32).sort()).abs().alias('diff')).select(pl.col('diff').sum()).item()

if __name__ == "__main__":
    # A sort of Hamming Distance like measure between 
    # sorted lists. 
    import cProfile
    import pstats

    with cProfile.Profile() as profile:
        print(solve_via_numpy())
        pstats.Stats(profile).print_stats(3)

    with cProfile.Profile() as profile:
        print(solve_via_polars())
        pstats.Stats(profile).print_stats(3)
    