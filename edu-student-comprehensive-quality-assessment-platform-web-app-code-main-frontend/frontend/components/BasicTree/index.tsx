import { TreeProps, Tree } from 'primereact/tree';
import 'primereact/resources/themes/lara-light-indigo/theme.css';
import 'primereact/resources/primereact.min.css';
import classes from './BasicTree.module.css';

const BasicTree = (props: TreeProps) => (
  <>
    <Tree
      {...props}
      className={classes.treeContent}
    />
  </>
);

export default BasicTree;
