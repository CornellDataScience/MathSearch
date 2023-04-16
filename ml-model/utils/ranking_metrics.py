from sklearn.metrics import label_ranking_average_precision_score


def hit_rate(topNPredicted, total, gt):
    """
    Measures the fraction of images for which the correct answer is included in the recommendation list

    Args:
      topNPredicted (Dict): topNRecommendations for every image, where each key is an imageID and its respective value is the top N recommendations
        Example: {
          0: [1, 9, 20], 1: [3, 5, 30]
        }
      total (int): Length of dataset
      gt (List): Groundtruth data

    Returns:
      Hit rate

    """
    hits = 0

    for user in gt:
        userID = user[0]
        imageID = user[1]
        recommendations = topNPredicted[userID]
        if imageID in recommendations:
            hits += 1

    return hits / total


def mean_reciprocal_rank(topNPredicted, total, gt):
    """
    Measures how far down the ranking the first relevant document is
    MRR --> 1 means relevant results are close to the top of search results
    MRR --> 0 indicates poorer search quality, with the right answer farther down in the search results

    Args:
      topNPredicted (Dict): topNRecommendations for every image, where each key is an imageID and its respective value is the top N recommendations
        Example: {
          0: [1, 9, 20], 1: [3, 5, 30]
        }
      total (int): Length of dataset
      gt (List): Groundtruth data

    Returns:
      Mean Reciprocal Rank

    """
    sum_reciprocal = 0
    for user in gt:
        userID = user[0]
        imageID = user[1]
        recommendations = topNPredicted[userID]
        if imageID in recommendations:
            rank = recommendations.index(imageID)
            sum_reciprocal += 1 / (rank)
        else:
            raise NotImplementedError("Need to figure what to count if doesn't exist!")

    return sum_reciprocal / total


def mAP(y_true, y_pred):
    """
    Measures average over each ground truth label assigned to each sample
    of the ratio of true vs. total labels with lower score

    Args:
      y_true (ndarray) of shape (n_samples, n_labels): True binary labels in binary indicator format; One hot encoded
      y_pred (ndarray) of shape (n_samples, n_labels): Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions
    """
    return label_ranking_average_precision_score(y_true, y_pred)


if __name__ == "__main__":
    pass
