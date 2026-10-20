from recommend_v2 import recommend, recommend_by_index, df

if __name__ == "__main__":
    title = input("Enter a movie or series: ")
    print(recommend(title, n=5)[["title", "type", "genre_names", "rating", "match_score"]])