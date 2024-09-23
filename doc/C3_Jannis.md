:::mermaid
---
title: TEST
---

%% type of graph
%% graph LR
graph TD

Extern[Extern/User]
Input[Input]
Output[Output]

subgraph System[System]
    DataSelector[Data Selector] -->
    DataProcessor[Data Processor] -->
    DataLogger[Data Logger]
    end

%% main links
Extern --> Input --> System --> Output
:::

