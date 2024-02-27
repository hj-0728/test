// #!/usr/bin/env node

import { runBuildConfig } from './buildConf';
import colors from 'picocolors';

import pkg from '../../package.json';

export const runBuild = async () => {
  try {
    const argvList = process.argv.splice(2);

    // Generate configuration file
    if (!argvList.includes('disabled-config')) {
      runBuildConfig();
    }

    console.log(`✨ ${colors.cyan(`[${pkg.name}]`)}` + ' - tools successfully!');
  } catch (error) {
    console.log(colors.red('vite tools error:\n' + error));
    process.exit(1);
  }
};
runBuild();
