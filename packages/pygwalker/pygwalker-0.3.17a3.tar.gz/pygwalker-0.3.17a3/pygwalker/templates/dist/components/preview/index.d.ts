import React from "react";
interface IPreviewProps {
    themeKey: string;
    charts: {
        visSpec: any;
        data: string;
    }[];
}
declare const Preview: React.FC<IPreviewProps>;
interface IChartPreviewProps {
    themeKey: string;
    visSpec: any;
    data: string;
    title: string;
    desc: string;
}
declare const ChartPreview: React.FC<IChartPreviewProps>;
export { Preview, ChartPreview, };
export type { IPreviewProps, IChartPreviewProps };
