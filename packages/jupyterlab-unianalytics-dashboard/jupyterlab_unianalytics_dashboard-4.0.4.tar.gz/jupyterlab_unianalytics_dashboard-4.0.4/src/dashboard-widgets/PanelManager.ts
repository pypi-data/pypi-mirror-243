import { NotebookPanel } from '@jupyterlab/notebook';
import { ActivityMonitor } from '@jupyterlab/coreutils';
import { ISignal, Signal } from '@lumino/signaling';
import {
  BACKEND_API_URL,
  Selectors,
  TOC_DASHBOARD_RENDER_TIMEOUT
} from '../utils/constants';
import {
  areListsEqual,
  hashCellList,
  isNotebookValidForVisu
} from '../utils/utils';
import { AppDispatch, store } from '../redux/store';
import { NotebookCell } from '../redux/types';
import { setNotebookCells } from '../redux/reducers/CommonDashboardReducer';
import { RegistrationState, ValidityChecks } from '../utils/interfaces';
import { WebsocketManager } from './WebsocketManager';
import { CompatibilityManager } from '../utils/compatibility';

const dispatch = store.dispatch as AppDispatch;

export class PanelManager {
  constructor() {
    this._panel = null;
    this._monitor = null;

    this._validityChecks = {
      tag: null,
      registered: RegistrationState.LOADING
    };

    this._websocketManager = new WebsocketManager();
  }

  get validityChecks(): ValidityChecks {
    return this._validityChecks;
  }

  get notebookCells(): string[] | null | undefined {
    return this._notebookCells;
  }

  get panel(): NotebookPanel | null {
    return this._panel;
  }

  set panel(value: NotebookPanel | null) {
    if (value && this._panel && this._panel === value) {
      return;
    }

    if (this._panel) {
      this._panel.disposed.disconnect(this._onPanelDisposed, this);
    }

    // reset validity checks
    this._validityChecks = {
      tag: null,
      registered: RegistrationState.LOADING
    };

    // remove the websocket connection if there's one
    this._websocketManager.terminateSocketConnection();

    this._panel = value;
    // emit signal that there was a panel switch
    this._onPanelSwitched();

    if (this._panel) {
      this._panel.disposed.connect(this._onPanelDisposed, this);
    }

    // dispose an old activity monitor if one existed...
    if (this._monitor) {
      this._monitor.dispose();
      this._monitor = null;
    }

    // if there is no panel, update and return...
    if (!this._panel) {
      this._onPanelUpdated();
      return;
    }

    // to make sure the panel hasn't changed by the time the context is ready
    const scopeId = crypto.randomUUID();
    this._ongoingContextId = scopeId;
    // wait for the panel session context to be ready, for the metadata to be available
    // and all the cell nodes to be added to the DOM, required for the toc generation
    this._panel.sessionContext.ready.then(() => {
      if (
        this._ongoingContextId === scopeId &&
        this._panel &&
        !this._panel.isDisposed
      ) {
        // throttle the rendering rate of the table of contents
        this._monitor = new ActivityMonitor({
          signal: this._panel.context.model.contentChanged,
          timeout: TOC_DASHBOARD_RENDER_TIMEOUT
        });
        this._monitor.activityStopped.connect(this._onPanelUpdated, this);

        // check if notebook is tagged and assign the notebook id
        if (isNotebookValidForVisu(this._panel)) {
          const notebookId = CompatibilityManager.getMetadataComp(
            this._panel.model,
            Selectors.notebookId
          );
          this._validityChecks.tag = notebookId;
        }

        this._onPanelUpdated();
      }
    });
  }

  private _onPanelDisposed(_panel: NotebookPanel) {
    // when the panel is disposed, dispose from the panel (calling the _panel setter)
    this.panel = null;
  }

  // expose the signal as a public property
  get panelSwitched(): ISignal<PanelManager, void> {
    return this._panelSwitchedSignal;
  }

  private _onPanelSwitched() {
    // emit the signal when the panel is updated
    this._panelSwitchedSignal.emit(void 0);
  }

  // expose the signal as a public property
  get panelUpdated(): ISignal<PanelManager, void> {
    return this._panelUpdatedSignal;
  }

  private _onPanelUpdated() {
    const hasListChanged = this._updateCellList();

    if (this._validityChecks.tag) {
      // check if notebook is registered (only if the cell list changed)
      if (hasListChanged) {
        this._websocketManager.terminateSocketConnection();
        this._validityChecks.registered = RegistrationState.LOADING;

        // to make sure the panel hasn't changed by the time the promise resolves
        const scopeId = crypto.randomUUID();
        this._ongoingCheckId = scopeId;

        // check with the backend if the notebook is registered and that the cells match
        let currentRegistrationState = RegistrationState.ERROR;

        fetch(
          `${BACKEND_API_URL}/dashboard/${
            this._validityChecks.tag
          }/check?hashedList=${hashCellList(this._notebookCells)}`,
          {
            credentials: 'include'
          }
        )
          .then(res => {
            if (res.ok) {
              return res.json();
            } else {
              throw new Error('Fetching response not OK');
            }
          })
          .then(data => {
            if (data.status === 'not_found') {
              // no entry found in the Notebook table for the notebook id
              currentRegistrationState = RegistrationState.NOTFOUND;
            } else if (data.status === 'hash_mismatch') {
              // hash mismatch between cell lists
              currentRegistrationState = RegistrationState.MISMATCH;
            } else if (data.status === 'no_user_permission') {
              currentRegistrationState = RegistrationState.USERNOTAUTHORIZED;
            } else if (data.status === 'success') {
              currentRegistrationState = RegistrationState.SUCCESS;
            }
          })
          .catch(error => {
            console.log(
              'Notebook check fetching error (check your connection) : ' + error
            );
          })
          .finally(() => {
            if (
              this._ongoingCheckId === scopeId &&
              this._panel &&
              !this._panel.isDisposed
            ) {
              this._validityChecks.registered = currentRegistrationState;

              // only establish a socket connection once the notebook passed both the tag and registration checks
              if (
                this._validityChecks.registered === RegistrationState.SUCCESS
              ) {
                this._websocketManager.establishSocketConnection({
                  notebookId: this._validityChecks.tag as string
                });
              }
              this._panelUpdatedSignal.emit(void 0);
            }
          });
      }
    }
    // emit the signal when the panel is updated
    this._panelUpdatedSignal.emit(void 0);
  }

  // returns true if there is a list and it actually changed
  protected _updateCellList(): boolean {
    const cells = CompatibilityManager.getCellsArrComp(
      this.panel?.model?.cells
    );
    if (cells) {
      const cellList = cells.map(c => c.id);

      if (!areListsEqual(cellList, this._notebookCells)) {
        this._notebookCells = cellList;

        const notebookList: NotebookCell[] = cells.map(c => ({
          id: c.id,
          cellType: c.type
        }));

        // dispatch action for visualization dashboard update
        dispatch(setNotebookCells(notebookList));
        return true;
      }
    } else {
      this._notebookCells = null;
    }
    return false;
  }

  private _panel: NotebookPanel | null;
  // define a signal for panel updates
  private _panelUpdatedSignal = new Signal<PanelManager, void>(this);
  private _panelSwitchedSignal = new Signal<PanelManager, void>(this);
  private _monitor: ActivityMonitor<any, any> | null;
  private _notebookCells: string[] | null | undefined;
  // to define what should be rendered in DashboardPanel
  private _validityChecks: ValidityChecks;
  private _ongoingContextId = '';
  private _ongoingCheckId = '';

  private _websocketManager: WebsocketManager;
}
