from loguru import logger


def test_weighted_sum():
    """
    按权重汇总数据
    """
    data = [1, 2, 3]
    weights = [1, 2, 3]
    total = 0
    sum_weights = sum(weights)
    for i in range(len(data)):
        total += data[i] * weights[i]
    logger.info(f"{total}/{sum_weights}={total/sum_weights}")
