import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-q", default="#sailormoonredraw")
parse.add_argument("-f", default="../https_list.csv")
parse.add_argument("-r", "--min_rt", type=int, default=1000)
parse.add_argument("--max_rt", type=int, default=10000)
parse.add_argument("-p", "--max_count_page", type=int, default=3)

args = parse.parse_args()
