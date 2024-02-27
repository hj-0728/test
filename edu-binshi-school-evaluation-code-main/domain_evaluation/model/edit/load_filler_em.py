from infra_basic.basic_model import BasePlusModel


class LoadFillerEditModel(BasePlusModel):
    filler_calc_method: str
    benchmark_input_node_id: str
    establishment_assign_id: str
