
if __name__ == "__main__":
    import polars as pl

    input_data = pl.read_csv('AoC.input', separator='|', has_header=False, new_columns=['left_list','right_list'])

    left_counts = input_data.select(pl.col('left_list').value_counts()).unnest('left_list')
    right_counts = input_data.select(pl.col('right_list').value_counts()).unnest('right_list')

    similarity_score = (left_counts.join(right_counts, left_on='left_list', right_on='right_list', how='left')
                                   .filter(pl.col('count_right').is_not_null())
                                   .select(pl.col('left_list')*pl.col('count')*pl.col('count_right'))
                                   .sum())
    print(similarity_score.item())
    
