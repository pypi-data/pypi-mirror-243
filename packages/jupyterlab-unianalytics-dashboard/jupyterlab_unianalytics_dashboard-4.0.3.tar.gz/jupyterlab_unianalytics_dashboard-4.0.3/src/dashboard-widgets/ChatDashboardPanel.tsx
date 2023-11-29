import * as React from 'react';
import DashboardPanel from './DashboardPanel';
import { PanelManager } from './PanelManager';
import { refreshIcon } from '@jupyterlab/ui-components';
import ChatContainer from '../chat-dashboard/ChatContainer';

export class ChatDashboardPanel extends DashboardPanel {
  constructor(panelManager: PanelManager) {
    super(panelManager);

    this.title.caption = 'Chat Dashboard';
    this.title.icon = refreshIcon;
    this.id = 'chat-dashboard';
    this.node.setAttribute('role', 'region');
    this.node.setAttribute('aria-label', 'Chat dashboard section');
  }

  protected computeComponentToRender(): React.ReactElement {
    const panel = this._panelManager.panel;
    const notebookId = this._panelManager.validityChecks.tag;
    if (panel && notebookId) {
      return <ChatContainer notebookId={notebookId} />;
    } else {
      return <></>;
    }
  }
}
