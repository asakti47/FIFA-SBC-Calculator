# Import packages
import math
import website.fifaRatingScraping as fifaRatingScraping
import itertools
import collections
import pandas as pd


# A method to calculate the net sum rating of a team according to FIFA's algorithm
# Reference for algorithm: https://www.reddit.com/r/FIFA/comments/5osq7k/new_overall_rating_figured_out/
# Input: A list of ratings
# Output: A float value of the net teamTotal
def teamTotalCalculator(l: list):

    # Check if the list is greater than the maximum of 11 and raise a value error if it is
    if len(l) > 11:
        raise ValueError("Too many ratings inputted. A squad can only consist of 11 players")

    # Create variables sumRating, counter, lengthList, and newList to help iterate through the input list
    sumRatings = 0
    counter = 0
    lengthList = len(l)
    newList = l.copy()
    newList2 = l.copy()

    # Iterate through the list
    while counter < lengthList:
        currRating = newList.pop()

        # Check if the ratings in the input list are all in the proper format of integers
        if not isinstance(currRating, int):
            raise ValueError("Ratings inputted have to be integers!")
        sumRatings = sumRatings + currRating
        counter = counter + 1
    avgRating = sumRatings / 11.0

    # Count the "excess" as according to FIFA's rating algorithm
    totalExcess = 0.0
    counter = 0
    while counter < lengthList:
        currRating = newList2.pop()
        if currRating > avgRating:
            totalExcess = totalExcess + (currRating - avgRating)
        counter = counter + 1

    # Return the net teamTotal
    teamTotal = sumRatings + totalExcess
    return teamTotal


# A method to calculate the final rating of a team based on the team total rating value
# Input: A float value representing the team total rating value (refer to reference for algorithm)
# Output: An integer representing the final net rating
def calculateRating(team_total: float):

    # Round the team total value to the nearest integer
    temp_total = round(team_total)

    # Divide the rounded team total by 11
    net_rating = temp_total / 11.0

    # Return the final rating by rounding down the result from the previous calculation
    return math.floor(net_rating)


# A method that calculates what ratings are needed to achieve a target rating
# Input: a list of ratings, an integer corresponding to the target rating, an integer representing the
# lower range of ratings to check for, and an integer representing the
# upper range of ratings to check for
# Output: A list containing a list of ratings that would achieve the target rating when added to the
# initial set of ratings.
def ratingCheck(rating_list: list, target_rating: int, min_value: int, max_value: int):

    # If the input list of ratings contain more ratings than the maximum possibility of 11
    if len(rating_list) > 11:
        raise ValueError("Too many ratings inputted. A squad can only consist of 11 players")

    # If the input list of ratings already make up the length of a full squad of 11
    if len(rating_list) == 11:
        raise ValueError("Squad is already full. No more players can be added into the SBC.")

    # Calculate the number of players needed to make up a full 11
    num_players_needed = 11 - len(rating_list)

    # Find all the possible combinations of ratings given the range as specified by the input
    possible_ratings = allCombinations(min_value, max_value, num_players_needed)

    # Iterate through all the possible combinations of ratings and test to see whether they would
    # add up to the target rating desired
    output = []
    for i in possible_ratings:
        temp_rating_list = rating_list + list(i)

        # If the tested list of ratings make up a length of 11
        if len(temp_rating_list) == 11:

            # If the tested list of ratings add up to the target rating desired, append the current set
            # of additional ratings into a list of outputs
            if calculateRating(teamTotalCalculator(temp_rating_list)) >= target_rating:
                output.append(list(i))
    return output


# A method to calculate all the possible unique combinations with a specified length and
# repeating values from a range of numbers
# Input: An integer representing the lower bound, an integer representing the upper bound, and an
# integer representing the length of combinations that is desired
# Output: A list containing all the combinations
def allCombinations(min_range: int, max_range: int, n: int):
    range_ratings = []

    # Create a list based on the input of the range of ratings
    for i in range(min_range, max_range + 1):
        range_ratings.append(i)

    # Return the list containing all the combinations given the range and the length of each set
    output = list(itertools.combinations_with_replacement(range_ratings, n))
    return output


# A method to return the cheapest FIFA card with the given input rating
# Input: An integer corresponding to a rating
# Output: An integer representing the price of the cheapest FIFA card with the given input rating
def ratingCost(rating: int):
    return fifaRatingScraping.getCheapest(rating)


# A method to calculate the individual prices of the list of all combinations of ratings
# Input: A list of ratings, an integer representing the minimum rating in the calculation, 
# and an integer representing the maximum rating in the calculation
# Output: A list of all the individual prices of the list from all combinations of ratings
def calculatePrice(all_ratings_list: list, min_rating: int, max_rating: int):
    current_prices = {}
    curr_rating = min_rating
    for i in range(min_rating, max_rating + 1):
        current_prices[curr_rating] = ratingCost(curr_rating)
        curr_rating += 1
    output = []
    for curr_list in all_ratings_list:
        total_price = 0
        for i in curr_list:
            total_price = total_price + current_prices[i]
        output.append(total_price)

    return output


# A method that counts the frequency of each element in a set from a list of sets of ratings
# Input: A list containing sets of ratings
# Output: A list of dictionaries containing the frequency of each element in each set of ratings
def countRatings(all_ratings_list: list):
    output = []
    for i in all_ratings_list:
        output.append(collections.Counter(i))
    return output

# A method that finds all the possible ratings possible to solve an SBC, and the corresponding price
# of those sets of ratings.
# Input: a list of ratings, an integer corresponding to the target rating, an integer representing the
# lower range of ratings to check for, and an integer representing the
# upper range of ratings to check for
# Output: A DataFrame of all possible rating combinations to satisfy target rating as well as its corresponding estimated cost
# from the Xbox FIFA  Ultimate Team database
def findRatingsAndPrice(curr_ratings_list: list, target_rating: int, min_rating: int, max_rating: int):
    ratings_needed = ratingCheck(curr_ratings_list, target_rating, min_rating, max_rating)
    dict_ratings = countRatings(ratings_needed)
    all_prices = calculatePrice(ratings_needed, min_rating, max_rating)
    output_df = pd.DataFrame(dict_ratings)
    output_df = output_df.sort_index(axis=1)
    output_df["Estimated Cost"] = all_prices
    output_df = output_df.fillna(0)
    output_df = output_df.astype('int')
    output_df = output_df.sort_values('Estimated Cost')
    return output_df