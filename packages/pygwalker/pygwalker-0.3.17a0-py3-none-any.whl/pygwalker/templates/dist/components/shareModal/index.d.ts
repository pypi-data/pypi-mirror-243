import React from "react";
import type { IGWHandler } from "@kanaries/graphic-walker/dist/interfaces";
import type { VizSpecStore } from '@kanaries/graphic-walker/dist/store/visualSpecStore';
interface IShareModal {
    gwRef: React.MutableRefObject<IGWHandler | null>;
    storeRef: React.MutableRefObject<VizSpecStore | null>;
    open: boolean;
    setOpen: (open: boolean) => void;
}
declare const ShareModal: React.FC<IShareModal>;
export default ShareModal;
