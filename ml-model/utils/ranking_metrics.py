import torch


def getTopNPredictions(predictions, n=10):
    pass


def hit_ratio(topNPredicted, total, gt):
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


def mAP():
    pass


if __name__ == "__main__":
    pass
