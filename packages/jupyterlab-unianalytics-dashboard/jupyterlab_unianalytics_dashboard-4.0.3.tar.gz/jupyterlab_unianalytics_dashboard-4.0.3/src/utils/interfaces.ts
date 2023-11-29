import { ISignal } from '@lumino/signaling';
import { INotebookHeading } from './headings';
import { NotebookPanel } from '@jupyterlab/notebook';

export abstract class IOptionsManager {}

export interface ICollapseChangedArgs {
  collapsedState: boolean;

  heading: INotebookHeading;
}

export type ItemRenderer = (
  panel: NotebookPanel,
  item: INotebookHeading,
  headings: INotebookHeading[]
) => JSX.Element | null;

export interface IGenerator {
  options?: IOptionsManager;

  collapseChanged?: ISignal<IOptionsManager, ICollapseChangedArgs>;

  itemRenderer: ItemRenderer;

  toolbarGenerator: (panel: NotebookPanel) => any;

  generate(panel: NotebookPanel): INotebookHeading[];
}

export enum RegistrationState {
  LOADING = 'Loading',
  MISMATCH = 'Mismatch with the Registered Notebook',
  NOTFOUND = 'Notebook not Registered',
  USERNOTAUTHORIZED = 'No User Permission for this Notebook',
  ERROR = 'Fetching Error',
  SUCCESS = 'Success'
}

export type ValidityChecks = {
  tag: string | null | undefined;
  registered: RegistrationState;
};

export type NotebookTags = {
  notebookId: string;
};

export type LocationData = {
  location_count: { [key: string]: number };
} | null;
