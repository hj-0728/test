export interface BenchmarkInputNodeItem {
  benchmarkId: string;
  benchmarkName: string;
  numericMinScore?: number;
  numericMaxScore?: number;
  fillerCalcMethod?: string;
  limitedStringOptions?: Array<string>;
  scoreSymbolName: string;
  scoreSymbolCode: string;
  scoreSymbolValueType?: string;
  scoreSymbolNumericPrecision?: number;
  scoreSymbolStringOptions?: Array<string>;
  scoreResult?: string;
  stringScore?: string;
  numericScore?: number;
  inputScoreLogId?: string;
  inputScoreLogVersion?: number;
  displayPopover: boolean;
  canView?: boolean;
  benchmarkSourceCategory?: string;
}

export interface EvaluationCriteriaTreeItem {
  id: string;
  name: string;
  code?: string;
  comments?: string;
  evaluationCriteriaTreeId?: string;
  evaluationCriteriaId?: string;
  evaluationCriteriaName?: string;
  parentIndicatorId?: string;
  level?: number;
  sortInfo?: Array<number>;
  tagCode?: string;
  benchmarkDisplayList?: Array<BenchmarkInputNodeItem>;
  children: Array<EvaluationCriteriaTreeItem>;
}

export interface FormState {
  id: string;
  version: number | undefined;
  numericScore: number | undefined;
  stringScore: string | undefined;
  scoreSymbolValueType: string | undefined;
  scoreSymbolNumericPrecision: number | undefined;
  numericMinScore: number | undefined;
  numericMaxScore: number | undefined;
}
