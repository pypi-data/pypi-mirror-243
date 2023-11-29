import { PLUGIN_ID } from '../utils/constants';
import { LabIcon } from '@jupyterlab/ui-components';
import chatStr from '../../style/icons/chat2.svg';

export const chatIcon = new LabIcon({
  name: `${PLUGIN_ID}:chat-icon`,
  svgstr: chatStr
});
