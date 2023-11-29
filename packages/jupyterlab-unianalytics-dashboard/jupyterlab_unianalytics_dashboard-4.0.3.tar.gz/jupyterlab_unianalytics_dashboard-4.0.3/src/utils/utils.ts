import { SHA256 } from 'crypto-js';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Selectors } from './constants';
import { CompatibilityManager } from './compatibility';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { KernelMessage } from '@jupyterlab/services';

export const getUserIdFromEnv = async (
  app: JupyterFrontEnd,
  variableName: string
): Promise<string> => {
  let userId = '';

  // create a session and a kernel to execute python code to retrieve the env variable value
  const session = await app.serviceManager.sessions.startNew({
    path: '',
    type: '',
    name: ''
  });

  try {
    const kernel = session.kernel;

    if (kernel) {
      // execute the code to access env variables
      const executionFuture = kernel.requestExecute({
        code: `import os\nos.environ.get('${variableName}')`,
        store_history: false,
        allow_stdin: false
      });

      executionFuture.onIOPub = (msg: KernelMessage.IIOPubMessage) => {
        // catch the message containing the execution result
        if (msg.header.msg_type === 'execute_result') {
          const text = (msg as KernelMessage.IExecuteResultMsg).content.data[
            'text/plain'
          ];
          userId = text ? text.toString().replace(/^['"](.*)['"]$/, '$1') : '';
        }
      };

      await executionFuture.done;
    }
  } finally {
    // cleanup: shutdown the session and kernel
    if (session) {
      session.shutdown();
    }
  }

  return userId;
};

export const isNotebookValidForVisu = (
  panel: NotebookPanel | null
): boolean => {
  if (panel && !panel.isDisposed && panel.context.isReady) {
    if (
      CompatibilityManager.getMetadataComp(
        panel.context.model,
        Selectors.notebookId
      ) &&
      CompatibilityManager.getMetadataComp(
        panel.context.model,
        Selectors.cellMapping
      )
    ) {
      return true;
    }
  }
  return false;
};

export const areListsEqual = (
  list1: string[] | null | undefined,
  list2: string[] | null | undefined
): boolean => {
  // if any of them is not defined, return not equal
  if (!list1 || !list2) {
    return false;
  }
  // Check if the lengths are equal
  if (list1.length !== list2.length) {
    return false;
  }

  // Check if every element in list1 is equal to the corresponding element in list2
  return list1.every((item, index) => item === list2[index]);
};

export const hashCellList = (cellList: string[] | null | undefined): string => {
  if (cellList && cellList.length > 0) {
    const combinedString = cellList.join('');
    return SHA256(combinedString).toString();
  } else {
    return '';
  }
};

// calculates the delay (in ms) to the next full second
export const calculateDelay = () => {
  const now = new Date();
  const milliseconds = now.getMilliseconds();
  const delay = 1000 - milliseconds;
  return delay;
};

export const compareVersions = (version1: string, version2: string): number => {
  // extract numeric parts by splitting at non-digit characters
  const parts1 = version1.split(/[^0-9]+/).map(Number);
  const parts2 = version2.split(/[^0-9]+/).map(Number);

  for (let i = 0; i < Math.min(parts1.length, parts2.length); i++) {
    const num1 = parts1[i];
    const num2 = parts2[i];

    if (num1 !== num2) {
      return num1 - num2;
    }
  }

  // if all numeric parts are equal, compare the string parts
  const str1 = version1.replace(/[0-9]+/g, '');
  const str2 = version2.replace(/[0-9]+/g, '');

  return str1.localeCompare(str2);
};
