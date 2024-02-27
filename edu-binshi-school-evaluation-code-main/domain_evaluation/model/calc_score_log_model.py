from infra_basic.basic_model import VersionedModel


class CalcScoreLogModel(VersionedModel):
    """
    计算节点得分记录
    """

    evaluation_assignment_id: str
    benchmark_calc_node_id: str
