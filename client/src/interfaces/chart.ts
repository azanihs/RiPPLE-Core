import * as d3 from "d3";

export interface Line {
    x1: number,
    x2: number,
    y1: number,
    y2: number
};
export interface Text {
    x: number,
    y: number,
    dy: number,
    dx: number,
    text: string
};
export interface Circle {
    original: any,
    cx: number,
    cy: number,
    r: number,
    transform: string
};
export interface ScatterPoint {
    value: number,
    fill: string
};
export interface ChartConfiguration {
    grid: boolean,
    gridLabels: boolean
    axis: boolean,
    axisLabels: boolean,
};
export interface DisplaySettings {
    width: number,
    height: number,
    depth: number,
    radius: number,
    xView: number,
    yView: number,
    zView: number
};

export interface ValueRange {
    x: number,
    y: number,
    z: number
};

export interface DOMContainer {
    scatter: d3.Selection<Element, Circle, Element, any>,
    axis: d3.Selection<Element, Line, Element, any>,
    grid: d3.Selection<Element, Line, Element, any>,
    axisLabels: d3.Selection<Element, Text, Element, any>,
    gridLabels: d3.Selection<Element, Text, Element, any>
};

export interface DataContainer {
    scatter: Circle[],
    axis: Line[],
    axisLabels: Text[],
    grid: Line[],
    gridLabels: Text[],
    [key: string]: null | any
};

